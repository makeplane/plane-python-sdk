"""Release changelog (api_v2) -- one singleton per release, nested under a release id.
Named `ReleaseChangelogResource` to avoid clashing with the `ReleaseChangelog` model."""

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

    def retrieve(self, release_id: str) -> ReleaseChangelog:
        """The release's changelog. One per release, created implicitly with
        it -- there is no create/delete."""
        payload = self.transport.request("GET", self._collection_url(release_id=release_id))
        return self.model.model_validate(payload)

    def update(self, release_id: str, data: UpdateReleaseChangelog) -> ReleaseChangelog:
        payload = self.transport.request(
            "PATCH",
            self._collection_url(release_id=release_id),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return self.model.model_validate(payload)
