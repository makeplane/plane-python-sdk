"""Releases (api_v2) -- workspace-scoped, not project-scoped. Beyond CRUD:
a `.work_items` membership bridge, a `.changelog` singleton, catalog siblings
`.labels` (itself a bridge for the per-release association)/`.tags`, and
nested `.comments`/`.links` (see `tags.py` for a golden/server mismatch).

A fetched row (`retrieve`/`create`, and every row in a `list` page) comes back as a
`LoadedRelease`: it carries the row's data and can reach `.comments.list(...)` and
friends without the caller repeating `slug`/`release`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.releases import CreateRelease, Release, UpdateRelease
from .._generated.constants import (
    ReleasesCreateField,
    ReleasesListField,
    ReleasesListFilters,
    ReleasesListOrderBy,
    ReleasesPartialUpdateField,
    ReleasesRetrieveField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.release import LoadedRelease
from .changelog import ReleaseChangelogResource
from .comments import ReleaseComments
from .labels import ReleaseLabels
from .links import ReleaseLinks
from .tags import ReleaseTags
from .work_items import ReleaseWorkItems

__all__ = [
    "ReleaseChangelogResource",
    "ReleaseComments",
    "ReleaseLabels",
    "ReleaseLinks",
    "ReleaseTags",
    "ReleaseWorkItems",
    "Releases",
]


class Releases(
    V2Resource[Release, CreateRelease, UpdateRelease], LoadsNavigableRows[LoadedRelease]
):
    path = "/workspaces/{slug}/releases/"
    model = Release
    loaded_model = LoadedRelease
    loaded_names = ("slug", "release")
    operations = {
        "list": "releases_list",
        "retrieve": "releases_retrieve",
        "create": "releases_create",
        "update": "releases_partial_update",
        "delete": "releases_destroy",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.labels = ReleaseLabels(transport)
        self.tags = ReleaseTags(transport)
        self.comments = ReleaseComments(transport)
        self.links = ReleaseLinks(transport)
        self.changelog = ReleaseChangelogResource(transport)
        self.work_items = ReleaseWorkItems(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[ReleasesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ReleasesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[ReleasesListFilters],
    ) -> Page[LoadedRelease]:
        """One page of releases in the workspace."""
        page = self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
        )
        return self._load_page(page, slug, fields=fields)

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[ReleasesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ReleasesListOrderBy | None = None,
        **filters: Unpack[ReleasesListFilters],
    ) -> Iterator[LoadedRelease]:
        """Every release in the workspace, following pages automatically."""
        rows = self._iter(
            params={"fields": fields, "expand": expand, "order_by": order_by, **filters},
            slug=slug,
        )
        return (self._load(row, slug, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        release: str,
        *,
        fields: Sequence[ReleasesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedRelease:
        row = self._retrieve(pk=release, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def find_by_name(self, slug: str, name: str) -> LoadedRelease:
        """The one release with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug)
        return self._load(row, slug)

    def create(
        self,
        slug: str,
        data: CreateRelease,
        *,
        fields: Sequence[ReleasesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedRelease:
        row = self._create(data, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def update(
        self,
        slug: str,
        release: str,
        data: UpdateRelease,
        *,
        fields: Sequence[ReleasesPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedRelease:
        row = self._update(data, pk=release, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def delete(self, slug: str, release: str) -> None:
        return self._delete(pk=release, slug=slug)
