from collections.abc import Mapping
from typing import Any

from ..models.work_item_types import CreateWorkItemType, UpdateWorkItemType, WorkItemType
from .base_resource import BaseResource


class WorkItemTypes(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(
        self, workspace_slug: str, project_id: str, data: CreateWorkItemType
    ) -> WorkItemType:
        """Create a new work item type.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Work item type data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-item-types",
            data.model_dump(exclude_none=True),
        )
        return WorkItemType.model_validate(response)

    def retrieve(
        self, workspace_slug: str, project_id: str, work_item_type_id: str
    ) -> WorkItemType:
        """Retrieve a work item type by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_type_id: UUID of the work item type
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{work_item_type_id}"
        )
        return WorkItemType.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_type_id: str,
        data: UpdateWorkItemType,
    ) -> WorkItemType:
        """Update a work item type by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_type_id: UUID of the work item type
            data: Updated work item type data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{work_item_type_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItemType.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, work_item_type_id: str) -> None:
        """Delete a work item type by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_type_id: UUID of the work item type
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{work_item_type_id}"
        )

    def list(
        self, workspace_slug: str, project_id: str, params: Mapping[str, Any] | None = None
    ) -> list[WorkItemType]:
        """List work item types with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-types", params=params
        )
        return [WorkItemType.model_validate(item) for item in response]
