from typing import List, Optional, Dict, Any
from .base import BaseResource
from ..models.project import Project, ProjectCreate, ProjectUpdate
from ..models.base import PaginatedResponse


class ProjectsResource(BaseResource[Project]):
    """Resource for managing projects."""

    async def list(
        self,
        workspace_slug: str,
        page: int = 1,
        per_page: int = 20,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List projects in a workspace with pagination."""
        params = {
            "page": page,
            "per_page": per_page,
        }
        if search:
            params["search"] = search

        response = await self._request(
            "GET", f"api/v1/workspaces/{workspace_slug}/projects/", params=params
        )

        projects_data = response.get("data", []) or response.get("results", [])
        projects = [Project.from_dict(project_data) for project_data in projects_data]
        pagination = PaginatedResponse.from_dict(
            response.get("pagination", {}) or response
        )

        return {"projects": projects, "pagination": pagination}

    async def get(self, workspace_slug: str, project_id: str) -> Project:
        """Get a project by ID."""
        response = await self._request(
            "GET", f"api/v1/workspaces/{workspace_slug}/projects/{project_id}/"
        )
        return Project.from_dict(response)

    async def create(self, workspace_slug: str, project_data: ProjectCreate) -> Project:
        """Create a new project in a workspace."""
        response = await self._request(
            "POST",
            f"api/v1/workspaces/{workspace_slug}/projects/",
            data=project_data.to_dict(),
        )
        return Project.from_dict(response)

    async def update(
        self, workspace_slug: str, project_id: str, project_data: ProjectUpdate
    ) -> Project:
        """Update a project in a workspace."""
        response = await self._request(
            "PATCH",
            f"api/v1/workspaces/{workspace_slug}/projects/{project_id}/",
            data=project_data.to_dict(),
        )
        return Project.from_dict(response)

    async def delete(self, workspace_slug: str, project_id: str) -> bool:
        """Delete a project in a workspace."""
        await self._request(
            "DELETE", f"api/v1/workspaces/{workspace_slug}/projects/{project_id}/"
        )
        return True
