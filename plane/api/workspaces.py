from __future__ import annotations

from typing import Any

from ..models.query_params import MemberQueryParams
from ..models.workspaces import WorkspaceFeature, WorkspaceMember
from .base_resource import BaseResource


class Workspaces(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def get_members(
        self, workspace_slug: str, params: MemberQueryParams | None = None
    ) -> list[WorkspaceMember]:
        """Get all members of a workspace.

        Returns a list of WorkspaceMember objects that include role (int) and
        role_slug (str) fields in addition to basic identity fields.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters for filtering and ordering members
        """
        response = self._get(
            f"{workspace_slug}/members",
            params=params.model_dump(exclude_none=True) if params else None,
        )
        return [WorkspaceMember.model_validate(item) for item in response or []]

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
