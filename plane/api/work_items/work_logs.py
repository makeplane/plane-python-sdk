from collections.abc import Mapping
from typing import Any

from ...models.work_items import WorkItemWorkLog
from ..base_resource import BaseResource


class WorkLogs(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[WorkItemWorkLog]:
        """Get work logs for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/worklogs",
            params=params,
        )
        return [WorkItemWorkLog.model_validate(item) for item in response]

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: Mapping[str, Any],
    ) -> WorkItemWorkLog:
        """Create a work log for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Work log data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/worklogs", data
        )
        return WorkItemWorkLog.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        work_log_id: str,
        data: Mapping[str, Any],
    ) -> WorkItemWorkLog:
        """Update a work log for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            work_log_id: UUID of the work log
            data: Updated work log data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/worklogs/{work_log_id}",
            data,
        )
        return WorkItemWorkLog.model_validate(response)

    def delete(
        self, workspace_slug: str, project_id: str, work_item_id: str, work_log_id: str
    ) -> None:
        """Delete a work log for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            work_log_id: UUID of the work log
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/worklogs/{work_log_id}"
        )
