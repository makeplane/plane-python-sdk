from collections.abc import Mapping
from typing import Any

from ...models.work_items import (
    UpdateWorkItemAttachment,
    WorkItemAttachment,
    WorkItemAttachmentCreateResponse,
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
    ) -> WorkItemAttachmentCreateResponse:
        """Create an attachment for a work item.

        Plane returns a wrapper containing both the created attachment record
        and an S3 multipart-POST policy in ``upload_data``. The caller posts
        the file as ``multipart/form-data`` to ``upload_data["url"]`` with the
        ``upload_data["fields"]`` plus a ``file`` part, then calls ``update``
        with ``is_uploaded=True`` to mark the attachment ready.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Attachment data (filename, size, MIME type, etc.)

        Returns:
            WorkItemAttachmentCreateResponse with ``attachment`` record and
            ``upload_data`` S3 policy.
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments",
            data.model_dump(exclude_none=True),
        )
        return WorkItemAttachmentCreateResponse.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        attachment_id: str,
        data: UpdateWorkItemAttachment,
    ) -> WorkItemAttachment:
        """Update an attachment for a work item.

        The Plane API responds to attachment PATCH with ``204 No Content``
        and exposes no metadata-by-id endpoint (GET on a single attachment
        URL serves the file via S3 redirect). To return the updated record
        per CRUD convention, this method follows the PATCH with a ``list``
        call and filters by id.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            attachment_id: UUID of the attachment
            data: Updated attachment data

        Returns:
            Updated WorkItemAttachment record.

        Raises:
            ValueError: If the attachment cannot be found after the update.
                Plane only includes attachments with ``is_uploaded=True``
                in list responses, so updating an unuploaded attachment to
                stay unuploaded will raise.
        """
        self._patch(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments/{attachment_id}/",
            data.model_dump(exclude_none=True),
        )
        for attachment in self.list(workspace_slug, project_id, work_item_id):
            if attachment.id == attachment_id:
                return attachment
        raise ValueError(
            f"Attachment {attachment_id} not found after update; "
            "Plane only lists attachments with is_uploaded=True."
        )

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
