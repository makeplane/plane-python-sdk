from collections.abc import Mapping
from typing import Any

from ...models.work_item_properties import (
    CreateWorkItemPropertyValue,
    WorkItemPropertyValueDetail,
)
from ..base_resource import BaseResource


class WorkItemPropertyValues(BaseResource):
    """API resource for managing work item property values.

    Note: Each work item can have only ONE value per property.
    The POST method acts as an upsert operation (create or update).
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def retrieve(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        property_id: str,
    ) -> WorkItemPropertyValueDetail:
        """Retrieve the property value for a work item's property.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            property_id: UUID of the property

        Returns:
            The property value for the work item

        Raises:
            HttpError: If the property value is not set (404)
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}"
            f"/work-item-properties/{property_id}/values"
        )
        return WorkItemPropertyValueDetail.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        property_id: str,
        data: CreateWorkItemPropertyValue,
    ) -> WorkItemPropertyValueDetail:
        """Create or update the property value for a work item.

        Note: Since only one value is allowed per work item/property combination,
        this acts as an upsert operation. If a value already exists, it will
        be updated; otherwise, a new value will be created.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            property_id: UUID of the property
            data: Property value data

        Returns:
            The created or updated property value
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}"
            f"/work-item-properties/{property_id}/values",
            data.model_dump(exclude_none=True),
        )
        return WorkItemPropertyValueDetail.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        property_id: str,
        data: Mapping[str, Any] | CreateWorkItemPropertyValue,
    ) -> WorkItemPropertyValueDetail:
        """Update an existing property value (partial update).

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            property_id: UUID of the property
            data: Updated property value data (partial)

        Returns:
            The updated property value

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
        return WorkItemPropertyValueDetail.model_validate(response)

    def delete(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        property_id: str,
    ) -> None:
        """Delete the property value for a work item.

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
