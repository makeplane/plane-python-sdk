"""Unit tests for Pages API resource (smoke tests with real HTTP requests)."""

from plane.client import PlaneClient
from plane.models.pages import CreatePage
from plane.models.projects import Project


class TestPagesAPI:
    """Test Pages API resource."""

    def test_create_project_page(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test creating a project page."""
        import time
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
        import time
        page_data = CreatePage(
            name=f"Test Workspace Page {int(time.time())}",
            description_html="<p>Test workspace page</p>",
            color="#FF6B6B",
        )
        
        page = client.pages.create_workspace_page(workspace_slug, page_data)
        assert page is not None
        assert page.id is not None
        assert page.name == page_data.name

