"""`proj.members`/`ws.members` against a real server; `WorkspaceMembers.remove`
is deliberately not exercised on a real member -- it cascades a deactivation
through every project and isn't reversible, so only its error contract is tested."""

from __future__ import annotations

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.members import ProjectMembers, WorkspaceMembers
from plane.client import PlaneClient
from plane.models.v2.members import UpdateProjectMember, WorkspaceMemberRemove

from .helpers import unique_name


@pytest.fixture
def project_members(client: PlaneClient, workspace_slug: str, project_id: str) -> ProjectMembers:
    return client.v2.workspace(workspace_slug).project(project_id).members


@pytest.fixture
def workspace_members(client: PlaneClient, workspace_slug: str) -> WorkspaceMembers:
    return client.v2.workspace(workspace_slug).members


class TestProjectMembers:
    def test_list_includes_the_project_creator(self, project_members: ProjectMembers) -> None:
        """A freshly created project always has at least the creator as a
        member (verified live via the shared session `project` fixture)."""
        page = project_members.list()
        assert page.data

    def test_retrieve_then_update_role(self, project_members: ProjectMembers) -> None:
        existing = project_members.list().data[0]

        fetched = project_members.retrieve(existing.id)
        assert fetched.id == existing.id

        updated = project_members.update(existing.id, UpdateProjectMember(role=fetched.role))
        assert updated.id == existing.id

    def test_expand_member_rejects_an_unknown_relation(
        self, project_members: ProjectMembers
    ) -> None:
        with pytest.raises(ValueError, match="bogus"):
            project_members.list(expand=["bogus"])

    def test_retrieve_missing_row_404s(self, project_members: ProjectMembers) -> None:
        missing_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(PlaneAPIError) as exc_info:
            project_members.retrieve(missing_id)
        assert exc_info.value.status == 404


class TestWorkspaceMembers:
    def test_list_includes_at_least_the_api_principal(
        self, workspace_members: WorkspaceMembers
    ) -> None:
        page = workspace_members.list()
        assert page.data

    def test_remove_unknown_email_is_a_clean_error(
        self, workspace_members: WorkspaceMembers
    ) -> None:
        """Non-destructive: `unique_name` guarantees this email resolves to no
        one, so `remove` cannot actually deactivate a real member here."""
        bogus_email = f"{unique_name('nobody')}@example.invalid"
        with pytest.raises(PlaneAPIError):
            workspace_members.remove(WorkspaceMemberRemove(email=bogus_email))
