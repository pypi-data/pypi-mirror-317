// Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
//
// This software may be used and distributed according to the terms of the
// GNU General Public License version 2 or any later version.
// SPDX-License-Identifier: GPL-2.0-or-later
use std::fmt::{Debug, Formatter};
use std::sync::Arc;

use tokio_stream::StreamExt;
use tonic::{
    codegen::BoxStream, metadata::Ascii, metadata::MetadataValue, Request, Response, Status,
};
use tracing::{info, instrument};

use hg::revlog::NodePrefix;

use crate::config::Config;
use crate::gitaly::repository_service_client::RepositoryServiceClient;
use crate::gitaly::repository_service_server::{RepositoryService, RepositoryServiceServer};
use crate::gitaly::{
    FindMergeBaseRequest, FindMergeBaseResponse, GetArchiveRequest, GetArchiveResponse,
    HasLocalBranchesRequest, HasLocalBranchesResponse, ObjectFormat, ObjectFormatRequest,
    ObjectFormatResponse, Repository, RepositoryExistsRequest, RepositoryExistsResponse,
};
use crate::gitlab::revision::gitlab_revision_node_prefix;

use crate::gitlab::state::stream_gitlab_branches;
use crate::metadata::correlation_id;
use crate::repository::{
    checked_repo_path, default_repo_spec_error_status, load_changelog_and_then, repo_store_vfs,
    RepoSpecError, RequestWithRepo,
};
use crate::sidecar;
use crate::streaming::ResultResponseStream;
use crate::util::{bytes_strings_as_str, tracing_span_id};

#[derive(Debug)]
pub struct RepositoryServiceImpl {
    config: Arc<Config>,
    sidecar_servers: Arc<sidecar::Servers>,
}

#[tonic::async_trait]
impl RepositoryService for RepositoryServiceImpl {
    async fn repository_exists(
        &self,
        request: Request<RepositoryExistsRequest>,
    ) -> Result<Response<RepositoryExistsResponse>, Status> {
        let (metadata, _ext, inner) = request.into_parts();

        self.inner_repository_exists(inner, correlation_id(&metadata))
            .await
    }

    async fn object_format(
        &self,
        request: Request<ObjectFormatRequest>,
    ) -> Result<Response<ObjectFormatResponse>, Status> {
        let (metadata, _ext, inner) = request.into_parts();

        self.inner_object_format(inner, correlation_id(&metadata))
            .await
            .map(|v| Response::new(ObjectFormatResponse { format: v as i32 }))
    }

    async fn get_archive(
        &self,
        request: Request<GetArchiveRequest>,
    ) -> Result<Response<BoxStream<GetArchiveResponse>>, Status> {
        sidecar::fallback_server_streaming!(
            self,
            inner_get_archive,
            request,
            RepositoryServiceClient,
            get_archive
        )
    }

    async fn has_local_branches(
        &self,
        request: Request<HasLocalBranchesRequest>,
    ) -> Result<Response<HasLocalBranchesResponse>, Status> {
        let (metadata, _ext, inner) = request.into_parts();

        self.inner_has_local_branches(inner, correlation_id(&metadata))
            .await
            .map(|v| Response::new(HasLocalBranchesResponse { value: v }))
    }

    async fn find_merge_base(
        &self,
        request: Request<FindMergeBaseRequest>,
    ) -> Result<Response<FindMergeBaseResponse>, Status> {
        let (metadata, _ext, inner) = request.into_parts();

        self.inner_find_merge_base(inner, correlation_id(&metadata))
            .await
            .map(Response::new)
    }
}

impl RepositoryServiceImpl {
    #[instrument(name = "repository_exists", skip(self, request), fields(span_id))]
    async fn inner_repository_exists(
        &self,
        request: RepositoryExistsRequest,
        correlation_id: Option<&MetadataValue<Ascii>>,
    ) -> Result<Response<RepositoryExistsResponse>, Status> {
        tracing_span_id!();
        info!("Processing, repository={:?}", &request.repository);

        match checked_repo_path(&self.config, request.repository.as_ref()).await {
            Ok(_) => Ok(true),
            Err(RepoSpecError::RepoNotFound(_)) => Ok(false),
            Err(e) => Err(default_repo_spec_error_status(e)),
        }
        .map(|res| Response::new(RepositoryExistsResponse { exists: res }))
    }

    #[instrument(name = "object_format", skip(self, request), fields(span_id))]
    async fn inner_object_format(
        &self,
        request: ObjectFormatRequest,
        correlation_id: Option<&MetadataValue<Ascii>>,
    ) -> Result<ObjectFormat, Status> {
        tracing_span_id!();
        info!("Processing, repository={:?}", &request.repository);

        // return standard errors if repo does not exist, as Gitaly does
        repo_store_vfs(&self.config, &request.repository)
            .await
            .map_err(default_repo_spec_error_status)?;

        Ok(ObjectFormat::Unspecified)
    }

    #[instrument(name = "get_archive", skip(self, _request), fields(span_id))]
    async fn inner_get_archive(
        &self,
        _request: &GetArchiveRequest,
        correlation_id: Option<&MetadataValue<Ascii>>,
    ) -> ResultResponseStream<GetArchiveResponse> {
        tracing_span_id!();
        info!("Processing");
        Err(Status::unimplemented(""))
    }

    #[instrument(name = "has_local_branches", skip(self, request), fields(span_id))]
    async fn inner_has_local_branches(
        &self,
        request: HasLocalBranchesRequest,
        correlation_id: Option<&MetadataValue<Ascii>>,
    ) -> Result<bool, Status> {
        tracing_span_id!();
        info!("Processing, repository={:?}", &request.repository);

        let store_vfs = repo_store_vfs(&self.config, &request.repository)
            .await
            .map_err(default_repo_spec_error_status)?;
        if let Some(mut stream) = stream_gitlab_branches(&store_vfs).await.map_err(|e| {
            Status::internal(format!("Problem reading Gitlab branches file: {:?}", e))
        })? {
            Ok(stream.next().await.is_some())
        } else {
            Ok(false)
        }
    }

    #[instrument(name = "find_merge_base", skip(self, request), fields(span_id))]
    async fn inner_find_merge_base(
        &self,
        request: FindMergeBaseRequest,
        correlation_id: Option<&MetadataValue<Ascii>>,
    ) -> Result<FindMergeBaseResponse, Status> {
        tracing_span_id!();
        info!(
            "Processing, request={:?}",
            FindMergeBaseTracingRequest(&request)
        );

        if request.revisions.len() < 2 {
            return Err(Status::invalid_argument(
                "at least 2 revisions are required",
            ));
        }

        let store_vfs = repo_store_vfs(&self.config, &request.repository)
            .await
            .map_err(default_repo_spec_error_status)?;

        let mut nodes: Vec<NodePrefix> = Vec::with_capacity(request.revisions.len());
        // TODO perf we are reading potentially all state files for each revision, but we
        // have to hurry, to unblock Heptapod's own MRs.
        // (according to comments in protocol the case when there would be more than 2 revisions
        // is very unlikely).
        for revision in &request.revisions {
            match gitlab_revision_node_prefix(&store_vfs, revision)
                .await
                .map_err(|e| Status::internal(format!("Error resolving revision: {:?}", e)))?
            {
                None => {
                    info!(
                        "Revision {} not resolved",
                        String::from_utf8_lossy(revision)
                    );
                    return Ok(FindMergeBaseResponse::default());
                }
                Some(node_prefix) => {
                    nodes.push(node_prefix);
                }
            }
        }
        let maybe_gca_node = load_changelog_and_then(
            self.config.clone(),
            request,
            default_repo_spec_error_status,
            move |_req, _repo, cl| {
                // TODO unwrap*2
                let revs: Result<Vec<_>, _> =
                    nodes.into_iter().map(|n| cl.rev_from_node(n)).collect();
                let revs = revs.map_err(|e| {
                    Status::internal(format!(
                        "Inconsistency: Node ID from GitLab state file \
                     or received from client could not be resolved {:?}",
                        e
                    ))
                })?;
                Ok(cl
                    .get_index()
                    .ancestors(&revs)
                    .map_err(|e| Status::internal(format!("GraphError: {:?}", e)))?
                    .first()
                    .and_then(|rev| cl.node_from_rev((*rev).into()))
                    .copied())
            },
        )
        .await?;

        Ok(
            maybe_gca_node.map_or_else(FindMergeBaseResponse::default, |node| {
                FindMergeBaseResponse {
                    base: format!("{:x}", node),
                }
            }),
        )
    }
}

/// Takes care of boilerplate that would instead be in the startup sequence.
pub fn repository_server(
    config: &Arc<Config>,
    sidecar_servers: &Arc<sidecar::Servers>,
) -> RepositoryServiceServer<RepositoryServiceImpl> {
    RepositoryServiceServer::new(RepositoryServiceImpl {
        config: config.clone(),
        sidecar_servers: sidecar_servers.clone(),
    })
}

impl RequestWithRepo for FindMergeBaseRequest {
    fn repository_ref(&self) -> Option<&Repository> {
        self.repository.as_ref()
    }
}

struct FindMergeBaseTracingRequest<'a>(&'a FindMergeBaseRequest);

impl Debug for FindMergeBaseTracingRequest<'_> {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("FindMergeBaseRequest")
            .field("repository", &self.0.repository)
            .field("revisions", &bytes_strings_as_str(&self.0.revisions))
            .finish()
    }
}
