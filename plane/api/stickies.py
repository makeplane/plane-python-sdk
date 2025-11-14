from collections.abc import Mapping
from typing import Any

from ..models.stickies import CreateSticky, PaginatedStickyResponse, Sticky, UpdateSticky
from .base_resource import BaseResource


class Stickies(BaseResource):
    """API client for managing stickies in workspaces."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, data: CreateSticky) -> Sticky:
        """Create a new sticky in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Sticky data

        Returns:
            The created sticky
        """
        response = self._post(
            f"{workspace_slug}/stickies",
            data.model_dump(exclude_none=True),
        )
        return Sticky.model_validate(response)

    def retrieve(self, workspace_slug: str, sticky_id: str) -> Sticky:
        """Retrieve a sticky by ID.

        Args:
            workspace_slug: The workspace slug identifier
            sticky_id: UUID of the sticky

        Returns:
            The requested sticky
        """
        response = self._get(f"{workspace_slug}/stickies/{sticky_id}")
        return Sticky.model_validate(response)

    def update(self, workspace_slug: str, sticky_id: str, data: UpdateSticky) -> Sticky:
        """Update a sticky by ID.

        Args:
            workspace_slug: The workspace slug identifier
            sticky_id: UUID of the sticky
            data: Updated sticky data

        Returns:
            The updated sticky
        """
        response = self._patch(
            f"{workspace_slug}/stickies/{sticky_id}",
            data.model_dump(exclude_none=True),
        )
        return Sticky.model_validate(response)

    def delete(self, workspace_slug: str, sticky_id: str) -> None:
        """Delete a sticky by ID.

        Args:
            workspace_slug: The workspace slug identifier
            sticky_id: UUID of the sticky
        """
        return self._delete(f"{workspace_slug}/stickies/{sticky_id}")

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedStickyResponse:
        """List stickies in the workspace with optional filtering.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters (e.g., query for search, per_page, cursor)

        Returns:
            Paginated list of stickies
        """
        response = self._get(f"{workspace_slug}/stickies", params=params)
        return PaginatedStickyResponse.model_validate(response)

