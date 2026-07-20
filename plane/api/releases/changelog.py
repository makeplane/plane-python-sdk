from __future__ import annotations

from typing import Any

from ...models.releases import ReleaseChangelog, UpdateReleaseChangelog
from ..base_resource import BaseResource


class ReleaseChangelogs(BaseResource):
    """API client for a release's changelog (a singleton per release)."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def retrieve(self, workspace_slug: str, release_id: str) -> ReleaseChangelog:
        """Retrieve a release's changelog.

        The changelog is created empty on first access, so this always returns one.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
        """
        response = self._get(f"{workspace_slug}/releases/{release_id}/changelog/")
        return ReleaseChangelog.model_validate(response)

    def update(
        self, workspace_slug: str, release_id: str, data: UpdateReleaseChangelog
    ) -> ReleaseChangelog:
        """Update a release's changelog body.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            data: Updated changelog body (as `description_html` / `description_json`)
        """
        response = self._patch(
            f"{workspace_slug}/releases/{release_id}/changelog/",
            data.model_dump(exclude_none=True),
        )
        return ReleaseChangelog.model_validate(response)
