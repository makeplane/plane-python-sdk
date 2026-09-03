"""Initiative labels (api_v2) -- a workspace-level taxonomy, *not* nested under
an initiative id despite living at `initiatives.labels`. `create` defines a
label in the workspace catalog; `add`/`remove` (the bridge) put an existing
one on -- or take it off -- one initiative."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.initiatives import CreateInitiativeLabel, InitiativeLabel, UpdateInitiativeLabel
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class InitiativeLabels(V2Resource[InitiativeLabel, CreateInitiativeLabel, UpdateInitiativeLabel]):
    path = "/workspaces/{slug}/initiatives/labels/"
    bridge_path = "/workspaces/{slug}/initiatives/{initiative_id}/labels/"
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
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[InitiativeLabel]:
        """One page of initiative labels in a workspace."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[InitiativeLabel]:
        """Every initiative label in a workspace, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, pk: str, *, fields: Sequence[str] | None = None) -> InitiativeLabel:
        return self._retrieve(pk=pk, params={"fields": fields})

    def find_by_name(self, name: str) -> InitiativeLabel:
        """The one initiative label with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateInitiativeLabel) -> InitiativeLabel:
        return self._create(data)

    def update(self, pk: str, data: UpdateInitiativeLabel) -> InitiativeLabel:
        return self._update(data, pk=pk)

    def delete(self, pk: str) -> None:
        return self._delete(pk=pk)

    def add(self, initiative_id: str, label_ids: Sequence[str]) -> builtins.list[str]:
        """Put 1..100 existing labels on this initiative; returns the ids
        actually added (already-present ones are omitted)."""
        return self._bridge(key="add", ids=label_ids, initiative_id=initiative_id)

    def remove(self, initiative_id: str, label_ids: Sequence[str]) -> builtins.list[str]:
        """Take 1..100 labels off this initiative; returns the ids actually
        removed."""
        return self._bridge(key="remove", ids=label_ids, initiative_id=initiative_id)
