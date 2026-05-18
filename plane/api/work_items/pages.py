from collections.abc import Mapping
from typing import Any

from ...models.work_item_pages import (
    CreateWorkItemPage,
    PaginatedWorkItemPageResponse,
    WorkItemPage,
)
from ..base_resource import BaseResource


class WorkItemPages(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedWorkItemPageResponse:
        """List page links for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/pages",
            params=params,
        )
        return PaginatedWorkItemPageResponse.model_validate(response)

    def retrieve(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        work_item_page_id: str,
    ) -> WorkItemPage:
        """Retrieve a specific page link for a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            work_item_page_id: UUID of the work item page link
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/pages/{work_item_page_id}"
        )
        return WorkItemPage.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: CreateWorkItemPage,
    ) -> WorkItemPage:
        """Link a page to a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Page link data containing page_id
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/pages",
            data.model_dump(exclude_none=True),
        )
        return WorkItemPage.model_validate(response)

    def delete(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        work_item_page_id: str,
    ) -> None:
        """Remove a page link from a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            work_item_page_id: UUID of the work item page link
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/pages/{work_item_page_id}"
        )
