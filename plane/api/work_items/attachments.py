from collections.abc import Mapping
from typing import Any

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
    ) -> list[dict[str, Any]]:
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
        return response if isinstance(response, list) else []

    def retrieve(
        self, workspace_slug: str, project_id: str, work_item_id: str, attachment_id: str
    ) -> dict[str, Any]:
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
        return response if isinstance(response, dict) else {}

    def create(
        self, workspace_slug: str, project_id: str, work_item_id: str, data: Mapping[str, Any]
    ) -> dict[str, Any]:
        """Create an attachment for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Attachment data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/attachments", data
        )
        return response if isinstance(response, dict) else {}

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        attachment_id: str,
        data: Mapping[str, Any],
    ) -> dict[str, Any]:
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
            data,
        )
        return response if isinstance(response, dict) else {}

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
