from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ...models.releases import (
    CreateReleaseLink,
    PaginatedReleaseLinkResponse,
    ReleaseLink,
    UpdateReleaseLink,
)
from ..base_resource import BaseResource


class ReleaseLinks(BaseResource):
    """API client for the links on a release."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, release_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedReleaseLinkResponse:
        """List the links on a release (paginated).

        Returns one page (20 by default). Pass `per_page`/`cursor` in params and
        follow `next_cursor` to page through the rest.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            params: Optional query parameters, e.g. `per_page`, `cursor`
        """
        response = self._get(f"{workspace_slug}/releases/{release_id}/links/", params=params)
        return PaginatedReleaseLinkResponse.model_validate(response)

    def retrieve(self, workspace_slug: str, release_id: str, link_id: str) -> ReleaseLink:
        """Retrieve a release link by ID.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            link_id: UUID of the link
        """
        response = self._get(f"{workspace_slug}/releases/{release_id}/links/{link_id}/")
        return ReleaseLink.model_validate(response)

    def create(self, workspace_slug: str, release_id: str, data: CreateReleaseLink) -> ReleaseLink:
        """Create a link on a release.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            data: Link data (`url` required)
        """
        response = self._post(
            f"{workspace_slug}/releases/{release_id}/links/",
            data.model_dump(exclude_none=True),
        )
        return ReleaseLink.model_validate(response)

    def update(
        self, workspace_slug: str, release_id: str, link_id: str, data: UpdateReleaseLink
    ) -> ReleaseLink:
        """Update a release link by ID.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            link_id: UUID of the link
            data: Updated link data
        """
        response = self._patch(
            f"{workspace_slug}/releases/{release_id}/links/{link_id}/",
            data.model_dump(exclude_none=True),
        )
        return ReleaseLink.model_validate(response)

    def delete(self, workspace_slug: str, release_id: str, link_id: str) -> None:
        """Delete a release link by ID.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            link_id: UUID of the link
        """
        return self._delete(f"{workspace_slug}/releases/{release_id}/links/{link_id}/")
