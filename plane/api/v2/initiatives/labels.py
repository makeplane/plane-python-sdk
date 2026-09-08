"""Initiative label catalog (api_v2). Workspace-level, distinct from the
per-initiative association (`InitiativeLabels.add`/`.remove`) -- the catalog CRUD
hits `path` (`.../initiatives/labels/`) while `add`/`remove` bridge to the
`extra_paths` override (`.../initiatives/{initiative_id}/labels/`) via `url_for`.
Same shape as `releases/labels.py` -- copied from it."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.initiatives import CreateInitiativeLabel, InitiativeLabel, UpdateInitiativeLabel
from .._generated.constants import (
    InitiativeLabelsCreateField,
    InitiativeLabelsListField,
    InitiativeLabelsListFilters,
    InitiativeLabelsListOrderBy,
    InitiativeLabelsPartialUpdateField,
    InitiativeLabelsRetrieveField,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class InitiativeLabels(V2Resource[InitiativeLabel, CreateInitiativeLabel, UpdateInitiativeLabel]):
    path = "/workspaces/{slug}/initiatives/labels/"
    extra_paths = {
        "add": "/workspaces/{slug}/initiatives/{initiative_id}/labels/",
        "remove": "/workspaces/{slug}/initiatives/{initiative_id}/labels/",
    }
    model = InitiativeLabel
    operations = {
        "list": "initiative_labels_list",
        "retrieve": "initiative_labels_retrieve",
        "create": "initiative_labels_create",
        "update": "initiative_labels_partial_update",
        "delete": "initiative_labels_destroy",
        "bridge": "initiatives_labels",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[InitiativeLabelsListField] | None = None,
        order_by: InitiativeLabelsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[InitiativeLabelsListFilters],
    ) -> Page[InitiativeLabel]:
        """One page of the workspace's initiative-label catalog."""
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
        fields: Sequence[InitiativeLabelsListField] | None = None,
        order_by: InitiativeLabelsListOrderBy | None = None,
        **filters: Unpack[InitiativeLabelsListFilters],
    ) -> Iterator[InitiativeLabel]:
        """Every initiative label in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, "order_by": order_by, **filters}, slug=slug)

    def retrieve(
        self,
        slug: str,
        label: str,
        *,
        fields: Sequence[InitiativeLabelsRetrieveField] | None = None,
    ) -> InitiativeLabel:
        return self._retrieve(pk=label, params={"fields": fields}, slug=slug)

    def find_by_name(self, slug: str, name: str) -> InitiativeLabel:
        """The one initiative label with this name; raises if none or several match."""
        return self._find_one(filters={"name": name}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateInitiativeLabel,
        *,
        fields: Sequence[InitiativeLabelsCreateField] | None = None,
    ) -> InitiativeLabel:
        """Define a new label in the workspace catalog. To put an existing
        label on an initiative, use `.add` instead."""
        return self._create(data, params={"fields": fields}, slug=slug)

    def update(
        self,
        slug: str,
        label: str,
        data: UpdateInitiativeLabel,
        *,
        fields: Sequence[InitiativeLabelsPartialUpdateField] | None = None,
    ) -> InitiativeLabel:
        return self._update(data, pk=label, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, label: str) -> None:
        return self._delete(pk=label, slug=slug)

    # -- Per-initiative membership bridge (alternate path via `extra_paths`) ---

    def add(self, slug: str, initiative: str, label_ids: Sequence[str]) -> builtins.list[str]:
        """Put 1..100 existing catalog labels on this initiative; returns the
        ids actually added (already-present ones are omitted). POSTs to the
        `extra_paths["add"]` override, not `path`."""
        return self._bridge(key="add", ids=label_ids, slug=slug, initiative_id=initiative)

    def remove(self, slug: str, initiative: str, label_ids: Sequence[str]) -> builtins.list[str]:
        """Take 1..100 labels off this initiative; returns the ids actually
        removed. POSTs to the `extra_paths["remove"]` override, not `path`."""
        return self._bridge(key="remove", ids=label_ids, slug=slug, initiative_id=initiative)
