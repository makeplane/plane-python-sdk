from typing import Any

from ...models.workspace_templates import (
    CreateWorkItemTemplate,
    UpdateWorkItemTemplate,
    WorkItemTemplate,
)
from ..base_resource import BaseResource


class WorkspaceWorkItemTemplates(BaseResource):
    """API client for managing workspace-level work item templates."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str) -> list[WorkItemTemplate]:
        """List all work item templates in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/workitems/templates/")
        return [WorkItemTemplate.model_validate(item) for item in response]

    def create(self, workspace_slug: str, data: CreateWorkItemTemplate) -> WorkItemTemplate:
        """Create a new work item template in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Work item template data
        """
        response = self._post(
            f"{workspace_slug}/workitems/templates/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemTemplate.model_validate(response)

    def update(
        self, workspace_slug: str, template_id: str, data: UpdateWorkItemTemplate
    ) -> WorkItemTemplate:
        """Update a work item template in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            template_id: UUID of the template
            data: Updated template data
        """
        response = self._patch(
            f"{workspace_slug}/workitems/templates/{template_id}/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemTemplate.model_validate(response)

    def delete(self, workspace_slug: str, template_id: str) -> None:
        """Delete a work item template in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            template_id: UUID of the template
        """
        return self._delete(f"{workspace_slug}/workitems/templates/{template_id}/")
