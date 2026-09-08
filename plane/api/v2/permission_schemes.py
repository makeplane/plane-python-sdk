"""Workspace permission schemes (api_v2). Read-only -- system + custom schemes,
no create/update/delete on this endpoint."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.permission_schemes import PermissionScheme
from ._generated.constants import (
    PermissionSchemesListField,
    PermissionSchemesListFilters,
    PermissionSchemesListOrderBy,
    PermissionSchemesRetrieveField,
)
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


# No write/patch DTO exists for permission schemes -- the type parameters are
# filled with the read model itself as an unused placeholder (see the work_items
# build's documented kernel gap).
class PermissionSchemes(V2Resource[PermissionScheme, PermissionScheme, PermissionScheme]):
    path = "/workspaces/{slug}/permission-schemes/"
    model = PermissionScheme
    operations = {
        "list": "permission_schemes_list",
        "retrieve": "permission_schemes_retrieve",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[PermissionSchemesListField] | None = None,
        order_by: PermissionSchemesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[PermissionSchemesListFilters],
    ) -> Page[PermissionScheme]:
        """One page of permission schemes (system + custom) in the workspace."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
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
        **filters: Unpack[PermissionSchemesListFilters],
    ) -> Iterator[PermissionScheme]:
        """Every permission scheme, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
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
