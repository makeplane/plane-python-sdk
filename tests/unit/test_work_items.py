"""Unit tests for WorkItems API resource (smoke tests with real HTTP requests)."""

import pytest

from plane.client import PlaneClient
from plane.models.projects import Project
from plane.models.query_params import PaginatedQueryParams
from plane.models.work_items import CreateWorkItem, UpdateWorkItem


class TestWorkItemsAPI:
    """Test WorkItems API resource."""

    def test_list_work_items(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing work items."""
        response = client.work_items.list(workspace_slug, project.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_work_items_with_params(
        self, client: PlaneClient, workspace_slug: str, project
    ) -> None:
        """Test listing work items with query parameters."""
        params = PaginatedQueryParams(per_page=10)
        response = client.work_items.list(workspace_slug, project.id, params=params)
        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) <= 10

    def test_search_work_items(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test searching work items."""
        response = client.work_items.search(workspace_slug, "test")
        assert response is not None
        assert hasattr(response, "issues")
        assert isinstance(response.issues, list)


class TestWorkItemsAPICRUD:
    """Test WorkItems API CRUD operations."""

    @pytest.fixture
    def work_item_data(self) -> CreateWorkItem:
        """Create test work item data."""
        import time
        return CreateWorkItem(
            name=f"Test Work Item {int(time.time())}",
            description_html="<p>Test work item description</p>",
            priority="medium",
        )

    @pytest.fixture
    def work_item(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_data: CreateWorkItem,
    ):
        """Create a test work item and yield it, then delete it."""
        work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
        yield work_item
        try:
            client.work_items.delete(workspace_slug, project.id, work_item.id)
        except Exception:
            pass

    def test_create_work_item(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_data: CreateWorkItem,
    ) -> None:
        """Test creating a work item."""
        work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
        assert work_item is not None
        assert work_item.id is not None
        assert work_item.name == work_item_data.name
        
        # Cleanup
        try:
            client.work_items.delete(workspace_slug, project.id, work_item.id)
        except Exception:
            pass

    def test_retrieve_work_item(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item
    ) -> None:
        """Test retrieving a work item."""
        retrieved = client.work_items.retrieve(workspace_slug, project.id, work_item.id)
        assert retrieved is not None
        assert retrieved.id == work_item.id
        assert hasattr(retrieved, "name")

    def test_update_work_item(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item
    ) -> None:
        """Test updating a work item."""
        update_data = UpdateWorkItem(description_html="<p>Updated description</p>")
        updated = client.work_items.update(workspace_slug, project.id, work_item.id, update_data)
        assert updated is not None
        assert updated.id == work_item.id


class TestWorkItemsSubResources:
    """Test WorkItems sub-resources (comments, links, relations, etc.)."""

    @pytest.fixture
    def work_item(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ):
        """Create a test work item."""
        import time

        from plane.models.work_items import CreateWorkItem
        
        work_item_data = CreateWorkItem(
            name=f"Test Work Item {int(time.time())}",
            description_html="<p>Test work item</p>",
            priority="medium",
        )
        work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
        yield work_item
        try:
            client.work_items.delete(workspace_slug, project.id, work_item.id)
        except Exception:
            pass

    def test_list_comments(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item
    ) -> None:
        """Test listing work item comments."""
        response = client.work_items.comments.list(workspace_slug, project.id, work_item.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_links(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item
    ) -> None:
        """Test listing work item links."""
        response = client.work_items.links.list(workspace_slug, project.id, work_item.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_activities(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item
    ) -> None:
        """Test listing work item activities."""
        response = client.work_items.activities.list(workspace_slug, project.id, work_item.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_attachments(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item
    ) -> None:
        """Test listing work item attachments."""
        response = client.work_items.attachments.list(workspace_slug, project.id, work_item.id)
        assert response is not None
        assert isinstance(response, list)

