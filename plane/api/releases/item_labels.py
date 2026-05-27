from __future__ import annotations

from typing import Any

from ...models.releases import AddReleaseItemLabel, ReleaseLabel
from ..base_resource import BaseResource


class ReleaseItemLabels(BaseResource):
    """API client for managing labels on a specific release."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, release_id: str) -> list[ReleaseLabel]:
        """List labels assigned to a release.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
        """
        response = self._get(f"{workspace_slug}/releases/{release_id}/labels/")
        return [ReleaseLabel.model_validate(item) for item in response]

    def add(
        self, workspace_slug: str, release_id: str, data: AddReleaseItemLabel
    ) -> list[ReleaseLabel]:
        """Add labels to a release.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            data: Label IDs to add
        """
        response = self._post(
            f"{workspace_slug}/releases/{release_id}/labels/",
            data.model_dump(exclude_none=True),
        )
        return [ReleaseLabel.model_validate(item) for item in response]

    def remove(self, workspace_slug: str, release_id: str, label_id: str) -> None:
        """Remove a label from a release.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            label_id: UUID of the label to remove
        """
        return self._delete(f"{workspace_slug}/releases/{release_id}/labels/{label_id}/")
