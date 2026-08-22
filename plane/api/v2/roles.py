"""Roles (api_v2) -- system + custom roles for the workspace. Read-only: list +
retrieve only, no write surface (full role CRUD lives only in the app UI)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.roles import Role
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
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Role]:
        """One page of roles. `**filters` covers the golden's query filters
        directly, e.g. `namespace="workspace"`, `is_system=True`, `search="admin"`."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Role]:
        """Every role, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, role_id: str, *, fields: Sequence[str] | None = None) -> Role:
        return self._retrieve(pk=role_id, params={"fields": fields})

    def find_by_name(self, name: str, *, namespace: str | None = None) -> Role:
        """The one role with this name; raises if none or several match. Filters
        client-side (no `?name=`); names are unique only *within* a namespace, so
        pass `namespace` or expect `MultipleMatchesFound`."""
        filters: dict[str, Any] = {"namespace": namespace} if namespace else {}
        matches = [row for row in self.iterate(**filters) if row.name == name]
        if not matches:
            raise NoMatchFound(f"No Roles matched name={name!r}.")
        if len(matches) > 1:
            raise MultipleMatchesFound(
                f"Multiple rows matched name={name!r}; "
                f"use the id instead, or list to see every match."
            )
        return matches[0]
