// Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
//
// This software may be used and distributed according to the terms of the
// GNU General Public License version 2 or any later version.
// SPDX-License-Identifier: GPL-2.0-or-later
use futures_core::Future;
use std::ffi::{OsStr, OsString};
use std::fmt;
use std::io::ErrorKind;
use std::marker::Send;
use std::os::unix::ffi::OsStringExt;
use std::path::{Path, PathBuf};
use std::process::Stdio;
use std::sync::Arc;

use futures::executor::block_on;

use tokio::fs;
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::process::Command;
use tokio::select;
use tokio::sync::mpsc::{self, Sender};
use tokio::task::JoinError;
use tokio_stream::wrappers::ReceiverStream;
use tokio_stream::StreamExt;
use tokio_util::sync::CancellationToken;
use tonic::codegen::BoxStream;
use tonic::metadata::MetadataMap;
use tonic::{Response, Status, Streaming};
use tracing::{debug, info, span::Span, warn};

use hg::changelog::Changelog;
use hg::repo::{Repo, RepoError};

use super::config::Config;
use super::gitaly::{Repository, User};
use super::metadata::{
    get_boolean_md_value, ACCEPT_MR_IID_KEY, HG_GIT_MIRRORING_MD_KEY, NATIVE_PROJECT_MD_KEY,
    SKIP_HOOKS_MD_KEY,
};
use super::process;
use super::streaming::{empty_response_stream, BlockingResponseSender, WRITE_BUFFER_SIZE};

/// Represent errors that are due to a wrong repository specification.
///
/// In terms of gRPC methods, the specifications is usually enclosed in  a [`Repository`] message
/// and these errors are considered to be client errors.
#[derive(Debug, PartialEq, Eq)]
pub enum RepoSpecError {
    MissingSpecification,
    UnknownStorage(String),
    RepoNotFound(PathBuf),
}

/// Represent errors loading a repository (bad specification or internal errors)
#[derive(Debug, derive_more::From)] // TODO add PartialEq, but do it in core for RepoError first
pub enum RepoLoadError {
    #[from]
    SpecError(RepoSpecError),
    LoadError(RepoError),
}

impl From<RepoError> for RepoLoadError {
    fn from(value: RepoError) -> Self {
        if let RepoError::NotFound { at } = value {
            return Self::SpecError(RepoSpecError::RepoNotFound(at));
        }
        Self::LoadError(value)
    }
}

/// Default conversion of ['RepoSpecError'] into a gRPC ['Status']
///
/// This function does not care to precisely match the error details, focusing on the error
/// codes instead.
///
/// The resulting codes match the most common behaviour of Gitaly, which actually behaves more
/// and more like this with time (e.g., as internal Git error get catched and handled).
pub fn default_repo_spec_error_status(err: RepoSpecError) -> Status {
    match err {
        RepoSpecError::MissingSpecification => Status::invalid_argument("repository not set"),
        RepoSpecError::UnknownStorage(storage) => Status::invalid_argument(format!(
            "GetStorageByName: no such storage: \"{}\"",
            storage
        )),
        RepoSpecError::RepoNotFound(at) => {
            Status::not_found(format!("repository at \"{}\" not found", at.display()))
        }
    }
}

pub fn repo_path(config: &Config, repo: &Repository) -> Result<PathBuf, RepoSpecError> {
    if repo.storage_name != "default" {
        return Err(RepoSpecError::UnknownStorage(repo.storage_name.clone()));
    }
    let root = &config.repositories_root;

    let res = match repo.relative_path.strip_suffix(".git") {
        Some(stripped) => root.join(stripped.to_owned() + ".hg"),
        None => root.join(&repo.relative_path),
    };

    // TODO forbid climbing up (same in Python, will be necessary for HGitaly3, even
    // though clients are deeply trusted.
    Ok(res)
}

/// Default gRPC error ['Status'] for repository not found.
///
/// To be used if repository path does not exist on disk.
pub fn default_repo_not_found_error_status(path: &Path) -> Status {
    Status::not_found(format!(
        "Mercurial repository at {} not found",
        path.display()
    ))
}

pub async fn checked_repo_path<'a>(
    config: &Config,
    gl_repo: Option<&'a Repository>,
) -> Result<(&'a Repository, PathBuf), RepoSpecError> {
    let repo = gl_repo
        .as_ref()
        .ok_or(RepoSpecError::MissingSpecification)?;
    let path = repo_path(config, repo)?;
    if match fs::metadata(&path).await {
        Ok(md) => md.is_dir(),
        Err(_) => false,
    } {
        return Ok((repo, path));
    }
    Err(RepoSpecError::RepoNotFound(path))
}

/// Return a path to virtual filesystem for the repository store.
///
/// As of this writing, this is nothing but a [`Path`], but it could become something
/// more advanced in the future (perhaps not as much as `hg_core` `Vfs` type, though).
///
/// Parameter `repo` is an `Option`, so that a service method can pass directly
/// something like `&request.repository`, with `None` giving rise to the natural
/// `MissingSpecification` error.
///
/// If the repository is not found on disc, the appropriate error is also returned.
pub async fn repo_store_vfs(
    config: &Config,
    repo: &Option<Repository>,
) -> Result<PathBuf, RepoSpecError> {
    let root = checked_repo_path(config, repo.as_ref()).await?.1;
    Ok(root.join(".hg/store"))
}

/// Read repository VFS requirements and tell whether one fulfills the given condition
///
/// Note that some requirements are in the 'store` VFS (most of those that
/// will be of interest with RHGitaly), while some others are on the 'working dir' VFS.
///
/// Inspired by [`hg::requirements::load`] with thw following differences:
///
/// - we do not need to build a full `HashSet`, just to check a single value. If the caller
///   needs to use the requirements repeatedly, we will provide a more general parsing function
///   with storable results.
/// - this is async
pub async fn has_requirement_with(
    vfs: &Path,
    condition: impl FnMut(&[u8]) -> bool,
) -> Result<bool, Status> {
    let path = vfs.join("requires"); // TODO const
    let reqs = match fs::read(&path).await {
        Ok(bytes) => bytes,
        Err(e) => {
            if e.kind() == ErrorKind::NotFound {
                return Ok(false);
            } else {
                return Err(Status::internal(format!(
                    "Could not open requirements at {}: {}",
                    path.display(),
                    e
                )));
            }
        }
    };
    Ok(reqs.split(|b| *b == b'\n').any(condition))
}

/// Return `Status::Unimplemented` if the repo has the `largefiles` requirement.
pub async fn unimplemented_if_largefiles(
    config: &Config,
    repo: &Option<Repository>,
) -> Result<(), Status> {
    let store_vfs = repo_store_vfs(config, repo)
        .await
        .map_err(default_repo_spec_error_status)?;
    if has_requirement_with(&store_vfs, |req| req == b"largefiles").await? {
        // TODO const
        return Err(Status::unimplemented("largefiles repo requirement"));
    };
    // The requires file can be in the working dir vfs (probably older
    // repositories, that don't have any .hg/store/requires)
    if let Some(root_vfs) = store_vfs.parent() {
        if has_requirement_with(root_vfs, |req| req == b"largefiles").await? {
            // TODO const
            return Err(Status::unimplemented("largefiles repo requirement"));
        }
    }
    Ok(())
}

pub fn load_repo_at(config: &Config, repo_path: PathBuf) -> Result<Repo, RepoError> {
    // TODO better to use Repo::new_at_path, but it is private
    // (Repo::find does verifications that are useless to us.
    // At least it does not try to climb up when passed an explicit path)
    Repo::find(&config.hg_core_config, Some(repo_path))
}

pub fn load_repo(config: &Config, opt_repo: Option<&Repository>) -> Result<Repo, RepoLoadError> {
    Ok(load_repo_at(
        config,
        repo_path(config, opt_repo.ok_or(RepoSpecError::MissingSpecification)?)?,
    )?)
}

/// Trait for requests with a repository field
///
/// It provides the needed uniformity for methods such as [`load_repo_and_stream`]
pub trait RequestWithRepo: Send + 'static {
    /// Grab a reference to the [`Repository`] field from the request.
    ///
    /// Like all submessages, the repository is optional.
    fn repository_ref(&self) -> Option<&Repository>;
}

/// Trait for requests whose treatment involves spawning a hg child process
///
/// It provides the needed uniformity for [`HgSpawner`]
pub trait RequestHgSpawnable: RequestWithRepo {
    /// Grab a reference to the [`User`] field from the request.
    ///
    /// Like all submessages, the user is optional if it is indeed part of protocol.
    ///
    /// In the case of read-only gRPC methods, it is totally acceptable not to have
    /// any [`User`] field, whence the blanket implementation returning `None`.
    fn user_ref(&self) -> Option<&User> {
        None
    }
}

/// Load a repository and initiate streaming responses
///
/// This setups the `mpsc` channel expected by Tonic and spawns a blocking task (typically run
/// in a separate thread) loads the repository, and passes over the repository and the transmitting
/// end of the channel to the caller supplied closure.
///
/// The `and_then` closure must perform its streaming by sending `Result<Resp, Status>` values
/// on the channel, using the provided [`BlockingResponseSender`].
///
/// If the repository loading fails, the appropriate gRPC error response is sent over
/// or logged if sending is not possible.
///
/// Because Gitaly's error responses are not uniform, and we want to match them closely,
/// ethe caller has to supply a callable for conversion of [`RepoSpecError`] to the appropriate
/// [`Status`]. The [`default_repo_spec_error_status`] function can be used in the majority of
/// cases and serve as an example for other cases.
pub fn load_repo_and_stream<Req: RequestWithRepo, Resp: fmt::Debug + Send + 'static>(
    config: Arc<Config>,
    request: Req,
    repo_spec_error_status: impl Fn(RepoSpecError) -> Status + Send + 'static,
    and_then: impl FnOnce(Req, Repo, BlockingResponseSender<Resp>) + Send + 'static,
) -> Result<Response<BoxStream<Resp>>, Status> {
    // no point having channel capacity for several messages, since `blocking_send` is the only
    // way to use it.
    let (tx, rx) = mpsc::channel(1);
    let current_span = Span::current();
    tokio::task::spawn_blocking(move || {
        let btx: BlockingResponseSender<Resp> = tx.into();
        let _entered = current_span.enter();
        match load_repo(&config, request.repository_ref()) {
            Err(RepoLoadError::SpecError(e)) => btx.send(Err(repo_spec_error_status(e))),
            Err(RepoLoadError::LoadError(e)) => btx.send(Err(Status::internal(format!(
                "Error loading repository: {:?}",
                e
            )))),
            Ok(repo) => and_then(request, repo, btx),
        }
    });
    Ok(Response::new(Box::pin(ReceiverStream::new(rx))))
}

/// Load a repo and run closures for a bidirectional gRPC method
///
/// Similar to [`load_repo_and_stream`] except that the request is actually a stream
/// and the closure is called repeatedly, once per request message, hence there is
/// at least one response message per request message.
///
/// The repository is loaded from the first request message, the additional boolean argument
/// to the closure tells it if it is called on the first message.
///
/// Possible improvements: consume the request faster, parking the values using another
/// inner channel.
pub async fn load_repo_and_stream_bidir<
    Req: RequestWithRepo,
    T,
    Resp: fmt::Debug + Send + 'static,
>(
    config: Arc<Config>,
    mut request: Streaming<Req>,
    repo_spec_error_status: impl Fn(RepoSpecError) -> Status + Send + 'static,
    treat_first: impl Fn(Req, &Repo, &BlockingResponseSender<Resp>) -> T + Send + 'static,
    treat_subsequent: impl Fn(Req, &T, &Repo, &BlockingResponseSender<Resp>) + Send + 'static,
) -> Result<Response<BoxStream<Resp>>, Status> {
    // no point having channel capacity for several messages, since `blocking_send` is the only
    // way to use it.
    let (tx, rx) = mpsc::channel(1);
    let current_span = Span::current();
    if let Some(first_res) = request.next().await {
        let first_req = first_res?; // TODO provide specific error treatment

        tokio::task::spawn_blocking(move || {
            let btx: BlockingResponseSender<Resp> = tx.into();
            let _entered = current_span.enter();
            match load_repo(&config, first_req.repository_ref()) {
                Err(RepoLoadError::SpecError(e)) => btx.send(Err(repo_spec_error_status(e))),
                Err(RepoLoadError::LoadError(e)) => btx.send(Err(Status::internal(format!(
                    "Error loading repository: {:?}",
                    e
                )))),
                Ok(repo) => {
                    let first_out = treat_first(first_req, &repo, &btx);
                    while let Some(res) = block_on(request.next()) {
                        match res {
                            Err(e) => btx.send(Err(e)), // TODO expose specific error treatment
                            Ok(req) => treat_subsequent(req, &first_out, &repo, &btx),
                        }
                    }
                }
            }
        });
        Ok(Response::new(Box::pin(ReceiverStream::new(rx))))
    } else {
        empty_response_stream()
    }
}

fn blocking_join_error_status(err: JoinError) -> Status {
    if err.is_cancelled() {
        // According to https://grpc.io/docs/guides/error/, it should be
        // `Unavailable()` if this is a graceful shutdown, but now the question is how
        // to tell that apart from user cancellation.
        Status::cancelled("Inner blocking task on Mercurial repo was cancelled")
    } else {
        Status::internal(format!("Unexpected error in inner thread: {:?}", err))
    }
}

/// Load a repository in a separate thread and hand it over to a closure
///
/// This creates a new thread suitable for blocking operations, using
/// [`tokio::task::spawn_blocking`] and then hands it over together with the orignal request
/// to the `and_then` closure, whose return value is finally returned to the caller.
/// The closure is at liberty to use any blocking operation (most calls to `hg-core` are blocking).
///
/// If the repository loading fails, the appropriate gRPC error [`Status`] is returned
///
/// `repo_spec_error_status` plays the same role as in [`load_repo_and_stream`], and again
/// the [`default_repo_spec_error_status`] function can be used in the majority of
/// cases.
pub async fn load_repo_and_then<Req: RequestWithRepo, Res: Send + 'static>(
    config: Arc<Config>,
    request: Req,
    repo_spec_error_status: impl Fn(RepoSpecError) -> Status + Send + 'static,
    and_then: impl FnOnce(Req, Repo) -> Result<Res, Status> + Send + 'static,
) -> Result<Res, Status> {
    let current_span = Span::current();
    tokio::task::spawn_blocking(move || {
        let _entered = current_span.enter();
        match load_repo(&config, request.repository_ref()) {
            Err(RepoLoadError::SpecError(e)) => Err(repo_spec_error_status(e)),
            Err(RepoLoadError::LoadError(e)) => Err(Status::internal(format!(
                "Error loading repository: {:?}",
                e
            ))),
            Ok(repo) => and_then(request, repo),
        }
    })
    .await
    .map_err(blocking_join_error_status)?
}

async fn load_repo_at_and_then<Res: Send + 'static>(
    config: Arc<Config>,
    repo_path: PathBuf,
    and_then: impl FnOnce(Repo) -> Result<Res, Status> + Send + 'static,
) -> Result<Res, Status> {
    let current_span = Span::current();
    tokio::task::spawn_blocking(move || {
        let _entered = current_span.enter();
        match load_repo_at(&config, repo_path) {
            Err(e) => Err(Status::internal(format!(
                "Error loading repository: {:?}",
                e
            ))),
            Ok(repo) => and_then(repo),
        }
    })
    .await
    .map_err(blocking_join_error_status)?
}

pub struct HgSpawnerTemplate {
    config: Arc<Config>,
    common_args: Vec<OsString>,
    common_env: Vec<(OsString, OsString)>,
    repo_path: PathBuf,
}

pub struct HgSpawner {
    config: Arc<Config>,
    cmd: Command,
    stdout_tx: Option<Sender<Vec<u8>>>,
    repo_path: PathBuf,
}

/// Serialize booleans in the same way as was done by heptapod-rails.
///
/// The `"true"` and `"false"` strings would work the same way, but would
/// create differences in `hg config` output, as it just repeats the configuration
/// as it was passed.
fn hg_config_bool2str(b: bool) -> &'static str {
    if b {
        "yes"
    } else {
        "no"
    }
}

impl HgSpawnerTemplate {
    /// Reusable preparations to instantiate [`HgSpawner`] objects
    ///
    /// If the request specifies an [`User`], all necessary environment variables are given to
    /// the child process so that repository mutation on behalf of the given user can work.
    /// This is similar to the legacy code in the Rails application. A difference lies in the way
    /// the (usually necessary) `HGRCPATH` environment variable is given to the child process:
    /// nothing special is done about it, hence it is assumed it is set on the whole RHGitaly
    /// service.
    pub async fn new<Req: RequestHgSpawnable>(
        config: Arc<Config>,
        request: Req,
        metadata: &MetadataMap,
        repo_spec_error_status: impl Fn(RepoSpecError) -> Status + Send + 'static + Copy,
    ) -> Result<Self, Status> {
        let (gitaly_repo, repo_path) = checked_repo_path(&config, request.repository_ref())
            .await
            .map_err(repo_spec_error_status)?;
        let mut common_args = Vec::new();
        let mut common_env: Vec<(OsString, OsString)> = vec![
            (
                "GL_REPOSITORY".to_owned().into(),
                gitaly_repo.gl_repository.clone().into(),
            ),
            // same hardcoding as in Gitaly
            ("GL_PROTOCOL".to_owned().into(), "web".to_owned().into()),
        ];

        debug!("Invocation metadata: {:?}", &metadata);
        let mirroring = get_boolean_md_value(metadata, HG_GIT_MIRRORING_MD_KEY, false);
        let native = get_boolean_md_value(metadata, NATIVE_PROJECT_MD_KEY, false);
        let skip_gl_hooks = get_boolean_md_value(metadata, SKIP_HOOKS_MD_KEY, false);

        common_args.push("--config".to_owned().into());
        common_args.push(format!("heptapod.native={}", hg_config_bool2str(native)).into());
        common_args.push("--config".to_owned().into());
        common_args.push(format!("heptapod.no-git={}", !mirroring).into());

        if skip_gl_hooks {
            common_env.push((
                "'HEPTAPOD_SKIP_ALL_GITLAB_HOOKS'".to_owned().into(),
                "yes".to_owned().into(),
            ));
        }

        if let Some(user) = request.user_ref() {
            common_env.push((
                "HEPTAPOD_USERINFO_GL_ID".to_owned().into(),
                user.gl_id.clone().into(),
            ));
            common_env.push((
                "HEPTAPOD_USERINFO_USERNAME".to_owned().into(),
                user.gl_username.clone().into(),
            ));
            common_env.push((
                "HEPTAPOD_USERINFO_NAME".to_owned().into(),
                OsString::from_vec(user.name.clone()),
            ));
            common_env.push((
                "HEPTAPOD_USERINFO_EMAIL".to_owned().into(),
                OsString::from_vec(user.email.clone()),
            ));

            if let Some(v) = metadata.get(ACCEPT_MR_IID_KEY) {
                if let Ok(iid) = v.to_str() {
                    common_env.push(("HEPTAPOD_ACCEPT_MR_IID".to_owned().into(), iid.into()));
                }
            }
        }

        Ok(Self {
            common_args,
            common_env,
            config,
            repo_path,
        })
    }

    pub fn spawner(&self) -> HgSpawner {
        let mut cmd = Command::new(&self.config.hg_executable);
        cmd.args(&self.common_args);
        cmd.envs(self.common_env.iter().map(|item| (&item.0, &item.1)));
        cmd.current_dir(&self.repo_path);

        HgSpawner {
            cmd,
            config: self.config.clone(),
            repo_path: self.repo_path.clone(),
            stdout_tx: None,
        }
    }

    /// Spawn a `hg log` subprocess on the given revsec, return a vector
    /// of Node Ids (hexadecimal representation)
    pub async fn log(
        &self,
        revset: &OsStr,
        cancel_token: CancellationToken,
        limit: Option<usize>,
    ) -> Result<Vec<String>, Status> {
        let mut spawner = self.spawner();

        let mut args: Vec<OsString> = vec![
            "log".to_owned().into(),
            "-r".to_owned().into(),
            revset.to_owned(),
            "-T{node}\\n".to_owned().into(),
        ];
        if let Some(limit) = limit {
            args.push(format!("-l{}", limit).into())
        }
        let (stdout_tx, mut stdout_rx) = mpsc::channel(3);
        spawner.capture_stdout(stdout_tx);
        spawner.args(&args);
        let spawned = spawner.spawn(cancel_token);
        let mut changesets = Vec::new();
        let read_stdout = async {
            while let Some(mut line) = stdout_rx.recv().await {
                if line.last() == Some(&b'\n') {
                    line.pop();
                }
                match String::from_utf8(line) {
                    Ok(changeset) => changesets.push(changeset),
                    Err(e) => {
                        // actually returning an Err from there is really painful and this can
                        // happen in pratice only if `hg` is very buggy (been replaced by something
                        // else?).
                        warn!(
                            "Unexpected non utf-8 `hg log -T '{{node}}\\n'` output: {:?}",
                            e.as_bytes()
                        )
                    }
                };
            }
        };
        let spawn_result = tokio::join!(spawned, read_stdout).0;
        let hg_exit_code = spawn_result?;
        if hg_exit_code != 0 {
            return Err(Status::internal(format!(
                "Mercurial subprocess exited with code {}",
                hg_exit_code
            )));
        }
        Ok(changesets)
    }
}

impl HgSpawner {
    /// Object to spawn a `hg` child process on the repository specified by the request
    ///
    /// First repository loading is similar to [`load_repo_and_then`], executing the provided
    /// `before_spawn` closure on the repository and the prepared [`Command`].
    ///
    /// The entire environment of the current process is passed down to the child process.
    ///
    /// The path to the `hg` executable is taken from `Config`.
    pub async fn prepare<Req: RequestHgSpawnable>(
        config: Arc<Config>,
        request: Req,
        metadata: &MetadataMap,
        repo_spec_error_status: impl Fn(RepoSpecError) -> Status + Send + 'static + Copy,
    ) -> Result<Self, Status> {
        Ok(
            HgSpawnerTemplate::new(config, request, metadata, repo_spec_error_status)
                .await?
                .spawner(),
        )
    }

    /// Convenience method similar to [`load_repo_and_then`]
    ///
    /// It is typically used to gather information from the repository to tweak arguments.
    ///
    /// Compared to calling [`load_repo_and_then`, it avoids redoing some checks already done
    /// and passing some arguments again. Also, since the closure does not take a request
    /// argument, it also prevents some unnecessary cloning (just extract the needed information
    /// from the request in the caller task before hand).
    pub fn load_repo_and_then<Res: Send + 'static>(
        &self,
        and_then: impl FnOnce(Repo) -> Result<Res, Status> + Send + 'static,
    ) -> impl Future<Output = Result<Res, Status>> {
        load_repo_at_and_then(self.config.clone(), self.repo_path.clone(), and_then)
    }

    /// Configure for stdout capture.
    ///
    /// With this, the child process standard output will be captured and
    /// sent line by line over it.
    /// In general, other means of obtaining information should be preferred, but there is
    /// sometimes nothing else that can be used.
    pub fn capture_stdout(&mut self, tx: Sender<Vec<u8>>) {
        self.stdout_tx = Some(tx);
    }

    /// Set child process arguments
    pub fn args<Arg: AsRef<OsStr>>(&mut self, args: impl IntoIterator<Item = Arg>) {
        self.cmd.args(args);
    }

    /// Run the `hg` process asynchronously.
    ///
    /// The entire environment of the current process is passed down to the child process. Notably
    /// this is how `HGRCPATH` is supposed to be set (see comment about that in
    /// [prepare](`Self::prepare`)).
    pub async fn spawn(mut self, shutdown_token: CancellationToken) -> Result<i32, Status> {
        if self.stdout_tx.is_some() {
            self.cmd.stdout(Stdio::piped());
        }
        debug!("Spawning command {:#?}", self.cmd);
        let shutdown_token = shutdown_token.clone();
        let mut hg = self
            .cmd
            .spawn()
            .map_err(|e| Status::internal(format!("Error spawning Mercurial subprocess: {}", e)))?;

        let stdout_and_tx = self.stdout_tx.take().map(|stdtx| {
            (
                hg.stdout
                    .take()
                    .expect("Spawned process has no stdout (already been taken?)"),
                stdtx,
            )
        });

        let token = CancellationToken::new();
        let _drop_guard = token.clone().drop_guard();

        let (tx, mut rx) = mpsc::channel(1);
        tokio::spawn(async move {
            let hg_status = select! {
                res = hg.wait() => res.map_err(|e| {
                    Status::internal(
                        format!("Error waiting for Mercurial subprocess: {}", e))
                    }),
                _ = token.cancelled() => {
                    // TODO logs from a subthread are not in the context of the request
                    // hence will turn pretty useless without correlation_id etc.
                    info!("Task cancelled, terminating Mercurial child process with SIGTERM");
                    process::terminate(hg).await;
                    Err(Status::cancelled("Task dropped, probably due to \
                                           client-side cancellation"))
                },
                _ = shutdown_token.cancelled() => {
                    warn!("General shutdown required, terminating Mercurial child \
                           process with SIGTERM");
                    process::terminate(hg).await;
                    Err(Status::unavailable("RHGitaly server is shutting down"))
                },
            };
            tx.send(hg_status).await
        });

        let hg_status = if let Some((stdout, stdout_tx)) = stdout_and_tx {
            let mut reader = BufReader::new(stdout);

            async move {
                let hg_status: Result<_, Status>;
                let mut buf = Vec::with_capacity(*WRITE_BUFFER_SIZE);
                loop {
                    select! {
                        maybe_bytes = reader.read_until(b'\n', &mut buf) => {
                            match maybe_bytes {
                                Ok(0) => {},
                                Ok(n) => {
                                    info!("Line: read {} bytes from subprocess stdout", n);
                                    // it seems that a vector clone has capacity==length
                                    // (perfect in this case)
                                    if stdout_tx.send(buf.clone()).await.is_err() {
                                        // we have no other choice than ignoring it,
                                        // although it is probably symptom
                                        // of some really unexpected problem
                                        warn!("Subprocess stdout receiver already dropped!")
                                    }
                                    buf.clear();
                                },
                                Err(e) => {
                                    // probably the error is not due to stdout already closed, but
                                    // in any case, we must let the other arm of `select!` run so
                                    // that the process is eventually reaped
                                    warn!("Got error reading from child process stdout: {}", e)
                                }
                            }
                        },
                        res = rx.recv() => {
                            hg_status = res.unwrap_or_else(|| Err(Status::internal(
                                "Channel closed before sending back Mercurial subprocess status")));
                            break;
                        }
                    }
                }
                hg_status
            }
            .await?
        } else {
            rx.recv().await.unwrap_or_else(|| {
                Err(Status::internal(
                    "Channel closed before sending back Mercurial subprocess status",
                ))
            })?
        };

        hg_status.code().ok_or(Status::internal(
            "Mercurial subprocess killed or stopped by signal",
        ))
    }
}

/// Load a repository and its changelog in a separate thread and hand it over to a closure
///
/// See [`load_repo_and_then`] on which this builds upon for more details.
pub async fn load_changelog_and_then<Req: RequestWithRepo, Res: Send + 'static>(
    config: Arc<Config>,
    request: Req,
    repo_spec_error_status: impl Fn(RepoSpecError) -> Status + Send + 'static,
    and_then: impl FnOnce(Req, &Repo, &Changelog) -> Result<Res, Status> + Send + 'static,
) -> Result<Res, Status> {
    load_repo_and_then(config, request, repo_spec_error_status, |req, repo| {
        let cl = repo
            .changelog()
            .map_err(|e| Status::internal(format!("Could not open changelog: {:?}", e)))?;
        and_then(req, &repo, &cl)
    })
    .await
}

/// Load a repository and its changelog in a separate thread for streaming responses
///
/// See [`load_repo_and_stream`] on which this builds upon for more details.
pub fn load_changelog_and_stream<Req: RequestWithRepo, Resp: fmt::Debug + Send + 'static>(
    config: Arc<Config>,
    request: Req,
    repo_spec_error_status: impl Fn(RepoSpecError) -> Status + Send + 'static,
    and_then: impl FnOnce(Req, &Repo, &Changelog, BlockingResponseSender<Resp>) + Send + 'static,
) -> Result<Response<BoxStream<Resp>>, Status> {
    load_repo_and_stream(
        config,
        request,
        repo_spec_error_status,
        |req, repo, tx| match repo.changelog() {
            Ok(cl) => and_then(req, &repo, &cl, tx),
            Err(e) => tx.send(Err(Status::internal(format!(
                "Could not open changelog: {:?}",
                e
            )))),
        },
    )
}

#[cfg(test)]
mod tests {

    use super::*;
    use crate::gitaly::ServerInfoRequest;

    #[test]
    fn test_repo_path() {
        let mut config = Config::default();
        config.repositories_root = "/repos".into();
        let mut repo = Repository::default();
        repo.storage_name = "default".into();
        repo.relative_path = "foo/bar".into();
        assert_eq!(repo_path(&config, &repo), Ok("/repos/foo/bar".into()));

        repo.relative_path = "foo/bar.git".into();
        assert_eq!(repo_path(&config, &repo), Ok("/repos/foo/bar.hg".into()));
    }

    impl RequestWithRepo for ServerInfoRequest {
        fn repository_ref(&self) -> Option<&Repository> {
            None // would not be acceptable in main code
        }
    }
    impl RequestHgSpawnable for ServerInfoRequest {}

    #[test]
    fn test_request_hg_spawnable() {
        assert!(ServerInfoRequest::default().user_ref().is_none());
    }
}
