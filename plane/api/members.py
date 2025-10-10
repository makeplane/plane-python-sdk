from collections.abc import Mapping
from typing import Any

from ..models.users import UserLite
from .base_resource import BaseResource


class Members(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list_project_members(
        self,
        workspace_slug: str,
        project_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[UserLite]:
        """List members of a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/members", params=params)
        return [UserLite.model_validate(item) for item in response]

    def add_to_project(self, workspace_slug: str, project_id: str, user_id: str) -> UserLite:
        """Add a user as a member to a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            user_id: UUID of the user
        """
        response = self._post(f"{workspace_slug}/projects/{project_id}/members", {"user": user_id})
        return UserLite.model_validate(response)

    def remove_from_project(self, workspace_slug: str, project_id: str, user_id: str) -> None:
        """Remove a user from a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            user_id: UUID of the user
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/members/{user_id}")
