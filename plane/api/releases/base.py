from typing import Any

from ...models.releases import CreateRelease, Release, UpdateRelease
from ..base_resource import BaseResource
from .item_labels import ReleaseItemLabels
from .labels import ReleaseLabels
from .tags import ReleaseTags


class Releases(BaseResource):
    """API client for managing workspace-level releases."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.tags = ReleaseTags(config)
        self.labels = ReleaseLabels(config)
        self.item_labels = ReleaseItemLabels(config)

    def list(self, workspace_slug: str) -> list[Release]:
        """List all releases in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/releases/")
        return [Release.model_validate(item) for item in response]

    def create(self, workspace_slug: str, data: CreateRelease) -> Release:
        """Create a new release in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Release data
        """
        response = self._post(
            f"{workspace_slug}/releases/",
            data.model_dump(exclude_none=True),
        )
        return Release.model_validate(response)

    def update(self, workspace_slug: str, release_id: str, data: UpdateRelease) -> Release:
        """Update a release in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            data: Updated release data
        """
        response = self._patch(
            f"{workspace_slug}/releases/{release_id}/",
            data.model_dump(exclude_none=True),
        )
        return Release.model_validate(response)
