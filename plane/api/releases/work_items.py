from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ...models.releases import (
    AddReleaseWorkItems,
    PaginatedReleaseWorkItemResponse,
    ReleaseWorkItem,
)
from ..base_resource import BaseResource


class ReleaseWorkItems(BaseResource):
    """API client for the work items linked to a release."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, release_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedReleaseWorkItemResponse:
        """List the work items linked to a release (paginated).

        Returns one page (20 by default). Pass `per_page`/`cursor` in params and
        follow `next_cursor` to page through the rest.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            params: Optional query parameters, e.g. `per_page`, `cursor`
        """
        response = self._get(f"{workspace_slug}/releases/{release_id}/work-items/", params=params)
        return PaginatedReleaseWorkItemResponse.model_validate(response)

    def add(self, workspace_slug: str, release_id: str, data: AddReleaseWorkItems) -> None:
        """Link work items to a release. Already-linked work items are skipped.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            data: Work item IDs to link
        """
        self._post(
            f"{workspace_slug}/releases/{release_id}/work-items/",
            data.model_dump(exclude_none=True),
        )

    def remove(self, workspace_slug: str, release_id: str, work_item_ids: list[str]) -> None:
        """Unlink work items from a release.

        Args:
            workspace_slug: The workspace slug identifier
            release_id: UUID of the release
            work_item_ids: UUIDs of the work items to unlink
        """
        return self._delete(
            f"{workspace_slug}/releases/{release_id}/work-items/",
            data={"work_item_ids": work_item_ids},
        )
