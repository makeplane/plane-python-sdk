"""Workspace permission schemes (api_v2). Read-only -- system + custom schemes,
no create/update/delete on this endpoint."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.permission_schemes import PermissionScheme
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
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[PermissionScheme]:
        """One page of permission schemes (system + custom) in the workspace."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[PermissionScheme]:
        """Every permission scheme, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self,
        scheme_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> PermissionScheme:
        return self._retrieve(pk=scheme_id, params={"fields": fields})
