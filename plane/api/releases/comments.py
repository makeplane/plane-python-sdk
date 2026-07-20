from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ...models.releases import (
    CreateReleaseComment,
    PaginatedReleaseCommentResponse,
    ReleaseComment,
    UpdateReleaseComment,
)
from ..base_resource import BaseResource


class ReleaseComments(BaseResource):
    """API client for the comments on a release."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, release_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedReleaseCommentResponse:
        """List the comments on a release (paginated).

        Returns one page (20 by default). Pass `per_page`/`cursor` in params and
        follow `next_cursor` to page through the rest.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            params: Optional query parameters, e.g. `per_page`, `cursor`
        """
        response = self._get(f"{workspace_slug}/releases/{release_id}/comments/", params=params)
        return PaginatedReleaseCommentResponse.model_validate(response)

    def retrieve(self, workspace_slug: str, release_id: str, comment_id: str) -> ReleaseComment:
        """Retrieve a release comment by ID.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            comment_id: UUID of the comment
        """
        response = self._get(f"{workspace_slug}/releases/{release_id}/comments/{comment_id}/")
        return ReleaseComment.model_validate(response)

    def create(
        self, workspace_slug: str, release_id: str, data: CreateReleaseComment
    ) -> ReleaseComment:
        """Create a comment on a release.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            data: Comment data (body as `comment_html`)
        """
        response = self._post(
            f"{workspace_slug}/releases/{release_id}/comments/",
            data.model_dump(exclude_none=True),
        )
        return ReleaseComment.model_validate(response)

    def update(
        self, workspace_slug: str, release_id: str, comment_id: str, data: UpdateReleaseComment
    ) -> ReleaseComment:
        """Update a release comment by ID.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            comment_id: UUID of the comment
            data: Updated comment data
        """
        response = self._patch(
            f"{workspace_slug}/releases/{release_id}/comments/{comment_id}/",
            data.model_dump(exclude_none=True),
        )
        return ReleaseComment.model_validate(response)

    def delete(self, workspace_slug: str, release_id: str, comment_id: str) -> None:
        """Delete a release comment by ID.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            comment_id: UUID of the comment
        """
        return self._delete(f"{workspace_slug}/releases/{release_id}/comments/{comment_id}/")
