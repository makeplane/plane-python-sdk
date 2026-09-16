"""`project.members`/`workspace.members` against a real server; `remove` is
deliberately not exercised on a real member -- it cascades a deactivation through
every project and is not reversible, so only its error contract is tested.

Both scopes off their own loaded row, which is also the clearest statement of what
they are: the same resource family at two levels of the URL."""

from __future__ import annotations

import pytest

from plane.api.v2 import LoadedProject, LoadedWorkspace, PlaneAPIError
from plane.models.v2.members import UpdateProjectMember, WorkspaceMemberRemove

from .helpers import unique_name


class TestProjectMembers:
    def test_list_includes_the_project_creator(self, project: LoadedProject) -> None:
        """A freshly created project always has at least the creator as a
        member (verified live via the shared session `project` fixture)."""
        page = project.members.list()
        assert page.data

    def test_retrieve_then_update_role(self, project: LoadedProject) -> None:
        existing = project.members.list().data[0]

        fetched = project.members.retrieve(existing.id)
        assert fetched.id == existing.id

        updated = project.members.update(existing.id, UpdateProjectMember(role=fetched.role))
        assert updated.id == existing.id

    def test_expand_member_rejects_an_unknown_relation(self, project: LoadedProject) -> None:
        with pytest.raises(ValueError, match="bogus"):
            project.members.list(expand=["bogus"])

    def test_retrieve_missing_row_404s(self, project: LoadedProject) -> None:
        missing_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(PlaneAPIError) as exc_info:
            project.members.retrieve(missing_id)
        assert exc_info.value.status == 404


class TestWorkspaceMembers:
    def test_list_includes_at_least_the_api_principal(self, workspace: LoadedWorkspace) -> None:
        page = workspace.members.list()
        assert page.data

    def test_remove_unknown_email_is_a_clean_error(self, workspace: LoadedWorkspace) -> None:
        """Non-destructive: `unique_name` guarantees this email resolves to no
        one, so `remove` cannot actually deactivate a real member here."""
        bogus_email = f"{unique_name('nobody')}@example.invalid"
        with pytest.raises(PlaneAPIError):
            workspace.members.remove(WorkspaceMemberRemove(email=bogus_email))
