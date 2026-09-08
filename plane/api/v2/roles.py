"""Roles (api_v2) -- system + custom roles for the workspace. Read-only: list +
retrieve only, no write surface (full role CRUD lives only in the app UI)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from typing_extensions import Unpack

from ...models.v2.roles import Role
from ._generated.constants import (
    RolesListField,
    RolesListFilters,
    RolesListOrderBy,
    RolesRetrieveField,
)
from ._kernel.errors import MultipleMatchesFound, NoMatchFound
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


class Roles(V2Resource[Role, Role, Role]):
    path = "/workspaces/{slug}/roles/"
    model = Role
    operations = {
        "list": "roles_list",
        "retrieve": "roles_retrieve",
    }

    def list(  # type: ignore[misc]
        self,
        slug: str,
        *,
        fields: Sequence[RolesListField] | None = None,
        order_by: RolesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[RolesListFilters],
    ) -> Page[Role]:
        """One page of roles. `**filters` covers the golden's query filters
        directly, e.g. `namespace="workspace"`, `is_system=True`, `search="admin"`.
        The golden's own `?slug=` filter (the role's slug) is not reachable here --
        `slug` already names the workspace, the leading path id -- use
        `find_by_slug` instead."""
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

    def iterate(  # type: ignore[misc]
        self,
        slug: str,
        *,
        fields: Sequence[RolesListField] | None = None,
        order_by: RolesListOrderBy | None = None,
        **filters: Unpack[RolesListFilters],
    ) -> Iterator[Role]:
        """Every role, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
        )

    def retrieve(
        self, slug: str, role_id: str, *, fields: Sequence[RolesRetrieveField] | None = None
    ) -> Role:
        return self._retrieve(pk=role_id, params={"fields": fields}, slug=slug)

    def find_by_name(self, slug: str, name: str, *, namespace: str | None = None) -> Role:
        """The one role with this name; raises if none or several match. Filters
        client-side (no `?name=`); names are unique only *within* a namespace, so
        pass `namespace` or expect `MultipleMatchesFound`."""
        filters: dict[str, Any] = {"namespace": namespace} if namespace else {}
        matches = [row for row in self.iterate(slug, **filters) if row.name == name]
        if not matches:
            raise NoMatchFound(f"No Roles matched name={name!r}.")
        if len(matches) > 1:
            raise MultipleMatchesFound(
                f"Multiple rows matched name={name!r}; "
                f"use the id instead, or list to see every match."
            )
        return matches[0]

    def find_by_slug(self, slug: str, role_slug: str, *, namespace: str | None = None) -> Role:
        """The one role with this slug in the workspace; raises if none or several
        match. Slugs are unique only within a namespace, so pass `namespace` or
        expect `MultipleMatchesFound`. `slug` is the workspace; `role_slug` is the role."""
        filters: dict[str, Any] = {"slug": role_slug}
        if namespace is not None:
            filters["namespace"] = namespace
        return self._find_one(filters=filters, slug=slug)
