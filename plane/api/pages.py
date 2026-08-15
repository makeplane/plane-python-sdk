from typing import Any

from ..models.pages import CreatePage, Page, PaginatedPageResponse, UpdatePage
from ..models.query_params import PaginatedQueryParams, RetrieveQueryParams
from .base_resource import BaseResource


class Pages(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list_workspace_pages(
        self,
        workspace_slug: str,
        params: PaginatedQueryParams | None = None,
    ) -> PaginatedPageResponse:
        """List all workspace pages.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional pagination/query parameters
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(f"{workspace_slug}/pages", params=query_params)
        return PaginatedPageResponse.model_validate(response)

    def list_project_pages(
        self,
        workspace_slug: str,
        project_id: str,
        params: PaginatedQueryParams | None = None,
    ) -> PaginatedPageResponse:
        """List all pages in a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional pagination/query parameters
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/pages", params=query_params
        )
        return PaginatedPageResponse.model_validate(response)

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

    def update_workspace_page(
        self,
        workspace_slug: str,
        page_id: str,
        data: UpdatePage,
    ) -> Page:
        """Update a workspace page.

        Args:
            workspace_slug: The workspace slug identifier
            page_id: UUID of the page
            data: Fields to change. Send name, description_html, or both; a page that
                is locked or archived is refused.

        Note:
            Content is written through Plane's live collaboration service, which owns
            the document. If it is unreachable the API answers 502 and nothing is
            written, rather than leaving the editor showing the old text.
        """
        response = self._put(
            f"{workspace_slug}/pages/{page_id}",
            data.model_dump(exclude_none=True, mode="json"),
        )
        return Page.model_validate(response)

    def update_project_page(
        self,
        workspace_slug: str,
        project_id: str,
        page_id: str,
        data: UpdatePage,
    ) -> Page:
        """Update a project page.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            page_id: UUID of the page
            data: Fields to change. Send name, description_html, or both; a page that
                is locked or archived is refused.

        Note:
            Content is written through Plane's live collaboration service, which owns
            the document. If it is unreachable the API answers 502 and nothing is
            written, rather than leaving the editor showing the old text.
        """
        response = self._put(
            f"{workspace_slug}/projects/{project_id}/pages/{page_id}",
            data.model_dump(exclude_none=True, mode="json"),
        )
        return Page.model_validate(response)

    def archive_workspace_page(self, workspace_slug: str, page_id: str) -> None:
        """Archive a workspace page.

        Args:
            workspace_slug: The workspace slug identifier
            page_id: UUID of the page

        Note:
            Archiving is the reversible step `delete_workspace_page` requires.
        """
        self._post(f"{workspace_slug}/pages/{page_id}/archive")

    def unarchive_workspace_page(self, workspace_slug: str, page_id: str) -> None:
        """Restore an archived workspace page.

        Args:
            workspace_slug: The workspace slug identifier
            page_id: UUID of the page
        """
        self._delete(f"{workspace_slug}/pages/{page_id}/archive")

    def archive_project_page(self, workspace_slug: str, project_id: str, page_id: str) -> None:
        """Archive a project page.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            page_id: UUID of the page

        Note:
            Archiving is the reversible step `delete_project_page` requires.
        """
        self._post(f"{workspace_slug}/projects/{project_id}/pages/{page_id}/archive")

    def unarchive_project_page(self, workspace_slug: str, project_id: str, page_id: str) -> None:
        """Restore an archived project page.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            page_id: UUID of the page
        """
        self._delete(f"{workspace_slug}/projects/{project_id}/pages/{page_id}/archive")

    def delete_workspace_page(self, workspace_slug: str, page_id: str) -> None:
        """Delete a workspace page by ID.

        Args:
            workspace_slug: The workspace slug identifier
            page_id: UUID of the page

        Note:
            The page must be archived first; the API answers 400
            "The page should be archived before deleting" otherwise.
        """
        return self._delete(f"{workspace_slug}/pages/{page_id}")

    def delete_project_page(self, workspace_slug: str, project_id: str, page_id: str) -> None:
        """Delete a project page by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            page_id: UUID of the page

        Note:
            The page must be archived first; the API answers 400
            "The page should be archived before deleting" otherwise.
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/pages/{page_id}")
