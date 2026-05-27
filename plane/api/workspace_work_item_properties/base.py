from typing import Any

from ...models.work_item_properties import (
    CreateWorkItemProperty,
    UpdateWorkItemProperty,
    WorkItemProperty,
)
from ..base_resource import BaseResource
from .options import WorkspaceWorkItemPropertyOptions


class WorkspaceWorkItemProperties(BaseResource):
    """API client for managing workspace-level work item properties."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.options = WorkspaceWorkItemPropertyOptions(config)

    def list(self, workspace_slug: str) -> list[WorkItemProperty]:
        """List all work item properties in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/work-item-properties/")
        return [WorkItemProperty.model_validate(item) for item in response]

    def create(
        self, workspace_slug: str, data: CreateWorkItemProperty
    ) -> WorkItemProperty:
        """Create a new work item property in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Work item property data
        """
        response = self._post(
            f"{workspace_slug}/work-item-properties/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemProperty.model_validate(response)

    def update(
        self, workspace_slug: str, property_id: str, data: UpdateWorkItemProperty
    ) -> WorkItemProperty:
        """Update a work item property in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
            data: Updated property data
        """
        response = self._patch(
            f"{workspace_slug}/work-item-properties/{property_id}/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemProperty.model_validate(response)

    def delete(self, workspace_slug: str, property_id: str) -> None:
        """Delete a work item property in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
        """
        return self._delete(f"{workspace_slug}/work-item-properties/{property_id}/")
