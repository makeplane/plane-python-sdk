from collections.abc import Mapping
from typing import Any

from ...models.work_item_properties import (
    CreateWorkItemPropertyValue,
    WorkItemPropertyValue,
    WorkItemPropertyValueDetail,
)
from ..base_resource import BaseResource


class WorkItemPropertyValues(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[WorkItemPropertyValueDetail]:
        """Get work item property values.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/work-item-properties/values",
            params=params,
        )
        return [WorkItemPropertyValueDetail.model_validate(item) for item in response]

    def retrieve(
        self, workspace_slug: str, project_id: str, work_item_id: str, value_id: str
    ) -> WorkItemPropertyValue:
        """Retrieve a work item property value.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            value_id: UUID of the property value
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/work-item-properties/values/{value_id}"
        )
        return WorkItemPropertyValue.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        property_id: str,
        data: CreateWorkItemPropertyValue,
    ) -> WorkItemPropertyValue:
        """Create a new work item property value.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            property_id: UUID of the property
            data: Property value data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/work-item-properties/{property_id}/values",
            data.model_dump(exclude_none=True),
        )
        return WorkItemPropertyValue.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        value_id: str,
        data: Mapping[str, Any],
    ) -> WorkItemPropertyValue:
        """Update a work item property value.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            value_id: UUID of the property value
            data: Updated property value data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/work-item-properties/values/{value_id}",
            data,
        )
        return WorkItemPropertyValue.model_validate(response)

    def delete(
        self, workspace_slug: str, project_id: str, work_item_id: str, value_id: str
    ) -> None:
        """Delete a work item property value.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            value_id: UUID of the property value
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/work-item-properties/values/{value_id}"
        )
