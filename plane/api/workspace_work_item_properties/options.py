from typing import Any

from ...models.work_item_properties import (
    CreateWorkItemPropertyOption,
    UpdateWorkItemPropertyOption,
    WorkItemPropertyOption,
)
from ..base_resource import BaseResource


class WorkspaceWorkItemPropertyOptions(BaseResource):
    """API client for managing options on workspace-level work item properties."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, property_id: str) -> list[WorkItemPropertyOption]:
        """List options for a workspace work item property.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
        """
        response = self._get(
            f"{workspace_slug}/work-item-properties/{property_id}/options/"
        )
        return [WorkItemPropertyOption.model_validate(item) for item in response]

    def create(
        self,
        workspace_slug: str,
        property_id: str,
        data: CreateWorkItemPropertyOption,
    ) -> WorkItemPropertyOption:
        """Create a new option for a workspace work item property.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
            data: Option data
        """
        response = self._post(
            f"{workspace_slug}/work-item-properties/{property_id}/options/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemPropertyOption.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        property_id: str,
        option_id: str,
        data: UpdateWorkItemPropertyOption,
    ) -> WorkItemPropertyOption:
        """Update an option for a workspace work item property.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
            option_id: UUID of the option
            data: Updated option data
        """
        response = self._patch(
            f"{workspace_slug}/work-item-properties/{property_id}/options/{option_id}/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemPropertyOption.model_validate(response)

    def retrieve(
        self, workspace_slug: str, property_id: str, option_id: str
    ) -> WorkItemPropertyOption:
        """Retrieve an option for a workspace work item property.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
            option_id: UUID of the option
        """
        response = self._get(
            f"{workspace_slug}/work-item-properties/{property_id}/options/{option_id}/"
        )
        return WorkItemPropertyOption.model_validate(response)

    def delete(self, workspace_slug: str, property_id: str, option_id: str) -> None:
        """Delete an option from a workspace work item property.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
            option_id: UUID of the option
        """
        return self._delete(
            f"{workspace_slug}/work-item-properties/{property_id}/options/{option_id}/"
        )
