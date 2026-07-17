from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ...models.releases import (
    AddReleaseItemLabel,
    PaginatedReleaseLabelResponse,
    ReleaseLabel,
    RemoveReleaseItemLabel,
)
from ..base_resource import BaseResource


class ReleaseItemLabels(BaseResource):
    """API client for managing the labels attached to a specific release."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, release_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedReleaseLabelResponse:
        """List labels attached to a release (paginated).

        Returns one page (20 by default). Pass `per_page`/`cursor` in params and
        follow `next_cursor` to page through the rest.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            params: Optional query parameters, e.g. `per_page`, `cursor`
        """
        response = self._get(f"{workspace_slug}/releases/{release_id}/labels/", params=params)
        return PaginatedReleaseLabelResponse.model_validate(response)

    def create(
        self, workspace_slug: str, release_id: str, data: AddReleaseItemLabel
    ) -> list[ReleaseLabel]:
        """Attach labels to a release.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            data: Label IDs to attach
        """
        response = self._post(
            f"{workspace_slug}/releases/{release_id}/labels/",
            data.model_dump(exclude_none=True),
        )
        return [ReleaseLabel.model_validate(item) for item in response]

    def delete(self, workspace_slug: str, release_id: str, data: RemoveReleaseItemLabel) -> None:
        """Detach labels from a release (the labels themselves are not deleted).

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            data: Label IDs to detach
        """
        return self._delete(
            f"{workspace_slug}/releases/{release_id}/labels/",
            data.model_dump(exclude_none=True),
        )
