from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import requests as _requests

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

    def upload_from_bytes(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        file_bytes: bytes,
        name: str,
        content_type: str,
    ) -> WorkItemAttachment:
        """Upload a file to a work item as an attachment.

        Handles the full three-step flow:
          1. Create the attachment record and receive a presigned S3 upload URL.
          2. Upload the file bytes directly to S3 via the presigned POST.
          3. Mark the attachment as uploaded (PATCH is_uploaded=True).

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            file_bytes: Raw file bytes to upload
            name: Filename (e.g. "report.pdf")
            content_type: MIME type (e.g. "application/pdf")
        """
        size = len(file_bytes)

        # Step 1 — create attachment record, get presigned S3 POST URL
        raw = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments",
            {"name": name, "type": content_type, "size": size},
        )
        upload_data = raw["upload_data"]
        asset_id = raw["asset_id"]
        attachment = WorkItemAttachment.model_validate(raw["attachment"])

        # Step 2 — upload bytes to S3 (raw requests, no Plane auth headers)
        fields = upload_data.get("fields", {})
        s3_resp = _requests.post(
            upload_data["url"],
            data=fields,
            files={"file": (name, file_bytes, content_type)},
            timeout=120,
        )
        s3_resp.raise_for_status()

        # Step 3 — mark as uploaded (returns 204, no body)
        self._patch(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments/{asset_id}",
            {"is_uploaded": True},
        )

        return attachment

    def get_download_url(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        attachment_id: str,
    ) -> str:
        """Get a presigned download URL for a work item attachment.

        Calls the attachment detail endpoint which issues a redirect to a
        time-limited presigned S3 URL. The returned URL can be opened in a
        browser or fetched with any HTTP client — no Plane auth required.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            attachment_id: UUID of the attachment

        Returns:
            Presigned S3 URL (time-limited, typically ~1 hour)
        """
        url = self._build_url(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments/{attachment_id}"
        )
        resp = self.session.get(url, headers=self._headers(), allow_redirects=False, timeout=self.config.timeout)
        if resp.status_code in (301, 302, 303, 307, 308):
            location = resp.headers.get("Location")
            if location:
                return location
        # Not a redirect — let _handle_response raise or return
        return self._handle_response(resp)

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
