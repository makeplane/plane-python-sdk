from collections.abc import Mapping
from typing import Any

from ...models.work_item_properties import (
    CreateWorkItemProperty,
    UpdateWorkItemProperty,
    WorkItemProperty,
)
from ..base_resource import BaseResource
from .options import WorkItemPropertyOptions
from .values import WorkItemPropertyValues


class WorkItemProperties(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.options = WorkItemPropertyOptions(config)
        self.values = WorkItemPropertyValues(config)

    def create(
        self, workspace_slug: str, project_id: str, type_id: str, data: CreateWorkItemProperty
    ) -> WorkItemProperty:
        """Create a new work item property.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
            data: Work item property data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/work-item-properties",
            data.model_dump(exclude_none=True),
        )
        return WorkItemProperty.model_validate(response)

    def retrieve(
        self, workspace_slug: str, project_id: str, type_id: str, work_item_property_id: str
    ) -> WorkItemProperty:
        """Retrieve a work item property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
            work_item_property_id: UUID of the property
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/work-item-properties/{work_item_property_id}"
        )
        return WorkItemProperty.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        type_id: str,
        work_item_property_id: str,
        data: UpdateWorkItemProperty,
    ) -> WorkItemProperty:
        """Update a work item property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
            work_item_property_id: UUID of the property
            data: Updated property data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/work-item-properties/{work_item_property_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItemProperty.model_validate(response)

    def delete(
        self, workspace_slug: str, project_id: str, type_id: str, work_item_property_id: str
    ) -> None:
        """Delete a work item property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
            work_item_property_id: UUID of the property
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/work-item-properties/{work_item_property_id}"
        )

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        type_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[WorkItemProperty]:
        """List work item properties with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/work-item-properties",
            params=params,
        )
        return [WorkItemProperty.model_validate(item) for item in response]
