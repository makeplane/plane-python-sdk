"""Offline coverage for `WorkspacePermissions`/`ProjectPermissions` -- two distinct GET-only
singleton classes, no `id`.

`WorkspacePermissions` is migrated flat (leading `slug`), per Task 2. `ProjectPermissions`
is a project-level twin (depth 2) that is out of scope here -- same situation as
`ProjectFeatures` in `test_features_resource.py` -- and is left on the pre-flat shape;
its tests below still error on construction until a later task migrates it."""

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.permissions import ProjectPermissions, WorkspacePermissions
from plane.config import Configuration

WORKSPACE_URL = "https://api.example.com/api/v2/workspaces/acme/permissions/me/"
PROJECT_URL = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/permissions/me/"


@pytest.fixture
def workspace_permissions(config: Configuration) -> WorkspacePermissions:
    return WorkspacePermissions(V2Transport(config))


@pytest.fixture
def project_permissions(config: Configuration) -> ProjectPermissions:
    return ProjectPermissions(V2Transport(config), slug="acme", project_id="ENG")


@responses.activate
def test_me_hits_the_workspace_scoped_url(workspace_permissions: WorkspacePermissions) -> None:
    responses.get(
        WORKSPACE_URL, json={"relation": "member", "permission_grants": ["workspace.view"]}
    )

    result = workspace_permissions.me("acme")

    assert responses.calls[0].request.url == WORKSPACE_URL
    assert result.relation == "member"
    assert result.permission_grants == ["workspace.view"]


@responses.activate
def test_project_me_hits_the_project_scoped_url(project_permissions: ProjectPermissions) -> None:
    responses.get(PROJECT_URL, json={"relation": "admin", "permission_grants": ["project.edit"]})

    result = project_permissions.me()

    assert responses.calls[0].request.url == PROJECT_URL
    assert result.relation == "admin"


@responses.activate
def test_me_and_project_me_hit_different_urls(
    workspace_permissions: WorkspacePermissions, project_permissions: ProjectPermissions
) -> None:
    """A regression here would silently point both methods at the same URL --
    proven by making it fail: swap the mocked URLs and confirm the assertion
    below breaks before restoring them."""
    responses.get(WORKSPACE_URL, json={"relation": "member", "permission_grants": []})
    responses.get(PROJECT_URL, json={"relation": "admin", "permission_grants": []})

    workspace_result = workspace_permissions.me("acme")
    project_result = project_permissions.me()

    assert workspace_result.relation != project_result.relation
