from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ...models.releases import (
    CreateReleaseTag,
    PaginatedReleaseTagResponse,
    ReleaseTag,
    UpdateReleaseTag,
)
from ..base_resource import BaseResource


class ReleaseTags(BaseResource):
    """API client for managing release tags (version markers)."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedReleaseTagResponse:
        """List release tags in the workspace (paginated).

        Returns one page (20 by default). Pass `per_page`/`cursor` in params and
        follow `next_cursor` to page through the rest.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters, e.g. `per_page`, `cursor`
        """
        response = self._get(f"{workspace_slug}/releases/tags/", params=params)
        return PaginatedReleaseTagResponse.model_validate(response)

    def retrieve(self, workspace_slug: str, tag_id: str) -> ReleaseTag:
        """Retrieve a release tag by ID.

        Args:
            workspace_slug: The workspace slug identifier
            tag_id: UUID of the release tag
        """
        response = self._get(f"{workspace_slug}/releases/tags/{tag_id}/")
        return ReleaseTag.model_validate(response)

    def create(self, workspace_slug: str, data: CreateReleaseTag) -> ReleaseTag:
        """Create a new release tag in the workspace.

        `data.version` is required and must be unique in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Release tag data
        """
        response = self._post(
            f"{workspace_slug}/releases/tags/",
            data.model_dump(exclude_none=True),
        )
        return ReleaseTag.model_validate(response)

    def update(self, workspace_slug: str, tag_id: str, data: UpdateReleaseTag) -> ReleaseTag:
        """Update a release tag by ID.

        Args:
            workspace_slug: The workspace slug identifier
            tag_id: UUID of the release tag
            data: Updated tag data
        """
        response = self._patch(
            f"{workspace_slug}/releases/tags/{tag_id}/",
            data.model_dump(exclude_none=True),
        )
        return ReleaseTag.model_validate(response)

    def delete(self, workspace_slug: str, tag_id: str) -> None:
        """Delete a release tag by ID.

        Args:
            workspace_slug: The workspace slug identifier
            tag_id: UUID of the release tag
        """
        return self._delete(f"{workspace_slug}/releases/tags/{tag_id}/")
