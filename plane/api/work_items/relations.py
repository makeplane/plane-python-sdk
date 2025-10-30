from typing import Any

from ...models.work_items import (
    CreateWorkItemRelation,
    RemoveWorkItemRelation,
    WorkItemRelationResponse,
)
from ..base_resource import BaseResource


class WorkItemRelations(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, project_id: str, work_item_id: str
    ) -> WorkItemRelationResponse:
        """Get relations for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/relations"
        )
        return WorkItemRelationResponse.model_validate(response)

    def create(
        self, workspace_slug: str, project_id: str, work_item_id: str, data: CreateWorkItemRelation
    ) -> None:
        """Create a relation for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Relation data
        """
        return self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/relations",
            data.model_dump(exclude_none=True),
        )

    def delete(
        self, workspace_slug: str, project_id: str, work_item_id: str, data: RemoveWorkItemRelation
    ) -> None:
        """Remove a relation for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Relation removal data
        """
        return self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/relations/remove",
            data.model_dump(exclude_none=True),
        )
