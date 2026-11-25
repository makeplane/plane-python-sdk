"""Teamspaces (api_v2) -- a named grouping of members + projects. Flat CRUD
(no bulk, no upsert). `expand` accepts `lead`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.permissions import EffectivePermissions
from ...models.v2.teamspaces import CreateTeamspace, Teamspace, UpdateTeamspace
from ._generated.constants import (
    TeamspacesCreateField,
    TeamspacesListField,
    TeamspacesListFilters,
    TeamspacesListOrderBy,
    TeamspacesPartialUpdateField,
    TeamspacesRetrieveField,
)
from ._kernel.pagination import Page, PaginateStyle
from ._kernel.resource import V2Resource


class Teamspaces(V2Resource[Teamspace, CreateTeamspace, UpdateTeamspace]):
    path = "/workspaces/{slug}/teamspaces/"
    extra_paths = {
        "my_permissions": "/workspaces/{slug}/teamspaces/{team_space_id}/permissions/me/"
    }
    model = Teamspace
    operations = {
        "list": "teamspaces_list",
        "retrieve": "teamspaces_retrieve",
        "create": "teamspaces_create",
        "update": "teamspaces_partial_update",
        "delete": "teamspaces_destroy",
        "my_permissions": "workspaces_teamspaces_permissions_me_retrieve",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[TeamspacesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: TeamspacesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[TeamspacesListFilters],
    ) -> Page[Teamspace]:
        """One page of teamspaces. `**filters` covers the golden's query filters
        directly, e.g. `lead_id=...`, `name="Platform"`, `search="plat"`."""
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
        fields: Sequence[TeamspacesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: TeamspacesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[TeamspacesListFilters],
    ) -> Iterator[Teamspace]:
        """Every teamspace, following pages automatically."""
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

    def retrieve(
        self,
        slug: str,
        teamspace: str,
        *,
        fields: Sequence[TeamspacesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Teamspace:
        return self._retrieve(
            pk=teamspace,
            params={"fields": fields, "expand": expand},
            slug=slug,
        )

    def find_by_name(self, slug: str, name: str) -> Teamspace:
        """The one teamspace with this name; raises if none or several match."""
        return self._find_one(filters={"name": name}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateTeamspace,
        *,
        fields: Sequence[TeamspacesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Teamspace:
        return self._create(data, params={"fields": fields, "expand": expand}, slug=slug)

    def update(
        self,
        slug: str,
        teamspace: str,
        data: UpdateTeamspace,
        *,
        fields: Sequence[TeamspacesPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Teamspace:
        return self._update(
            data, pk=teamspace, params={"fields": fields, "expand": expand}, slug=slug
        )

    def delete(self, slug: str, teamspace: str) -> None:
        return self._delete(pk=teamspace, slug=slug)

    def my_permissions(self, slug: str, teamspace: str) -> EffectivePermissions:
        """The caller's effective permissions in this teamspace. A method here rather
        than a `permissions` child, which would need a navigable `LoadedTeamspace`."""
        return self._custom_action(
            "my_permissions",
            model=EffectivePermissions,
            method="GET",
            slug=slug,
            team_space_id=teamspace,
        )
