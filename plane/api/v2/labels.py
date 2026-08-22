"""Project labels (api_v2)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from ...models.v2.common import BulkWriteResponse
from ...models.v2.labels import CreateLabel, Label, UpdateLabel
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


class Labels(V2Resource[Label, CreateLabel, UpdateLabel]):
    path = "/workspaces/{slug}/projects/{project_id}/labels/"
    model = Label
    operations = {
        "list": "labels_list",
        "retrieve": "labels_retrieve",
        "create": "labels_create",
        "update": "labels_partial_update",
        "upsert": "labels_upsert",
        "delete": "labels_destroy",
        "bulk_create": "labels_bulk_create",
        "bulk_update": "labels_bulk_update",
        "bulk_delete": "labels_bulk_delete",
    }

    def list(self, *, fields: Sequence[str] | None = None, **filters: Any) -> Page[Label]:
        """One page of labels in this project."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[Label]:
        """Every label, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, label_id: str, *, fields: Sequence[str] | None = None) -> Label:
        return self._retrieve(pk=label_id, params={"fields": fields})

    def find_by_name(self, name: str) -> Label:
        """The one label with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateLabel) -> Label:
        return self._create(data)

    def update(self, label_id: str, data: UpdateLabel) -> Label:
        return self._update(data, pk=label_id)

    def delete(self, label_id: str) -> None:
        return self._delete(pk=label_id)

    def upsert(self, data: CreateLabel) -> Label:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data)

    def bulk_create(
        self, items: builtins.list[CreateLabel], *, all_or_none: bool = False
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
