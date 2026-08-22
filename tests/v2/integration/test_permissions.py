"""Effective permissions against a real server: read-only, no feature gate.
`WorkspacePermissions`/`ProjectPermissions` each expose a single `me()` method.
Not verified against a live server yet."""

from __future__ import annotations

from plane.client import PlaneClient


def test_me(client: PlaneClient, workspace_slug: str) -> None:
    result = client.v2.workspace(workspace_slug).permissions.me()
    assert result.relation is not None
    assert isinstance(result.permission_grants, list)


def test_project_me(client: PlaneClient, workspace_slug: str, project_id: str) -> None:
    result = client.v2.workspace(workspace_slug).project(project_id).permissions.me()
    assert result.relation is not None
    assert isinstance(result.permission_grants, list)


def test_workspace_and_project_grants_can_differ(
    client: PlaneClient, workspace_slug: str, project_id: str
) -> None:
    """Not the same call under two names -- the workspace and project grant sets
    are computed from different `RESOURCE_ACTIONS` subsets server-side."""
    ws = client.v2.workspace(workspace_slug)
    workspace_grants = set(ws.permissions.me().permission_grants or [])
    project_grants = set(ws.project(project_id).permissions.me().permission_grants or [])
    assert workspace_grants != project_grants or workspace_grants == set()
