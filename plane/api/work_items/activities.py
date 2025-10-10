from collections.abc import Mapping
from typing import Any

from ...models.work_items import PaginatedWorkItemActivityResponse, WorkItemActivity
from ..base_resource import BaseResource


class WorkItemActivities(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedWorkItemActivityResponse:
        """Get activities for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/activities",
            params=params,
        )
        return PaginatedWorkItemActivityResponse.model_validate(response)

    def retrieve(
        self, workspace_slug: str, project_id: str, work_item_id: str, activity_id: str
    ) -> WorkItemActivity:
        """Retrieve a specific activity for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            activity_id: UUID of the activity
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/activities/{activity_id}"
        )
        return WorkItemActivity.model_validate(response)
