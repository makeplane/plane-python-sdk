"""Release label catalog (api_v2). Workspace-level, distinct from the
per-release association (`ReleaseLabels.add`/`.remove`) -- the catalog CRUD
hits `path` (`.../releases/labels/`) while `add`/`remove` bridge to the
`extra_paths` override (`.../releases/{release}/labels/`) via `url_for`."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.releases import CreateReleaseLabel, ReleaseLabel, UpdateReleaseLabel
from .._generated.constants import (
    ReleaseLabelsCreateField,
    ReleaseLabelsListField,
    ReleaseLabelsListFilters,
    ReleaseLabelsListOrderBy,
    ReleaseLabelsPartialUpdateField,
    ReleaseLabelsRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource


class ReleaseLabels(V2Resource[ReleaseLabel, CreateReleaseLabel, UpdateReleaseLabel]):
    path = "/workspaces/{slug}/releases/labels/"
    extra_paths = {
        "add": "/workspaces/{slug}/releases/{release_id}/labels/",
        "remove": "/workspaces/{slug}/releases/{release_id}/labels/",
    }
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
        slug: str,
        *,
        fields: Sequence[ReleaseLabelsListField] | None = None,
        order_by: ReleaseLabelsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[ReleaseLabelsListFilters],
    ) -> Page[ReleaseLabel]:
        """One page of the workspace's release-label catalog."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[ReleaseLabelsListField] | None = None,
        order_by: ReleaseLabelsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[ReleaseLabelsListFilters],
    ) -> Iterator[ReleaseLabel]:
        """Every release label in the workspace, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )

    def retrieve(
        self,
        slug: str,
        label: str,
        *,
        fields: Sequence[ReleaseLabelsRetrieveField] | None = None,
    ) -> ReleaseLabel:
        return self._retrieve(pk=label, params={"fields": fields}, slug=slug)

    def find_by_name(self, slug: str, name: str) -> ReleaseLabel:
        """The one release label with this name; raises if none or several match."""
        return self._find_one(filters={"name": name}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateReleaseLabel,
        *,
        fields: Sequence[ReleaseLabelsCreateField] | None = None,
    ) -> ReleaseLabel:
        """Define a new label in the workspace catalog. To put an existing
        label on a release, use `.add` instead."""
        return self._create(data, params={"fields": fields}, slug=slug)

    def update(
        self,
        slug: str,
        label: str,
        data: UpdateReleaseLabel,
        *,
        fields: Sequence[ReleaseLabelsPartialUpdateField] | None = None,
    ) -> ReleaseLabel:
        return self._update(data, pk=label, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, label: str) -> None:
        return self._delete(pk=label, slug=slug)

    # -- Per-release membership bridge (alternate path via `extra_paths`) ---

    def add(self, slug: str, release: str, label_ids: Sequence[str]) -> builtins.list[str]:
        """Attach 1..100 existing catalog labels to this release; returns the
        ids actually added (already-attached ones are omitted). POSTs to the
        `extra_paths["add"]` override, not `path`."""
        return self._bridge(key="add", ids=label_ids, slug=slug, release_id=release)

    def remove(self, slug: str, release: str, label_ids: Sequence[str]) -> builtins.list[str]:
        """Detach 1..100 labels from this release; returns the ids actually
        removed. POSTs to the `extra_paths["remove"]` override, not `path`."""
        return self._bridge(key="remove", ids=label_ids, slug=slug, release_id=release)
