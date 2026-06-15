from __future__ import annotations

from typing import Any

from ...models.work_items import (
    CreateWorkItemDependency,
    WorkItemDependencyResponse,
    WorkItemWithRelationType,
)
from ..base_resource import BaseResource


class WorkItemDependencies(BaseResource):
    """API client for managing work item dependency relations.

    Covers the six built-in dependency directions:
    blocking / blocked_by / start_before / start_after / finish_before / finish_after.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, project_id: str, work_item_id: str
    ) -> WorkItemDependencyResponse:
        """List all dependency relations for a work item grouped by direction.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/dependencies/"
        )
        return WorkItemDependencyResponse.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: CreateWorkItemDependency,
    ) -> list[WorkItemWithRelationType]:
        """Create one or more dependency relations for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Dependency creation payload
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/dependencies/",
            data.model_dump(exclude_none=True),
        )
        return [WorkItemWithRelationType.model_validate(item) for item in response]

    def remove(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        related_work_item_id: str,
    ) -> None:
        """Remove a dependency relation between this work item and a target.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            related_work_item_id: UUID of the related work item to remove the dependency with
        """
        self._delete(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/dependencies/{related_work_item_id}/"
        )
