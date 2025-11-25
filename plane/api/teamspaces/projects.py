from collections.abc import Iterable, Mapping
from typing import Any

from ...models.projects import PaginatedProjectResponse, Project
from ..base_resource import BaseResource


class TeamspaceProjects(BaseResource):
    """API client for managing projects associated with teamspaces."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, teamspace_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedProjectResponse:
        """List projects associated with a teamspace.

        Args:
            workspace_slug: The workspace slug identifier
            teamspace_id: UUID of the teamspace
            params: Optional query parameters (e.g., per_page, cursor)

        Returns:
            Paginated list of projects
        """
        response = self._get(
            f"{workspace_slug}/teamspaces/{teamspace_id}/projects", params=params
        )
        return PaginatedProjectResponse.model_validate(response)

    def add(
        self, workspace_slug: str, teamspace_id: str, project_ids: Iterable[str]
    ) -> Iterable[Project]:
        """Add projects to a teamspace.

        Args:
            workspace_slug: The workspace slug identifier
            teamspace_id: UUID of the teamspace
            project_ids: List of project UUIDs to add

        Returns:
            List of added projects
        """
        response = self._post(
            f"{workspace_slug}/teamspaces/{teamspace_id}/projects",
            {"project_ids": project_ids},
        )
        return [Project.model_validate(project) for project in response]

    def remove(self, workspace_slug: str, teamspace_id: str, project_ids: Iterable[str]) -> None:
        """Remove projects from a teamspace.

        Args:
            workspace_slug: The workspace slug identifier
            teamspace_id: UUID of the teamspace
            project_ids: List of project UUIDs to remove
        """
        return self._delete(
            f"{workspace_slug}/teamspaces/{teamspace_id}/projects",
            {"project_ids": project_ids},
        )

