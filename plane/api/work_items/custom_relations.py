from __future__ import annotations

from typing import Any

from ...models.work_items import (
    CreateWorkItemCustomRelation,
    RemoveWorkItemCustomRelation,
    WorkItemWithRelationType,
)
from ..base_resource import BaseResource


class WorkItemCustomRelations(BaseResource):
    """API client for managing custom (definition-based) work item relations.

    Custom relations are workspace-level types defined via the
    work-item-relation-definitions endpoint.  Each definition has an outward label
    and an inward label that controls directionality.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, project_id: str, work_item_id: str
    ) -> dict[str, list[WorkItemWithRelationType]]:
        """List all custom relations for a work item grouped by definition label.

        Response keys are the outward/inward labels from active workspace relation
        definitions (e.g. 'implements', 'implemented by', 'relates to').

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/work-item-relations/"
        )
        return {
            label: [WorkItemWithRelationType.model_validate(item) for item in items]
            for label, items in response.items()
        }

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: CreateWorkItemCustomRelation,
    ) -> list[WorkItemWithRelationType]:
        """Create one or more custom relations for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Custom relation creation payload
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/work-item-relations/",
            data.model_dump(exclude_none=True),
        )
        return [WorkItemWithRelationType.model_validate(item) for item in response]

    def remove(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: RemoveWorkItemCustomRelation,
    ) -> None:
        """Remove a custom relation between this work item and a target.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Removal payload containing the related work item UUID
        """
        return self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/work-item-relations/remove/",
            data.model_dump(exclude_none=True),
        )
