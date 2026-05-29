from typing import Any

from ..models.workspace_project_states import (
    CreateWorkspaceProjectState,
    UpdateWorkspaceProjectState,
    WorkspaceProjectState,
)
from .base_resource import BaseResource


class WorkspaceProjectStates(BaseResource):
    """API client for managing workspace-level project states."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str) -> list[WorkspaceProjectState]:
        """List all project states in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/project-states/")
        return [WorkspaceProjectState.model_validate(item) for item in response]

    def create(
        self, workspace_slug: str, data: CreateWorkspaceProjectState
    ) -> WorkspaceProjectState:
        """Create a new project state in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Project state data
        """
        response = self._post(
            f"{workspace_slug}/project-states/",
            data.model_dump(exclude_none=True),
        )
        return WorkspaceProjectState.model_validate(response)

    def update(
        self, workspace_slug: str, state_id: str, data: UpdateWorkspaceProjectState
    ) -> WorkspaceProjectState:
        """Update a project state in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            state_id: UUID of the state
            data: Updated state data
        """
        response = self._patch(
            f"{workspace_slug}/project-states/{state_id}/",
            data.model_dump(exclude_none=True),
        )
        return WorkspaceProjectState.model_validate(response)

    def delete(self, workspace_slug: str, state_id: str) -> None:
        """Delete a project state in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            state_id: UUID of the state
        """
        return self._delete(f"{workspace_slug}/project-states/{state_id}/")
