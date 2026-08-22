"""Members (api_v2) -- project rosters (full CRUD) and the workspace roster
(list + remove-by-email). Workspace removal is `POST …/members/remove/` keyed
on `email` (v1 parity), not a detail DELETE keyed on a row id."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.members import (
    CreateProjectMember,
    Member,
    UpdateProjectMember,
    WorkspaceMemberRemove,
)
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource

__all__ = ["ProjectMembers", "WorkspaceMembers"]


class ProjectMembers(V2Resource[Member, CreateProjectMember, UpdateProjectMember]):
    path = "/workspaces/{slug}/projects/{project_id}/members/"
    model = Member
    operations = {
        "list": "project_members_list",
        "retrieve": "project_members_retrieve",
        "create": "project_members_create",
        "update": "project_members_partial_update",
        "delete": "project_members_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Member]:
        """One page of this project's roster."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Member]:
        """Every row on this project's roster, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        member_row_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Member:
        """Fetch by the membership row's own id (not the member's user id)."""
        return self._retrieve(pk=member_row_id, params={"fields": fields, "expand": expand})

    def create(self, data: CreateProjectMember) -> Member:
        """Add a member to the project."""
        return self._create(data)

    def update(self, member_row_id: str, data: UpdateProjectMember) -> Member:
        """Change a member's role."""
        return self._update(data, pk=member_row_id)

    def delete(self, member_row_id: str) -> None:
        return self._delete(pk=member_row_id)


class WorkspaceMembers(V2Resource[Member, CreateProjectMember, UpdateProjectMember]):
    """The workspace roster. List-only plus `remove` -- see the module docstring."""

    path = "/workspaces/{slug}/members/"
    model = Member
    operations = {
        "list": "workspace_members_list",
        "remove": "workspace_members_remove",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Member]:
        """One page of the workspace roster."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Member]:
        """Every row on the workspace roster, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def remove(self, data: WorkspaceMemberRemove) -> None:
        """Remove a member from the workspace by email (v1 parity) --
        soft-deactivates and cascades out of every project. Not addressed by a
        row id; the response is 204 with no body."""
        url = f"{self._collection_url()}remove/"
        self.transport.request("POST", url, json=data.model_dump(mode="json", exclude_none=True))
        return None
