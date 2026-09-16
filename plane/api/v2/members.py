"""Members (api_v2) -- project rosters (full CRUD) and the workspace roster
(list + remove-by-email). Workspace removal is `POST …/members/remove/` keyed
on `email` (v1 parity), not a detail DELETE keyed on a row id."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.members import (
    CreateProjectMember,
    Member,
    UpdateProjectMember,
    WorkspaceMemberRemove,
)
from ._generated.constants import (
    ProjectMembersCreateField,
    ProjectMembersListField,
    ProjectMembersListFilters,
    ProjectMembersListOrderBy,
    ProjectMembersPartialUpdateField,
    ProjectMembersRetrieveField,
    WorkspaceMembersListField,
    WorkspaceMembersListFilters,
    WorkspaceMembersListOrderBy,
)
from ._kernel.pagination import Page, PaginateStyle
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
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectMembersListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ProjectMembersListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[ProjectMembersListFilters],
    ) -> Page[Member]:
        """One page of this project's roster."""
        return self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
            project_id=project,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectMembersListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ProjectMembersListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[ProjectMembersListFilters],
    ) -> Iterator[Member]:
        """Every row on this project's roster, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
            project_id=project,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        member: str,
        *,
        fields: Sequence[ProjectMembersRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Member:
        """Fetch by the membership row's own id (not the member's user id)."""
        return self._retrieve(
            pk=member,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )

    def create(
        self,
        slug: str,
        project: str,
        data: CreateProjectMember,
        *,
        fields: Sequence[ProjectMembersCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Member:
        """Add a member to the project."""
        return self._create(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )

    def update(
        self,
        slug: str,
        project: str,
        member: str,
        data: UpdateProjectMember,
        *,
        fields: Sequence[ProjectMembersPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Member:
        """Change a member's role."""
        return self._update(
            data,
            pk=member,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )

    def delete(self, slug: str, project: str, member: str) -> None:
        return self._delete(pk=member, slug=slug, project_id=project)


class WorkspaceMembers(V2Resource[Member, CreateProjectMember, UpdateProjectMember]):
    """The workspace roster. List-only plus `remove` -- see the module docstring."""

    path = "/workspaces/{slug}/members/"
    extra_paths = {"remove": "/workspaces/{slug}/members/remove/"}
    model = Member
    operations = {
        "list": "workspace_members_list",
        "remove": "workspace_members_remove",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceMembersListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkspaceMembersListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkspaceMembersListFilters],
    ) -> Page[Member]:
        """One page of the workspace roster."""
        return self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceMembersListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkspaceMembersListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkspaceMembersListFilters],
    ) -> Iterator[Member]:
        """Every row on the workspace roster, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )

    def remove(self, slug: str, data: WorkspaceMemberRemove) -> None:
        """Remove a member from the workspace by email (v1 parity) --
        soft-deactivates and cascades out of every project. Not addressed by a
        row id; POSTs to the `extra_paths["remove"]` override, not `path`.

        Unlike `V2Resource._bridge`'s `add`/`remove` pairs (which always return
        `list[str]`), this has no `add` counterpart -- it is a standalone
        removal keyed on email, not one side of a membership bridge -- so it
        keeps returning `None`, matching the golden's 204 with no body."""
        self._custom_request("remove", data=data, slug=slug)
        return None
