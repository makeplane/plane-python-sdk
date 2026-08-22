"""Project states (api_v2)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from ...models.v2.common import BulkWriteResponse
from ...models.v2.states import CreateState, State, UpdateState
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


class States(V2Resource[State, CreateState, UpdateState]):
    path = "/workspaces/{slug}/projects/{project_id}/states/"
    model = State
    operations = {
        "list": "states_list",
        "retrieve": "states_retrieve",
        "create": "states_create",
        "update": "states_partial_update",
        "upsert": "states_upsert",
        "delete": "states_destroy",
        "bulk_create": "states_bulk_create",
        "bulk_update": "states_bulk_update",
        "bulk_delete": "states_bulk_delete",
    }

    def list(self, *, fields: Sequence[str] | None = None, **filters: Any) -> Page[State]:
        """One page of states in this project."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[State]:
        """Every state, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, state_id: str, *, fields: Sequence[str] | None = None) -> State:
        return self._retrieve(pk=state_id, params={"fields": fields})

    def find_by_name(self, name: str) -> State:
        """The one state with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateState) -> State:
        return self._create(data)

    def update(self, state_id: str, data: UpdateState) -> State:
        return self._update(data, pk=state_id)

    def delete(self, state_id: str) -> None:
        return self._delete(pk=state_id)

    def upsert(self, data: CreateState) -> State:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data)

    def bulk_create(
        self, items: builtins.list[CreateState], *, all_or_none: bool = False
    ) -> BulkWriteResponse:
        return self._bulk_create(items, all_or_none=all_or_none)

    def bulk_update(
        self, items: builtins.list[Mapping[str, Any]], *, all_or_none: bool = False
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`."""
        return self._bulk_update(items, all_or_none=all_or_none)

    def bulk_delete(
        self, ids: builtins.list[str], *, all_or_none: bool = False
    ) -> BulkWriteResponse:
        return self._bulk_delete(ids, all_or_none=all_or_none)
