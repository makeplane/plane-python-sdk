from collections.abc import Mapping
from typing import Any

from ...models.teamspaces import (
    CreateTeamspace,
    PaginatedTeamspaceResponse,
    Teamspace,
    UpdateTeamspace,
)
from ..base_resource import BaseResource
from .members import TeamspaceMembers
from .projects import TeamspaceProjects


class Teamspaces(BaseResource):
    """API client for managing teamspaces in workspaces."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.projects = TeamspaceProjects(config)
        self.members = TeamspaceMembers(config)

    def create(self, workspace_slug: str, data: CreateTeamspace) -> Teamspace:
        """Create a new teamspace in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Teamspace data

        Returns:
            The created teamspace
        """
        response = self._post(
            f"{workspace_slug}/teamspaces",
            data.model_dump(exclude_none=True),
        )
        return Teamspace.model_validate(response)

    def retrieve(self, workspace_slug: str, teamspace_id: str) -> Teamspace:
        """Retrieve a teamspace by ID.

        Args:
            workspace_slug: The workspace slug identifier
            teamspace_id: UUID of the teamspace

        Returns:
            The requested teamspace
        """
        response = self._get(f"{workspace_slug}/teamspaces/{teamspace_id}")
        return Teamspace.model_validate(response)

    def update(
        self, workspace_slug: str, teamspace_id: str, data: UpdateTeamspace
    ) -> Teamspace:
        """Update a teamspace by ID.

        Args:
            workspace_slug: The workspace slug identifier
            teamspace_id: UUID of the teamspace
            data: Updated teamspace data

        Returns:
            The updated teamspace
        """
        response = self._patch(
            f"{workspace_slug}/teamspaces/{teamspace_id}",
            data.model_dump(exclude_none=True),
        )
        return Teamspace.model_validate(response)

    def delete(self, workspace_slug: str, teamspace_id: str) -> None:
        """Delete a teamspace by ID.

        Args:
            workspace_slug: The workspace slug identifier
            teamspace_id: UUID of the teamspace
        """
        return self._delete(f"{workspace_slug}/teamspaces/{teamspace_id}")

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedTeamspaceResponse:
        """List teamspaces in the workspace with optional filtering.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters (e.g., per_page, cursor)

        Returns:
            Paginated list of teamspaces
        """
        response = self._get(f"{workspace_slug}/teamspaces", params=params)
        return PaginatedTeamspaceResponse.model_validate(response)

