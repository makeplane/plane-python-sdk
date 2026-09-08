"""Release changelog (api_v2) -- one singleton per release, nested under a release id.
Named `ReleaseChangelogResource` to avoid clashing with the `ReleaseChangelog` model.

No pk of its own: a GET auto-creates it empty (there is no create/delete), so it goes
through the kernel's `_retrieve_singleton`/`_update_singleton` pair, not `_retrieve`/
`_update`, which both require a `pk` to append. The golden declares no `?fields=` or
`?expand=` for either operation, so neither is exposed here."""

from __future__ import annotations

from ....models.v2.releases import ReleaseChangelog, UpdateReleaseChangelog
from .._kernel.resource import V2Resource

__all__ = ["ReleaseChangelogResource"]


class ReleaseChangelogResource(
    V2Resource[ReleaseChangelog, ReleaseChangelog, UpdateReleaseChangelog]
):
    """`releases.changelog` -- one per release, created implicitly (no create/delete)."""

    path = "/workspaces/{slug}/releases/{release_id}/changelog/"
    model = ReleaseChangelog
    operations = {
        "retrieve": "releases_changelog_retrieve",
        "update": "releases_changelog_partial_update",
    }

    def retrieve(self, slug: str, release: str) -> ReleaseChangelog:
        """The release's changelog. One per release, created implicitly with
        it -- there is no create/delete."""
        return self._retrieve_singleton(slug=slug, release_id=release)

    def update(self, slug: str, release: str, data: UpdateReleaseChangelog) -> ReleaseChangelog:
        return self._update_singleton(data, slug=slug, release_id=release)
