from collections.abc import Mapping
from typing import Any

from .base_resource import BaseResource


class Pages(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def retrieve_workspace_page(
        self, workspace_slug: str, page_id: str, params: Mapping[str, Any] | None = None
    ) -> dict[str, Any]:
        """Retrieve a workspace page by ID.

        Args:
            workspace_slug: The workspace slug identifier
            page_id: UUID of the page
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/pages/{page_id}", params=params)
        return response if isinstance(response, dict) else {}

    def retrieve_project_page(
        self,
        workspace_slug: str,
        project_id: str,
        page_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Retrieve a project page by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            page_id: UUID of the page
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/pages/{page_id}", params=params
        )
        return response if isinstance(response, dict) else {}

    def list_workspace_pages(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """List workspace pages.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/pages", params=params)
        return response if isinstance(response, list) else []

    def list_project_pages(
        self,
        workspace_slug: str,
        project_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """List project pages.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/pages", params=params)
        return response if isinstance(response, list) else []
