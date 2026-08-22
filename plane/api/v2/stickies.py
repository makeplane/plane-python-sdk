"""Sticky notes (api_v2) -- a workspace member's personal sticky notes. Flat
CRUD; rows are implicitly owner-scoped server-side (a member only sees their own)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.stickies import CreateSticky, Sticky, UpdateSticky
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


class Stickies(V2Resource[Sticky, CreateSticky, UpdateSticky]):
    path = "/workspaces/{slug}/stickies/"
    model = Sticky
    operations = {
        "list": "stickies_list",
        "retrieve": "stickies_retrieve",
        "create": "stickies_create",
        "update": "stickies_partial_update",
        "delete": "stickies_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Sticky]:
        """One page of stickies. `**filters` covers the golden's query filters
        directly, e.g. `color="#fff"`, `owner_id=...`, `search="todo"`."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Sticky]:
        """Every sticky, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self,
        sticky_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> Sticky:
        return self._retrieve(pk=sticky_id, params={"fields": fields})

    def create(self, data: CreateSticky) -> Sticky:
        return self._create(data)

    def update(self, sticky_id: str, data: UpdateSticky) -> Sticky:
        return self._update(data, pk=sticky_id)

    def delete(self, sticky_id: str) -> None:
        return self._delete(pk=sticky_id)
