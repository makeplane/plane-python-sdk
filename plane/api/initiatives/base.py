from collections.abc import Mapping
from typing import Any

from ...models.initiatives import (
    CreateInitiative,
    Initiative,
    PaginatedInitiativeResponse,
    UpdateInitiative,
)
from ..base_resource import BaseResource
from .epics import InitiativeEpics
from .labels import InitiativeLabels
from .projects import InitiativeProjects


class Initiatives(BaseResource):
    """API client for managing initiatives in workspaces."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.labels = InitiativeLabels(config)
        self.projects = InitiativeProjects(config)
        self.epics = InitiativeEpics(config)

    def create(self, workspace_slug: str, data: CreateInitiative) -> Initiative:
        """Create a new initiative in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Initiative data

        Returns:
            The created initiative
        """
        response = self._post(
            f"{workspace_slug}/initiatives",
            data.model_dump(exclude_none=True),
        )
        return Initiative.model_validate(response)

    def retrieve(self, workspace_slug: str, initiative_id: str) -> Initiative:
        """Retrieve an initiative by ID.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative

        Returns:
            The requested initiative
        """
        response = self._get(f"{workspace_slug}/initiatives/{initiative_id}")
        return Initiative.model_validate(response)

    def update(
        self, workspace_slug: str, initiative_id: str, data: UpdateInitiative
    ) -> Initiative:
        """Update an initiative by ID.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
            data: Updated initiative data

        Returns:
            The updated initiative
        """
        response = self._patch(
            f"{workspace_slug}/initiatives/{initiative_id}",
            data.model_dump(exclude_none=True),
        )
        return Initiative.model_validate(response)

    def delete(self, workspace_slug: str, initiative_id: str) -> None:
        """Delete an initiative by ID.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
        """
        return self._delete(f"{workspace_slug}/initiatives/{initiative_id}")

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedInitiativeResponse:
        """List initiatives in the workspace with optional filtering.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters (e.g., per_page, cursor)

        Returns:
            Paginated list of initiatives
        """
        response = self._get(f"{workspace_slug}/initiatives", params=params)
        return PaginatedInitiativeResponse.model_validate(response)

