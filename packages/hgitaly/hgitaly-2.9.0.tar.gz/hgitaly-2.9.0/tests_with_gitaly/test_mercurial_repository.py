# Copyright 2024 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import pytest
import random
import time

from grpc import RpcError, StatusCode
from psutil import Process

from heptapod.testhelpers.hg import RepoWrapper

from hgitaly.stub.mercurial_repository_pb2 import (
    HgCallRequest,
    MercurialPeer,
    PullRequest,
)
from hgitaly.stub.repository_pb2 import (
    CreateRepositoryRequest,
)
from hgitaly.stub.shared_pb2 import (
    Repository,
)

from hgitaly.stub.mercurial_repository_pb2_grpc import (
    MercurialRepositoryServiceStub,
)
from hgitaly.stub.repository_pb2_grpc import (
    RepositoryServiceStub,
)

from .rhgitaly import RHGitalyServer

from . import skip_comparison_tests
if skip_comparison_tests():  # pragma no cover
    pytestmark = pytest.mark.skip


parametrize = pytest.mark.parametrize


def test_rhgitaly_pull(rhgitaly, server_repos_root):
    fixture = rhgitaly
    repo_wrapper = fixture.hg_repo_wrapper
    rpc_helper = fixture.rpc_helper(stub_cls=MercurialRepositoryServiceStub,
                                    method_name='Pull',
                                    request_cls=PullRequest)

    src_repo_name = 'src-%s.hg' % hex(random.getrandbits(64))[2:]
    src_repo = RepoWrapper.init(server_repos_root / src_repo_name)
    src_hex = src_repo.commit_file('foo', message='foo-pull').hex()

    peer = MercurialPeer(url=str(src_repo.path))
    resp = rpc_helper.rpc('rhgitaly', remote_peer=peer)
    assert resp.new_changesets

    fixture.invalidate()
    assert repo_wrapper.repo[src_hex].description() == b'foo-pull'

    resp = rpc_helper.rpc('rhgitaly', remote_peer=peer)
    assert not resp.new_changesets


def test_rhgitaly_hg_call(rhgitaly, server_repos_root):
    fixture = rhgitaly
    repo_wrapper = fixture.hg_repo_wrapper
    rpc_helper = fixture.rpc_helper(stub_cls=MercurialRepositoryServiceStub,
                                    method_name='HgCall',
                                    request_cls=HgCallRequest)
    repo_wrapper.commit_file('foo')
    # a case without final line
    resps = list(rpc_helper.rpc('rhgitaly', args=[b'log', b'-T.']))
    assert len(resps) == 1
    resp = resps[0]
    assert resp.exit_code == 0
    assert resp.stdout == [b"."]

    # a case more realistic, as we probably will not expose this
    resps = list(rpc_helper.rpc('rhgitaly', args=[b'debugobsol']))
    resp = resps[0]
    assert resp.exit_code == 0
    assert resp.stdout == []

    # now with actual content
    repo_wrapper.amend_file('foo')
    resps = list(rpc_helper.rpc('rhgitaly', args=[b'debugobsol']))
    resp = resps[0]
    assert resp.exit_code == 0
    assert len(resp.stdout) == 1
    assert b"'operation': 'amend'" in resp.stdout[0]

    resps = list(rpc_helper.rpc('rhgitaly', args=[b'version', b'--debug']))


@parametrize('cause', ['client', 'server-shutdown'])
def test_pull_rhgitaly_termination(grpc_channel, server_repos_root, cause):
    # Here we are using the regular HGitaly grpc channel to create the repo,
    hgitaly_service = RepositoryServiceStub(grpc_channel)
    repo_path = 'repo-%s.hg' % hex(random.getrandbits(64))[2:]
    gl_repo = Repository(relative_path=repo_path, storage_name="default")
    hgitaly_service.CreateRepository(
        CreateRepositoryRequest(repository=gl_repo))

    sleeper_path = server_repos_root / 'sleeper'
    with open(sleeper_path, 'w') as sf:
        sf.writelines(("#!/bin/sh\n",
                       "echo $@\n",
                       "sleep 120\n"))

    sleeper_path.chmod(0o755)

    rhgitaly = RHGitalyServer(
        server_repos_root,
        socket_name='rhgitaly-oneshot.socket',
        sidecar_address='http://sidecar.example',  # no attempt to open channel
        env_overrides={'RHGITALY_HG_EXECUTABLE': str(sleeper_path)},
    )
    with rhgitaly.running() as rhgitaly_channel:
        mercurial_repo_service = MercurialRepositoryServiceStub(
            rhgitaly_channel)
        peer = MercurialPeer(url='/does/not/matter')
        async_meth = mercurial_repo_service.Pull.future
        future = async_meth(PullRequest(remote_peer=peer, repository=gl_repo))
        start = time.time()
        while time.time() - start < 1:
            rhgitaly_children = Process(rhgitaly.pid).children()
            sleepers = [p for p in rhgitaly_children if p.name() == 'sleeper']
            if sleepers:
                break
            time.sleep(0.01)

        sleeper = sleepers[0]

        if cause == 'client':
            future.cancel()
            # client lib will forbid us to call for the result, so we cannot
            # check that the server sends a `CANCELLED` status code.
            # But our major point is the termination of the subprocess

    if cause == 'server-shutdown':
        with pytest.raises(RpcError) as exc_info:
            future.result()
        assert exc_info.value.code() == StatusCode.CANCELLED
        assert 'Channel closed' in exc_info.value.details()

    # according to documentation at
    #   https://psutil.readthedocs.io/en/latest/#psutil.Process.is_running,
    # this does not suffer from PID recycling *and* detects zombies
    assert not sleeper.is_running()
