from __future__ import annotations

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

    def list_project(
        self,
        workspace_slug: str,
        project_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[WorkItemProperty]:
        """List all work item properties for a project regardless of work item type.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-properties",
            params=params,
        )
        return [WorkItemProperty.model_validate(item) for item in response]

    def create_project(
        self, workspace_slug: str, project_id: str, data: CreateWorkItemProperty
    ) -> WorkItemProperty:
        """Create a project-level work item property (not linked to a specific type).

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Work item property data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-item-properties",
            data.model_dump(exclude_none=True),
        )
        return WorkItemProperty.model_validate(response)

    def retrieve_project(
        self, workspace_slug: str, project_id: str, property_id: str
    ) -> WorkItemProperty:
        """Retrieve a project-level work item property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            property_id: UUID of the property
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-properties/{property_id}"
        )
        return WorkItemProperty.model_validate(response)

    def update_project(
        self, workspace_slug: str, project_id: str, property_id: str, data: UpdateWorkItemProperty
    ) -> WorkItemProperty:
        """Update a project-level work item property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            property_id: UUID of the property
            data: Updated property data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-item-properties/{property_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItemProperty.model_validate(response)

    def delete_project(
        self, workspace_slug: str, project_id: str, property_id: str
    ) -> None:
        """Delete a project-level work item property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            property_id: UUID of the property
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-item-properties/{property_id}"
        )

    def attach_to_type(
        self, workspace_slug: str, project_id: str, type_id: str, property_ids: list[str]
    ) -> list[str]:
        """Attach existing project-level properties to a work item type.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
            property_ids: List of property UUIDs to attach
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/properties",
            {"properties": property_ids},
        )
        return response.get("properties", [])

    def detach_from_type(
        self, workspace_slug: str, project_id: str, type_id: str, property_id: str
    ) -> None:
        """Detach a property from a work item type.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
            property_id: UUID of the property to detach
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/properties/{property_id}"
        )

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        type_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[WorkItemProperty]:
        """List project-level work item properties for a type.

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

