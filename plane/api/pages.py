from collections.abc import Mapping
from typing import Any

from ..models.pages import CreatePage, Page, PaginatedPageResponse
from ..models.query_params import PaginatedQueryParams, RetrieveQueryParams
from .base_resource import BaseResource


class Pages(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def retrieve_workspace_page(
        self,
        workspace_slug: str,
        page_id: str,
        params: RetrieveQueryParams | None = None,
    ) -> Page:
        """Retrieve a workspace page by ID.

        Args:
            workspace_slug: The workspace slug identifier
            page_id: UUID of the page
            params: Optional query parameters for expand, fields, etc.
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(f"{workspace_slug}/pages/{page_id}", params=query_params)
        return Page.model_validate(response)

    def retrieve_project_page(
        self,
        workspace_slug: str,
        project_id: str,
        page_id: str,
        params: RetrieveQueryParams | None = None,
    ) -> Page:
        """Retrieve a project page by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            page_id: UUID of the page
            params: Optional query parameters for expand, fields, etc.
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/pages/{page_id}", params=query_params
        )
        return Page.model_validate(response)
    
    def create_workspace_page(
        self,
        workspace_slug: str,
        data: CreatePage,
    ) -> Page:
        """Create a workspace page.

        Args:
            workspace_slug: The workspace slug identifier
            data: Page data
        """
        response = self._post(
            f"{workspace_slug}/pages",
            data.model_dump(exclude_none=True),
        )
        return Page.model_validate(response)

    def create_project_page(
        self,
        workspace_slug: str,
        project_id: str,
        data: CreatePage,
    ) -> Page:
        """Create a project page.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Page data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/pages",
            data.model_dump(exclude_none=True),
        )
        return Page.model_validate(response)
