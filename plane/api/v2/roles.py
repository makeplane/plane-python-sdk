"""Roles (api_v2) -- system + custom roles for the workspace. Every role reads;
only custom roles take create/update/delete (a system role accepts `sort_order`
alone). Writes need the plan's custom-roles feature (402 otherwise) and an owner
or admin. `expand` accepts `permission_schemes`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.roles import CreateRole, Role, UpdateRole
from ._generated.constants import (
    RolesCreateField,
    RolesListField,
    RolesListOrderBy,
    RolesPartialUpdateField,
    RolesRetrieveField,
)
from ._kernel.errors import MultipleMatchesFound, NoMatchFound
from ._kernel.pagination import Page, PaginateStyle
from ._kernel.resource import V2Resource


class Roles(V2Resource[Role, CreateRole, UpdateRole]):
    path = "/workspaces/{slug}/roles/"
    model = Role
    operations = {
        "list": "roles_list",
        "retrieve": "roles_retrieve",
        "create": "roles_create",
        "update": "roles_partial_update",
        "delete": "roles_destroy",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[RolesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: RolesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
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
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
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
        expand: Sequence[str] | None = None,
        order_by: RolesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
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
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                "namespace": namespace,
                "is_system": is_system,
                "search": search,
                "slug": role_slug,
            },
            slug=slug,
        )

    def retrieve(
        self,
        slug: str,
        role: str,
        *,
        fields: Sequence[RolesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Role:
        return self._retrieve(pk=role, params={"fields": fields, "expand": expand}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateRole,
        *,
        fields: Sequence[RolesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Role:
        """Create a custom role from `permission_scheme_ids`, or copy another role's
        schemes with `based_on_slug`."""
        return self._create(data, params={"fields": fields, "expand": expand}, slug=slug)

    def update(
        self,
        slug: str,
        role: str,
        data: UpdateRole,
        *,
        fields: Sequence[RolesPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Role:
        """Edit a custom role. Disabling one that has members (`status="inactive"`)
        needs `reassign_to`: another active role of the same namespace."""
        return self._update(data, pk=role, params={"fields": fields, "expand": expand}, slug=slug)

    def delete(self, slug: str, role: str, *, reassign_to: str | None = None) -> None:
        """Delete a custom role. `reassign_to` (a role id) is required when the role
        has members: they move to it first."""
        return self._delete(pk=role, params={"reassign_to": reassign_to}, slug=slug)

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
