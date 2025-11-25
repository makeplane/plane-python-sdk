from typing import Any

from ..models.users import UserLite
from ..models.workspaces import WorkspaceFeature
from .base_resource import BaseResource


class Workspaces(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def get_members(
        self, workspace_slug: str
    ) -> [UserLite]:
        """Get all members of a workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/members")
        return [UserLite.model_validate(item) for item in response or []]

    def get_features(self, workspace_slug: str) -> WorkspaceFeature:
        """Get features of a workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/features")
        return WorkspaceFeature.model_validate(response)
    
    def update_features(self, workspace_slug: str, data: WorkspaceFeature) -> WorkspaceFeature:
        """Update features of a workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Updated workspace features
        """
        response = self._patch(f"{workspace_slug}/features", data.model_dump(exclude_none=True))
        return WorkspaceFeature.model_validate(response)