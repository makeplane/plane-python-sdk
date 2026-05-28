from typing import Any

from ...models.releases import CreateReleaseLabel, ReleaseLabel
from ..base_resource import BaseResource


class ReleaseLabels(BaseResource):
    """API client for managing release labels."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str) -> list[ReleaseLabel]:
        """List all release labels in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/releases/labels/")
        return [ReleaseLabel.model_validate(item) for item in response]

    def create(self, workspace_slug: str, data: CreateReleaseLabel) -> ReleaseLabel:
        """Create a new release label in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Release label data
        """
        response = self._post(
            f"{workspace_slug}/releases/labels/",
            data.model_dump(exclude_none=True),
        )
        return ReleaseLabel.model_validate(response)
