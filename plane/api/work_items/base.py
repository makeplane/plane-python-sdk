from typing import Any

from ...models.query_params import RetrieveQueryParams, WorkItemQueryParams
from ...models.work_items import (
    CreateWorkItem,
    PaginatedWorkItemResponse,
    UpdateWorkItem,
    WorkItem,
    WorkItemDetail,
    WorkItemSearch,
)
from ..base_resource import BaseResource
from .activities import WorkItemActivities
from .attachments import WorkItemAttachments
from .comments import WorkItemComments
from .links import WorkItemLinks
from .relations import WorkItemRelations
from .work_logs import WorkLogs


class WorkItems(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.relations = WorkItemRelations(config)
        self.links = WorkItemLinks(config)
        self.attachments = WorkItemAttachments(config)
        self.comments = WorkItemComments(config)
        self.activities = WorkItemActivities(config)
        self.work_logs = WorkLogs(config)

    def create(self, workspace_slug: str, project_id: str, data: CreateWorkItem) -> WorkItem:
        """Create a new work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Work item data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items",
            data.model_dump(exclude_none=True),
        )
        return WorkItem.model_validate(response)

    def retrieve(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: RetrieveQueryParams | None = None,
    ) -> WorkItemDetail:
        """Retrieve a work item by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            params: Optional query parameters for expand, fields, etc.

        Example:
            # Get work item with expanded relationships
            from plane.models.schemas import RetrieveQueryParams

            work_item = client.work_items.retrieve(
                "my-workspace",
                "project-id",
                "work-item-id",
                params=RetrieveQueryParams(expand="assignees,labels,state")
            )

            # Get specific fields only
            work_item = client.work_items.retrieve(
                "my-workspace",
                "project-id",
                "work-item-id",
                params=RetrieveQueryParams(fields="id,name,priority,state")
            )
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}",
            params=query_params,
        )
        return WorkItemDetail.model_validate(response)

    def retrieve_by_identifier(
        self,
        workspace_slug: str,
        project_identifier: str,
        issue_identifier: int,
        params: RetrieveQueryParams | None = None,
    ) -> WorkItemDetail:
        """Retrieve a work item by project and issue identifiers.

        Args:
            workspace_slug: The workspace slug identifier
            project_identifier: Project identifier string
            issue_identifier: Issue sequence number
            params: Optional query parameters for expand, fields, etc.
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/work-items/{project_identifier}-{issue_identifier}",
            params=query_params,
        )
        return WorkItemDetail.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: UpdateWorkItem,
    ) -> WorkItem:
        """Update a work item by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Updated work item data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItem.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, work_item_id: str) -> None:
        """Delete a work item by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        params: WorkItemQueryParams | None = None,
    ) -> PaginatedWorkItemResponse:
        """List work items with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters for filtering, ordering, and pagination

        Example:
            from plane.models.schemas import WorkItemQueryParams

            # List work items with filters
            work_items = client.work_items.list(
                "my-workspace",
                "project-id",
                params=WorkItemQueryParams(
                    priority="high",
                    state="state-id",
                    expand="assignees,labels"
                )
            )
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items", params=query_params
        )
        return PaginatedWorkItemResponse.model_validate(response)

    def search(
        self,
        workspace_slug: str,
        query: str,
        params: RetrieveQueryParams | None = None,
    ) -> WorkItemSearch:
        """Search work items.

        Args:
            workspace_slug: The workspace slug identifier
            query: Search query string
            params: Optional query parameters for expand, fields, etc.
        """
        search_params = {"q": query}
        if params:
            search_params.update(params.model_dump(exclude_none=True))
        response = self._get(f"{workspace_slug}/work-items/search", params=search_params)
        return WorkItemSearch.model_validate(response)
