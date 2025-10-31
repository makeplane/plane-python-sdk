from collections.abc import Mapping
from typing import Any

from ...models.work_items import (
    CreateWorkItemLink,
    PaginatedWorkItemLinkResponse,
    UpdateWorkItemLink,
    WorkItemLink,
)
from ..base_resource import BaseResource


class WorkItemLinks(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedWorkItemLinkResponse:
        """Get links for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/links",
            params=params,
        )
        return PaginatedWorkItemLinkResponse.model_validate(response)

    def retrieve(
        self, workspace_slug: str, project_id: str, work_item_id: str, link_id: str
    ) -> WorkItemLink:
        """Retrieve a specific link for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            link_id: UUID of the link
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/links/{link_id}"
        )
        return WorkItemLink.model_validate(response)

    def create(
        self, workspace_slug: str, project_id: str, work_item_id: str, data: CreateWorkItemLink
    ) -> WorkItemLink:
        """Create a link for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Link data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/links",
            data.model_dump(exclude_none=True),
        )
        return WorkItemLink.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        link_id: str,
        data: UpdateWorkItemLink,
    ) -> WorkItemLink:
        """Update a link for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            link_id: UUID of the link
            data: Updated link data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/links/{link_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItemLink.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, work_item_id: str, link_id: str) -> None:
        """Delete a link for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            link_id: UUID of the link
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/links/{link_id}"
        )
