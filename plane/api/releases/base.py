from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ...models.releases import (
    CreateRelease,
    PaginatedReleaseResponse,
    Release,
    UpdateRelease,
)
from ..base_resource import BaseResource
from .comments import ReleaseComments
from .item_labels import ReleaseItemLabels
from .labels import ReleaseLabels
from .links import ReleaseLinks
from .tags import ReleaseTags
from .work_items import ReleaseWorkItems


class Releases(BaseResource):
    """API client for managing workspace-level releases."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.tags = ReleaseTags(config)
        self.labels = ReleaseLabels(config)
        self.item_labels = ReleaseItemLabels(config)
        self.work_items = ReleaseWorkItems(config)
        self.comments = ReleaseComments(config)
        self.links = ReleaseLinks(config)

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedReleaseResponse:
        """List releases in the workspace (paginated).

        Returns one page (20 by default). Pass `per_page`/`cursor` in params and
        follow `next_cursor` to page through the rest.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters, e.g. `per_page`, `cursor`
        """
        response = self._get(f"{workspace_slug}/releases/", params=params)
        return PaginatedReleaseResponse.model_validate(response)

    def retrieve(self, workspace_slug: str, release_id: str) -> Release:
        """Retrieve a release by ID.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
        """
        response = self._get(f"{workspace_slug}/releases/{release_id}/")
        return Release.model_validate(response)

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

    def delete(self, workspace_slug: str, release_id: str) -> None:
        """Delete a release by ID.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
        """
        return self._delete(f"{workspace_slug}/releases/{release_id}/")
