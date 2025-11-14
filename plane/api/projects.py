from collections.abc import Mapping
from typing import Any

from ..models.projects import (
    CreateProject,
    PaginatedProjectResponse,
    Project,
    ProjectFeature,
    ProjectWorklogSummary,
    UpdateProject,
)
from ..models.query_params import PaginatedQueryParams
from ..models.users import UserLite
from .base_resource import BaseResource


class Projects(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, data: CreateProject) -> Project:
        """Create a new project.

        Args:
            workspace_slug: The workspace slug identifier
            data: Project data
        """
        response = self._post(f"{workspace_slug}/projects", data.model_dump(exclude_none=True))
        return Project.model_validate(response)

    def retrieve(self, workspace_slug: str, project_id: str) -> Project:
        """Retrieve a project by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}")
        return Project.model_validate(response)

    def update(self, workspace_slug: str, project_id: str, data: UpdateProject) -> Project:
        """Update a project by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Updated project data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}", data.model_dump(exclude_none=True)
        )
        return Project.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str) -> None:
        """Delete a project by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}")

    def list(
        self, workspace_slug: str, params: PaginatedQueryParams | None = None
    ) -> PaginatedProjectResponse:
        """List projects with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(f"{workspace_slug}/projects", params=query_params)
        return PaginatedProjectResponse.model_validate(response)

    def get_worklog_summary(self, workspace_slug: str, project_id: str) -> [ProjectWorklogSummary]:
        """Get work log summary for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/total-worklogs")
        return [ProjectWorklogSummary.model_validate(item) for item in response]

    def get_members(
        self, workspace_slug: str, project_id: str, params: Mapping[str, Any] | None = None
    ) -> [UserLite]:
        """Get all members of a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/members", params=params)
        return [UserLite.model_validate(item) for item in response or []]

    def get_features(self, workspace_slug: str, project_id: str) -> ProjectFeature:
        """Get features of a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/features")
        return ProjectFeature.model_validate(response)

    def update_features(
        self, workspace_slug: str, project_id: str, data: ProjectFeature
    ) -> ProjectFeature:
        """Update features of a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Updated project features
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/features", data.model_dump(exclude_none=True)
        )
        return ProjectFeature.model_validate(response)
