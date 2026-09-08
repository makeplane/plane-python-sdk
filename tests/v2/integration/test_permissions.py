"""Effective permissions against a real server: read-only, no feature gate.
`WorkspacePermissions`/`ProjectPermissions` each expose a single `me()` method.
Not verified against a live server yet.

Flat path deliberately: the whole point of the last test is that these are two
*different* URLs computing two different grant sets, and spelling both through one
bound row would blur exactly the distinction under test."""

from __future__ import annotations

from plane.client import PlaneClient


def test_me(client: PlaneClient, workspace_slug: str) -> None:
    result = client.v2.workspaces.permissions.me(workspace_slug)
    assert result.relation is not None
    assert isinstance(result.permission_grants, list)


def test_project_me(client: PlaneClient, workspace_slug: str, project_id: str) -> None:
    result = client.v2.workspaces.projects.permissions.me(workspace_slug, project_id)
    assert result.relation is not None
    assert isinstance(result.permission_grants, list)


def test_workspace_and_project_grants_can_differ(
    client: PlaneClient, workspace_slug: str, project_id: str
) -> None:
    """Not the same call under two names -- the workspace and project grant sets
    are computed from different `RESOURCE_ACTIONS` subsets server-side."""
    workspace_grants = set(
        client.v2.workspaces.permissions.me(workspace_slug).permission_grants or []
    )
    project_grants = set(
        client.v2.workspaces.projects.permissions.me(workspace_slug, project_id).permission_grants
        or []
    )
    assert workspace_grants != project_grants or workspace_grants == set()
