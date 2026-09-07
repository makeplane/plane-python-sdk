"""Releases (api_v2) -- workspace-scoped, not project-scoped. Beyond CRUD:
a `.work_items` membership bridge, a `.changelog` singleton, catalog siblings
`.labels` (itself a bridge for the per-release association)/`.tags`, and
nested `.comments`/`.links` (see `tags.py` for a golden/server mismatch).

**Only `.labels` is migrated to the flat shape.** `Releases` is wired onto
`Workspaces` for its sake, so `ws.releases.labels` works; the class's own CRUD and
its other children still omit the leading `slug`, and each says so when used --
see `_kernel/pending.py`. The unmigrated bodies are kept as the starting point for
that work."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.releases import CreateRelease, Release, UpdateRelease
from .._kernel.pagination import Page
from .._kernel.pending import PendingMigration, pending_flat_migration
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
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

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.labels = ReleaseLabels(transport)
        # Wired as placeholders, not as the real classes: each still takes only its
        # own id and would build `/workspaces/{slug}/...` with no slug to fill it.
        self.comments = PendingMigration("ReleaseComments", reached_as="releases.comments")
        self.links = PendingMigration("ReleaseLinks", reached_as="releases.links")
        self.tags = PendingMigration("ReleaseTags", reached_as="releases.tags")
        self.changelog = PendingMigration(
            "ReleaseChangelogResource", reached_as="releases.changelog"
        )
        self.work_items = PendingMigration("ReleaseWorkItems", reached_as="releases.work_items")

    # -- Workspace-scoped CRUD (pending flat migration: no leading `slug` yet) ----

    @pending_flat_migration
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

    @pending_flat_migration
    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Release]:
        """Every release in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    @pending_flat_migration
    def retrieve(
        self,
        release_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Release:
        return self._retrieve(pk=release_id, params={"fields": fields, "expand": expand})

    @pending_flat_migration
    def find_by_name(self, name: str) -> Release:
        """The one release with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    @pending_flat_migration
    def create(self, data: CreateRelease) -> Release:
        return self._create(data)

    @pending_flat_migration
    def update(self, release_id: str, data: UpdateRelease) -> Release:
        return self._update(data, pk=release_id)

    @pending_flat_migration
    def delete(self, release_id: str) -> None:
        return self._delete(pk=release_id)
