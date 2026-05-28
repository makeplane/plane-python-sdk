from typing import Any

from ...models.releases import CreateReleaseTag, ReleaseTag
from ..base_resource import BaseResource


class ReleaseTags(BaseResource):
    """API client for managing release tags."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str) -> list[ReleaseTag]:
        """List all release tags in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/releases/tags/")
        return [ReleaseTag.model_validate(item) for item in response]

    def create(self, workspace_slug: str, data: CreateReleaseTag) -> ReleaseTag:
        """Create a new release tag in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Release tag data
        """
        response = self._post(
            f"{workspace_slug}/releases/tags/",
            data.model_dump(exclude_none=True),
        )
        return ReleaseTag.model_validate(response)
