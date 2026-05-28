from typing import Any

from ...models.work_item_types import CreateWorkItemType, UpdateWorkItemType, WorkItemType
from ..base_resource import BaseResource
from .properties import WorkspaceWorkItemTypeProperties


class WorkspaceWorkItemTypes(BaseResource):
    """API client for managing workspace-level work item types."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.properties = WorkspaceWorkItemTypeProperties(config)

    def list(self, workspace_slug: str) -> list[WorkItemType]:
        """List all work item types in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/work-item-types")
        return [WorkItemType.model_validate(item) for item in response]

    def create(self, workspace_slug: str, data: CreateWorkItemType) -> WorkItemType:
        """Create a new work item type in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Work item type data
        """
        response = self._post(
            f"{workspace_slug}/work-item-types",
            data.model_dump(exclude_none=True),
        )
        return WorkItemType.model_validate(response)

    def retrieve(self, workspace_slug: str, type_id: str) -> WorkItemType:
        """Retrieve a workspace work item type by ID.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the work item type
        """
        response = self._get(f"{workspace_slug}/work-item-types/{type_id}")
        return WorkItemType.model_validate(response)

    def update(
        self, workspace_slug: str, type_id: str, data: UpdateWorkItemType
    ) -> WorkItemType:
        """Update a work item type in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the work item type
            data: Updated work item type data
        """
        response = self._patch(
            f"{workspace_slug}/work-item-types/{type_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItemType.model_validate(response)

    def delete(self, workspace_slug: str, type_id: str) -> None:
        """Delete a workspace work item type by ID.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the work item type
        """
        return self._delete(f"{workspace_slug}/work-item-types/{type_id}")
