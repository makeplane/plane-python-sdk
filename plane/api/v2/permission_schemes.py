"""Workspace permission schemes (api_v2) -- system + custom. Only custom schemes
take update/delete; writes need the plan's custom-roles feature (402 otherwise).
The server adds each key's prerequisites and folded keys on save, so a scheme
reads back with more `permissions` than were sent. Deleting a scheme a role still
uses is a 409; `impact` says who a change reaches."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.permission_schemes import (
    CreatePermissionScheme,
    PermissionScheme,
    PermissionSchemeImpact,
    UpdatePermissionScheme,
)
from ._generated.constants import (
    PermissionSchemesCreateField,
    PermissionSchemesListField,
    PermissionSchemesListFilters,
    PermissionSchemesListOrderBy,
    PermissionSchemesPartialUpdateField,
    PermissionSchemesRetrieveField,
)
from ._kernel.pagination import Page, PaginateStyle
from ._kernel.resource import V2Resource


class PermissionSchemes(
    V2Resource[PermissionScheme, CreatePermissionScheme, UpdatePermissionScheme]
):
    path = "/workspaces/{slug}/permission-schemes/"
    model = PermissionScheme
    operations = {
        "list": "permission_schemes_list",
        "retrieve": "permission_schemes_retrieve",
        "create": "permission_schemes_create",
        "update": "permission_schemes_partial_update",
        "delete": "permission_schemes_destroy",
        "impact": "permission_schemes_impact",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[PermissionSchemesListField] | None = None,
        order_by: PermissionSchemesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[PermissionSchemesListFilters],
    ) -> Page[PermissionScheme]:
        """One page of permission schemes (system + custom) in the workspace."""
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
        fields: Sequence[PermissionSchemesListField] | None = None,
        order_by: PermissionSchemesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[PermissionSchemesListFilters],
    ) -> Iterator[PermissionScheme]:
        """Every permission scheme, following pages automatically."""
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
        scheme: str,
        *,
        fields: Sequence[PermissionSchemesRetrieveField] | None = None,
    ) -> PermissionScheme:
        return self._retrieve(pk=scheme, params={"fields": fields}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreatePermissionScheme,
        *,
        fields: Sequence[PermissionSchemesCreateField] | None = None,
    ) -> PermissionScheme:
        return self._create(data, params={"fields": fields}, slug=slug)

    def update(
        self,
        slug: str,
        scheme: str,
        data: UpdatePermissionScheme,
        *,
        fields: Sequence[PermissionSchemesPartialUpdateField] | None = None,
    ) -> PermissionScheme:
        """Edit a custom scheme. Every role composing it changes with it -- check
        `impact` first."""
        return self._update(data, pk=scheme, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, scheme: str) -> None:
        """Delete a custom scheme; 409 while a role still uses it."""
        return self._delete(pk=scheme, slug=slug)

    def impact(self, slug: str, scheme: str) -> PermissionSchemeImpact:
        """How many roles compose the scheme, and how many people and projects they reach."""
        return self._custom_action(
            "impact", model=PermissionSchemeImpact, method="GET", pk=scheme, slug=slug
        )
