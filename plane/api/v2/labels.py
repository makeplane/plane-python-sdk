"""Project labels (api_v2)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence

from typing_extensions import Unpack

from ...models.v2.common import BulkWriteResponse
from ...models.v2.labels import CreateLabel, Label, UpdateLabel
from ._generated.constants import (
    LabelsListField,
    LabelsListFilters,
    LabelsListOrderBy,
    LabelsRetrieveField,
)
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
        "delete": "labels_destroy",
        "upsert": "labels_upsert",
        "bulk_create": "labels_bulk_create",
        "bulk_update": "labels_bulk_update",
        "bulk_delete": "labels_bulk_delete",
    }

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[LabelsListField] | None = None,
        order_by: LabelsListOrderBy | None = None,
        **filters: Unpack[LabelsListFilters],
    ) -> Page[Label]:
        """One page of labels in this project."""
        return self._list(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[LabelsListField] | None = None,
        order_by: LabelsListOrderBy | None = None,
        **filters: Unpack[LabelsListFilters],
    ) -> Iterator[Label]:
        """Every label, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        label_id: str,
        *,
        fields: Sequence[LabelsRetrieveField] | None = None,
    ) -> Label:
        return self._retrieve(pk=label_id, params={"fields": fields}, slug=slug, project_id=project)

    def find_by_name(self, slug: str, project: str, name: str) -> Label:
        """The one label with this name; raises if none or several match."""
        return self._find_one(filters={"name": name}, slug=slug, project_id=project)

    def create(self, slug: str, project: str, data: CreateLabel) -> Label:
        return self._create(data, slug=slug, project_id=project)

    def update(self, slug: str, project: str, label_id: str, data: UpdateLabel) -> Label:
        return self._update(data, pk=label_id, slug=slug, project_id=project)

    def delete(self, slug: str, project: str, label_id: str) -> None:
        return self._delete(pk=label_id, slug=slug, project_id=project)

    def upsert(self, slug: str, project: str, data: CreateLabel) -> Label:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data, slug=slug, project_id=project)

    def bulk_create(
        self,
        slug: str,
        project: str,
        items: builtins.list[CreateLabel],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_create(items, all_or_none=all_or_none, slug=slug, project_id=project)

    def bulk_update(
        self,
        slug: str,
        project: str,
        items: builtins.list[Mapping[str, object]],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`."""
        return self._bulk_update(items, all_or_none=all_or_none, slug=slug, project_id=project)

    def bulk_delete(
        self,
        slug: str,
        project: str,
        ids: builtins.list[str],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_delete(ids, all_or_none=all_or_none, slug=slug, project_id=project)
