"""Roles (api_v2) -- system + custom roles for the workspace. Read-only: list +
retrieve only, no write surface (full role CRUD lives only in the app UI)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.roles import Role
from ._generated.constants import RolesListField, RolesListOrderBy, RolesRetrieveField
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

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[RolesListField] | None = None,
        order_by: RolesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        namespace: str | None = None,
        is_system: bool | None = None,
        search: str | None = None,
        role_slug: str | None = None,
    ) -> Page[Role]:
        """One page of roles. `RolesListFilters` has only four keys -- `namespace`,
        `is_system`, `search`, and `slug` -- declared here explicitly (rather than
        `**filters: Unpack[RolesListFilters]`) because that last one, the golden's
        own `?slug=` role filter, collides by name with the leading path id `slug`
        (the workspace). `role_slug` carries it through to the `slug` query key."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "namespace": namespace,
                "is_system": is_system,
                "search": search,
                "slug": role_slug,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[RolesListField] | None = None,
        order_by: RolesListOrderBy | None = None,
        namespace: str | None = None,
        is_system: bool | None = None,
        search: str | None = None,
        role_slug: str | None = None,
    ) -> Iterator[Role]:
        """Every role, following pages automatically. See `list` for why the
        filters are named explicitly rather than `**filters`."""
        return self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "namespace": namespace,
                "is_system": is_system,
                "search": search,
                "slug": role_slug,
            },
            slug=slug,
        )

    def retrieve(
        self, slug: str, role_id: str, *, fields: Sequence[RolesRetrieveField] | None = None
    ) -> Role:
        return self._retrieve(pk=role_id, params={"fields": fields}, slug=slug)

    def find_by_name(self, slug: str, name: str, *, namespace: str | None = None) -> Role:
        """The one role with this name; raises if none or several match. Filters
        client-side: the golden's `roles_list` has no `?name=` query param (its
        filters are `is_system`, `namespace`, `search`, `slug` -- no `name`), so
        there is no server-side way to ask for this. Names are unique only *within*
        a namespace, so pass `namespace` or expect `MultipleMatchesFound`."""
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
        match. Server-side via the golden's `?slug=` filter on `roles_list` -- one
        request, not a client-side scan. Slugs are unique only within a namespace,
        so pass `namespace` or expect `MultipleMatchesFound`. `slug` is the
        workspace; `role_slug` is the role."""
        filters: dict[str, Any] = {"slug": role_slug}
        if namespace is not None:
            filters["namespace"] = namespace
        return self._find_one(filters=filters, slug=slug)
