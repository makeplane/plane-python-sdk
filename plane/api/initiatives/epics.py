from collections.abc import Iterable, Mapping
from typing import Any

from ...models.epics import Epic, PaginatedEpicResponse
from ..base_resource import BaseResource


class InitiativeEpics(BaseResource):
    """API client for managing epics associated with initiatives."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, initiative_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedEpicResponse:
        """List epics associated with an initiative.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
            params: Optional query parameters (e.g., per_page, cursor)

        Returns:
            Paginated list of epics
        """
        response = self._get(f"{workspace_slug}/initiatives/{initiative_id}/epics", params=params)
        return PaginatedEpicResponse.model_validate(response)

    def add(
        self, workspace_slug: str, initiative_id: str, epic_ids: Iterable[str]
    ) -> Iterable[Epic]:
        """Add epics to an initiative.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
            epic_ids: List of epic UUIDs to add

        Returns:
            List of added epics
        """
        response = self._post(
            f"{workspace_slug}/initiatives/{initiative_id}/epics",
            {"epic_ids": epic_ids},
        )
        return [Epic.model_validate(epic) for epic in response]

    def remove(self, workspace_slug: str, initiative_id: str, epic_ids: Iterable[str]) -> None:
        """Remove epics from an initiative.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
            epic_ids: List of epic UUIDs to remove
        """
        return self._delete(
            f"{workspace_slug}/initiatives/{initiative_id}/epics",
            {"epic_ids": epic_ids},
        )
