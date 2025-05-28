"""Users resource."""

from typing import List, Optional, Dict, Any
from .base import BaseResource
from ..models.workspace import Workspace, WorkspaceUpdate
from ..models.base import PaginatedResponse


class WorkspacesResource(BaseResource[Workspace]):
    """Resource for managing users."""

    async def list(
        self, page: int = 1, per_page: int = 20, search: Optional[str] = None
    ) -> Dict[str, Any]:
        """List users with pagination."""
        params = {
            "page": page,
            "per_page": per_page,
        }
        if search:
            params["search"] = search

        response = await self._request("GET", "workspaces", params=params)

        # Parse users
        workspaces_data = response.get("data", [])
        workspaces = [
            Workspace.from_dict(workspace_data) for workspace_data in workspaces_data
        ]

        # Parse pagination
        pagination = PaginatedResponse.from_dict(response.get("pagination", {}))

        return {"workspaces": workspaces, "pagination": pagination}

    async def get(self, workspace_id: str) -> Workspace:
        """Get a user by ID."""
        response = await self._request("GET", f"workspaces/{workspace_id}")
        return Workspace.from_dict(response)

    async def create(self, workspace_data: WorkspaceUpdate) -> Workspace:
        """Create a new user."""
        response = await self._request(
            "POST", "workspaces", data=workspace_data.to_dict()
        )
        return Workspace.from_dict(response)

    async def update(
        self, workspace_id: str, workspace_data: WorkspaceUpdate
    ) -> Workspace:
        """Update a user."""
        response = await self._request(
            "PATCH", f"workspaces/{workspace_id}", data=workspace_data.to_dict()
        )
        return Workspace.from_dict(response)

    async def delete(self, workspace_id: str) -> bool:
        """Delete a user."""
        await self._request("DELETE", f"workspaces/{workspace_id}")
        return True

    async def search(self, query: str, limit: int = 10) -> List[Workspace]:
        """Search users."""
        params = {"q": query, "limit": limit}
        response = await self._request("GET", "workspaces/search", params=params)

        workspaces_data = response.get("workspaces", [])
        return [
            Workspace.from_dict(workspace_data) for workspace_data in workspaces_data
        ]
