from collections.abc import Mapping
from typing import Any

from ...models.work_items import (
    UpdateWorkItemAttachment,
    WorkItemAttachment,
    WorkItemAttachmentUploadRequest,
)
from ..base_resource import BaseResource


class WorkItemAttachments(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[WorkItemAttachment]:
        """Get attachments for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments",
            params=params,
        )
        if isinstance(response, list):
            return [WorkItemAttachment.model_validate(item) for item in response]
        return []

    def retrieve(
        self, workspace_slug: str, project_id: str, work_item_id: str, attachment_id: str
    ) -> WorkItemAttachment:
        """Retrieve a specific attachment for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            attachment_id: UUID of the attachment
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments/{attachment_id}"
        )
        return WorkItemAttachment.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: WorkItemAttachmentUploadRequest,
    ) -> WorkItemAttachment:
        """Create an attachment for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Attachment data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments",
            data.model_dump(exclude_none=True),
        )
        return WorkItemAttachment.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        attachment_id: str,
        data: UpdateWorkItemAttachment,
    ) -> WorkItemAttachment:
        """Update an attachment for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            attachment_id: UUID of the attachment
            data: Updated attachment data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments/{attachment_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItemAttachment.model_validate(response)

    def delete(
        self, workspace_slug: str, project_id: str, work_item_id: str, attachment_id: str
    ) -> None:
        """Delete an attachment for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            attachment_id: UUID of the attachment
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments/{attachment_id}"
        )
