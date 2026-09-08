"""Sticky notes (api_v2) -- a workspace member's personal sticky notes. Flat
CRUD; rows are implicitly owner-scoped server-side (a member only sees their own)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.stickies import CreateSticky, Sticky, UpdateSticky
from ._generated.constants import (
    StickiesCreateField,
    StickiesListField,
    StickiesListFilters,
    StickiesListOrderBy,
    StickiesPartialUpdateField,
    StickiesRetrieveField,
)
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
        slug: str,
        *,
        fields: Sequence[StickiesListField] | None = None,
        order_by: StickiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[StickiesListFilters],
    ) -> Page[Sticky]:
        """One page of stickies. `**filters` covers the golden's query filters
        directly, e.g. `color="#fff"`, `owner_id=...`, `search="todo"`."""
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
        fields: Sequence[StickiesListField] | None = None,
        order_by: StickiesListOrderBy | None = None,
        **filters: Unpack[StickiesListFilters],
    ) -> Iterator[Sticky]:
        """Every sticky, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
        )

    def retrieve(
        self,
        slug: str,
        sticky: str,
        *,
        fields: Sequence[StickiesRetrieveField] | None = None,
    ) -> Sticky:
        return self._retrieve(pk=sticky, params={"fields": fields}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateSticky,
        *,
        fields: Sequence[StickiesCreateField] | None = None,
    ) -> Sticky:
        return self._create(data, params={"fields": fields}, slug=slug)

    def update(
        self,
        slug: str,
        sticky: str,
        data: UpdateSticky,
        *,
        fields: Sequence[StickiesPartialUpdateField] | None = None,
    ) -> Sticky:
        return self._update(data, pk=sticky, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, sticky: str) -> None:
        return self._delete(pk=sticky, slug=slug)
