from collections.abc import Mapping
from typing import Any

from ...models.work_item_properties import (
    CreateWorkItemPropertyValue,
    WorkItemPropertyValueDetail,
)
from ..base_resource import BaseResource


class WorkItemPropertyValues(BaseResource):
    """API resource for managing work item property values.

    For single-value properties:
    - Each work item can have only ONE value per property
    - The POST method acts as an upsert operation (create or update)

    For multi-value properties (when is_multi=True):
    - Multiple values can be set per work item/property
    - POST/PATCH methods replace all existing values (sync operation)
    - Returns a list of values instead of a single value
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def retrieve(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        property_id: str,
    ) -> WorkItemPropertyValueDetail | list[WorkItemPropertyValueDetail]:
        """Retrieve the property value(s) for a work item's property.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            property_id: UUID of the property

        Returns:
            Single WorkItemPropertyValueDetail for non-multi properties,
            or list of WorkItemPropertyValueDetail for multi-value properties

        Raises:
            HttpError: If the property value is not set (404)
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}"
            f"/work-item-properties/{property_id}/values"
        )
        # Handle both single value and list responses
        if isinstance(response, list):
            return [WorkItemPropertyValueDetail.model_validate(item) for item in response]
        return WorkItemPropertyValueDetail.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        property_id: str,
        data: CreateWorkItemPropertyValue,
    ) -> WorkItemPropertyValueDetail | list[WorkItemPropertyValueDetail]:
        """Create or update the property value(s) for a work item.

        For single-value properties:
        - Acts as an upsert operation (create or update)
        - Returns a single WorkItemPropertyValueDetail

        For multi-value properties (is_multi=True):
        - Replaces all existing values with the new ones (sync operation)
        - Returns a list of WorkItemPropertyValueDetail

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            property_id: UUID of the property
            data: Property value data (value can be typed or list for multi-value)

        Returns:
            Single value for non-multi properties, or list of values for multi-value properties
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}"
            f"/work-item-properties/{property_id}/values",
            data.model_dump(exclude_none=True),
        )
        # Handle both single value and list responses
        if isinstance(response, list):
            return [WorkItemPropertyValueDetail.model_validate(item) for item in response]
        return WorkItemPropertyValueDetail.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        property_id: str,
        data: Mapping[str, Any] | CreateWorkItemPropertyValue,
    ) -> WorkItemPropertyValueDetail | list[WorkItemPropertyValueDetail]:
        """Update an existing property value(s) (partial update).

        For single-value properties:
        - Updates the existing value
        - Returns a single WorkItemPropertyValueDetail

        For multi-value properties (is_multi=True):
        - Replaces all existing values with the new ones (sync operation)
        - Returns a list of WorkItemPropertyValueDetail

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            property_id: UUID of the property
            data: Updated property value data (value can be typed or list for multi-value)

        Returns:
            Single value for non-multi properties, or list of values for multi-value properties

        Raises:
            HttpError: If the property value does not exist (404)
        """
        payload = (
            data.model_dump(exclude_none=True)
            if isinstance(data, CreateWorkItemPropertyValue)
            else data
        )
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}"
            f"/work-item-properties/{property_id}/values",
            payload,
        )
        # Handle both single value and list responses
        if isinstance(response, list):
            return [WorkItemPropertyValueDetail.model_validate(item) for item in response]
        return WorkItemPropertyValueDetail.model_validate(response)

    def delete(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        property_id: str,
    ) -> None:
        """Delete the property value(s) for a work item.

        For single-value properties:
        - Deletes the single value

        For multi-value properties (is_multi=True):
        - Deletes all values for that property

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            property_id: UUID of the property

        Raises:
            HttpError: If the property value does not exist (404)
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}"
            f"/work-item-properties/{property_id}/values"
        )
