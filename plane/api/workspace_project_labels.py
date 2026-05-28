from typing import Any

from ..models.workspace_project_labels import (
    CreateWorkspaceProjectLabel,
    UpdateWorkspaceProjectLabel,
    WorkspaceProjectLabel,
)
from .base_resource import BaseResource


class WorkspaceProjectLabels(BaseResource):
    """API client for managing workspace-level project labels."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str) -> list[WorkspaceProjectLabel]:
        """List all project labels in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/project-labels/")
        return [WorkspaceProjectLabel.model_validate(item) for item in response]

    def create(
        self, workspace_slug: str, data: CreateWorkspaceProjectLabel
    ) -> WorkspaceProjectLabel:
        """Create a new project label in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Project label data
        """
        response = self._post(
            f"{workspace_slug}/project-labels/",
            data.model_dump(exclude_none=True),
        )
        return WorkspaceProjectLabel.model_validate(response)

    def update(
        self, workspace_slug: str, label_id: str, data: UpdateWorkspaceProjectLabel
    ) -> WorkspaceProjectLabel:
        """Update a project label in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            label_id: UUID of the label
            data: Updated label data
        """
        response = self._patch(
            f"{workspace_slug}/project-labels/{label_id}/",
            data.model_dump(exclude_none=True),
        )
        return WorkspaceProjectLabel.model_validate(response)

    def delete(self, workspace_slug: str, label_id: str) -> None:
        """Delete a project label in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            label_id: UUID of the label
        """
        return self._delete(f"{workspace_slug}/project-labels/{label_id}/")
