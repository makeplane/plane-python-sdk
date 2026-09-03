"""Release label catalog (api_v2). Workspace-level, distinct from the
per-release association (`ReleaseLabels.add`/`.remove`)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.releases import CreateReleaseLabel, ReleaseLabel, UpdateReleaseLabel
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class ReleaseLabels(V2Resource[ReleaseLabel, CreateReleaseLabel, UpdateReleaseLabel]):
    path = "/workspaces/{slug}/releases/labels/"
    bridge_path = "/workspaces/{slug}/releases/{release_id}/labels/"
    model = ReleaseLabel
    operations = {
        "list": "release_labels_list",
        "retrieve": "release_labels_retrieve",
        "create": "release_labels_create",
        "update": "release_labels_partial_update",
        "delete": "release_labels_destroy",
        "bridge": "releases_labels",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[ReleaseLabel]:
        """One page of the workspace's release-label catalog."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[ReleaseLabel]:
        """Every release label in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, label_id: str, *, fields: Sequence[str] | None = None) -> ReleaseLabel:
        return self._retrieve(pk=label_id, params={"fields": fields})

    def find_by_name(self, name: str) -> ReleaseLabel:
        """The one release label with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateReleaseLabel) -> ReleaseLabel:
        """Define a new label in the workspace catalog. To put an existing
        label on a release, use `.add` instead."""
        return self._create(data)

    def update(self, label_id: str, data: UpdateReleaseLabel) -> ReleaseLabel:
        return self._update(data, pk=label_id)

    def delete(self, label_id: str) -> None:
        return self._delete(pk=label_id)

    # -- Per-release membership bridge --------------------------------------

    def add(self, release_id: str, label_ids: Sequence[str]) -> builtins.list[str]:
        """Attach 1..100 existing catalog labels to this release; returns the
        ids actually added (already-attached ones are omitted)."""
        return self._bridge(key="add", ids=label_ids, release_id=release_id)

    def remove(self, release_id: str, label_ids: Sequence[str]) -> builtins.list[str]:
        """Detach 1..100 labels from this release; returns the ids actually
        removed."""
        return self._bridge(key="remove", ids=label_ids, release_id=release_id)
