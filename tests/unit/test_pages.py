"""Unit tests for Pages API resource (smoke tests with real HTTP requests)."""

import time

from plane.client import PlaneClient
from plane.models.pages import CreatePage, PaginatedPageResponse
from plane.models.projects import Project


class TestPagesAPI:
    """Test Pages API resource."""

    def test_create_project_page(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test creating a project page."""
        page_data = CreatePage(
            name=f"Test Page {int(time.time())}",
            description_html="<p>Test page description</p>",
            color="#4ECDC4",
        )

        page = client.pages.create_project_page(workspace_slug, project.id, page_data)
        assert page is not None
        assert page.id is not None
        assert page.name == page_data.name

    def test_create_workspace_page(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test creating a workspace page."""
        page_data = CreatePage(
            name=f"Test Workspace Page {int(time.time())}",
            description_html="<p>Test workspace page</p>",
            color="#FF6B6B",
        )

        page = client.pages.create_workspace_page(workspace_slug, page_data)
        assert page is not None
        assert page.id is not None
        assert page.name == page_data.name

    def test_list_workspace_pages(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing workspace pages returns paginated response."""
        response = client.pages.list_workspace_pages(workspace_slug)
        assert isinstance(response, PaginatedPageResponse)
        assert hasattr(response, "results")
        assert isinstance(response.results, list)

    def test_list_workspace_pages_contains_created_page(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test that a freshly created workspace page appears in the list."""
        page_data = CreatePage(
            name=f"Listable Workspace Page {int(time.time())}",
            description_html="<p>list test</p>",
        )
        created = client.pages.create_workspace_page(workspace_slug, page_data)
        try:
            response = client.pages.list_workspace_pages(workspace_slug)
            page_ids = [p.id for p in response.results]
            assert created.id in page_ids
        finally:
            try:
                client.pages.delete_workspace_page(workspace_slug, created.id)
            except Exception:
                pass

    def test_list_project_pages(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing project pages returns paginated response."""
        response = client.pages.list_project_pages(workspace_slug, project.id)
        assert isinstance(response, PaginatedPageResponse)
        assert hasattr(response, "results")
        assert isinstance(response.results, list)

    def test_list_project_pages_contains_created_page(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test that a freshly created project page appears in the list."""
        page_data = CreatePage(
            name=f"Listable Project Page {int(time.time())}",
            description_html="<p>list test</p>",
        )
        created = client.pages.create_project_page(workspace_slug, project.id, page_data)
        try:
            response = client.pages.list_project_pages(workspace_slug, project.id)
            page_ids = [p.id for p in response.results]
            assert created.id in page_ids
        finally:
            try:
                client.pages.delete_project_page(workspace_slug, project.id, created.id)
            except Exception:
                pass

