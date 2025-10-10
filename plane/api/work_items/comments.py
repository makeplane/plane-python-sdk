from collections.abc import Mapping
from typing import Any

from ...models.work_items import (
    CreateWorkItemComment,
    PaginatedWorkItemCommentResponse,
    UpdateWorkItemComment,
    WorkItemComment,
)
from ..base_resource import BaseResource


class WorkItemComments(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedWorkItemCommentResponse:
        """Get comments for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/comments",
            params=params,
        )
        return PaginatedWorkItemCommentResponse.model_validate(response)

    def retrieve(
        self, workspace_slug: str, project_id: str, work_item_id: str, comment_id: str
    ) -> WorkItemComment:
        """Retrieve a specific comment for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            comment_id: UUID of the comment
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/comments/{comment_id}"
        )
        return WorkItemComment.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: CreateWorkItemComment,
    ) -> WorkItemComment:
        """Create a comment for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Comment data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/comments",
            data.model_dump(exclude_none=True),
        )
        return WorkItemComment.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        comment_id: str,
        data: UpdateWorkItemComment,
    ) -> WorkItemComment:
        """Update a comment for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            comment_id: UUID of the comment
            data: Updated comment data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/comments/{comment_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItemComment.model_validate(response)

    def delete(
        self, workspace_slug: str, project_id: str, work_item_id: str, comment_id: str
    ) -> None:
        """Delete a comment for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            comment_id: UUID of the comment
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/comments/{comment_id}"
        )
