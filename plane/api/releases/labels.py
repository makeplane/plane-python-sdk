from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ...models.releases import (
    CreateReleaseLabel,
    PaginatedReleaseLabelResponse,
    ReleaseLabel,
    UpdateReleaseLabel,
)
from ..base_resource import BaseResource


class ReleaseLabels(BaseResource):
    """API client for managing workspace-level release labels."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedReleaseLabelResponse:
        """List release labels in the workspace (paginated).

        Returns one page (20 by default). Pass `per_page`/`cursor` in params and
        follow `next_cursor` to page through the rest.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters, e.g. `per_page`, `cursor`
        """
        response = self._get(f"{workspace_slug}/releases/labels/", params=params)
        return PaginatedReleaseLabelResponse.model_validate(response)

    def retrieve(self, workspace_slug: str, label_id: str) -> ReleaseLabel:
        """Retrieve a release label by ID.

        Args:
            workspace_slug: The workspace slug identifier
            label_id: UUID of the release label
        """
        response = self._get(f"{workspace_slug}/releases/labels/{label_id}/")
        return ReleaseLabel.model_validate(response)

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

    def update(self, workspace_slug: str, label_id: str, data: UpdateReleaseLabel) -> ReleaseLabel:
        """Update a release label by ID.

        Args:
            workspace_slug: The workspace slug identifier
            label_id: UUID of the release label
            data: Updated label data
        """
        response = self._patch(
            f"{workspace_slug}/releases/labels/{label_id}/",
            data.model_dump(exclude_none=True),
        )
        return ReleaseLabel.model_validate(response)

    def delete(self, workspace_slug: str, label_id: str) -> None:
        """Delete a release label by ID.

        This deletes the label itself from the workspace. To only detach a label
        from a release, use `client.releases.item_labels.delete`.

        Args:
            workspace_slug: The workspace slug identifier
            label_id: UUID of the release label
        """
        return self._delete(f"{workspace_slug}/releases/labels/{label_id}/")
