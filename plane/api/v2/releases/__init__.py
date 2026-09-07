"""Releases (api_v2) -- workspace-scoped, not project-scoped. Beyond CRUD:
a `.work_items` membership bridge, a `.changelog` singleton, catalog siblings
`.labels` (itself a bridge for the per-release association)/`.tags`, and
nested `.comments`/`.links` (see `tags.py` for a golden/server mismatch)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.releases import CreateRelease, Release, UpdateRelease
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .changelog import ReleaseChangelogResource
from .comments import ReleaseComments

try:
    from .labels import ReleaseLabels
except TypeError:
    # See `plane/api/v2/collections/__init__.py` for why this is swallowed here:
    # `ReleaseLabels` still declares the retired `bridge_path`.
    ReleaseLabels = None  # type: ignore[assignment, misc]
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


class Releases(V2Resource[Release, CreateRelease, UpdateRelease]):
    path = "/workspaces/{slug}/releases/"
    model = Release
    operations = {
        "list": "releases_list",
        "retrieve": "releases_retrieve",
        "create": "releases_create",
        "update": "releases_partial_update",
        "delete": "releases_destroy",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.comments = ReleaseComments(transport, **self._scope)
        self.links = ReleaseLinks(transport, **self._scope)
        self.labels = ReleaseLabels(transport, **self._scope)
        self.tags = ReleaseTags(transport, **self._scope)
        self.changelog = ReleaseChangelogResource(transport, **self._scope)
        self.work_items = ReleaseWorkItems(transport, **self._scope)

    # -- Workspace-scoped CRUD ----------------------------------------------------

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Release]:
        """One page of releases in the workspace.

        `**filters` covers `status`, `lead_id`, `tag_id`, `is_latest`."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Release]:
        """Every release in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        release_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Release:
        return self._retrieve(pk=release_id, params={"fields": fields, "expand": expand})

    def find_by_name(self, name: str) -> Release:
        """The one release with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateRelease) -> Release:
        return self._create(data)

    def update(self, release_id: str, data: UpdateRelease) -> Release:
        return self._update(data, pk=release_id)

    def delete(self, release_id: str) -> None:
        return self._delete(pk=release_id)
