"""Workspace invitations (api_v2). No PATCH; only `list`/`retrieve`/`create`/
`delete` plus `bulk`. Golden documents `bulk`'s 201 as one `WorkspaceInvite`, but
the view returns the whole created list -- this SDK follows the live behavior."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.invitations import (
    BulkCreateWorkspaceInvites,
    CreateWorkspaceInvite,
    WorkspaceInvite,
)
from ._generated.constants import (
    MembersBulkField,
    MembersCreateField,
    MembersListField,
    MembersListFilters,
    MembersListOrderBy,
    MembersRetrieveField,
)
from ._kernel.pagination import Page, PaginateStyle
from ._kernel.resource import V2Resource


class Invitations(V2Resource[WorkspaceInvite, CreateWorkspaceInvite, CreateWorkspaceInvite]):
    path = "/workspaces/{slug}/invitations/"
    extra_paths = {"bulk": "/workspaces/{slug}/invitations/bulk/"}
    model = WorkspaceInvite
    operations = {
        "list": "members_list",
        "retrieve": "members_retrieve",
        "create": "members_create",
        "bulk": "members_bulk",
        "delete": "members_destroy",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[MembersListField] | None = None,
        order_by: MembersListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[MembersListFilters],
    ) -> Page[WorkspaceInvite]:
        """One page of pending/accepted invitations. `**filters` covers the
        golden's query filters directly, e.g. `accepted=False`, `email="a@b.com"`."""
        return self._list(
            params={
                "fields": fields,
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
        fields: Sequence[MembersListField] | None = None,
        order_by: MembersListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[MembersListFilters],
    ) -> Iterator[WorkspaceInvite]:
        """Every invitation, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )

    def retrieve(
        self,
        slug: str,
        invitation: str,
        *,
        fields: Sequence[MembersRetrieveField] | None = None,
    ) -> WorkspaceInvite:
        return self._retrieve(pk=invitation, params={"fields": fields}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateWorkspaceInvite,
        *,
        fields: Sequence[MembersCreateField] | None = None,
    ) -> WorkspaceInvite:
        return self._create(data, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, invitation: str) -> None:
        return self._delete(pk=invitation, slug=slug)

    def bulk(
        self,
        slug: str,
        data: BulkCreateWorkspaceInvites,
        *,
        fields: Sequence[MembersBulkField] | None = None,
    ) -> builtins.list[WorkspaceInvite]:
        """Create up to 100 invitations in one call. Emails already invited are
        silently skipped server-side (not re-sent, not errored). POSTs to the
        `extra_paths["bulk"]` override, not `path`."""
        return self._custom_action_list(
            "bulk", model=WorkspaceInvite, data=data, params={"fields": fields}, slug=slug
        )
