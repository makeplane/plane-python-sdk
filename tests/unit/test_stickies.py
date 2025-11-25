"""Unit tests for Stickies API resource (smoke tests with real HTTP requests)."""

from datetime import datetime

import pytest

from plane.client import PlaneClient
from plane.models.stickies import CreateSticky, UpdateSticky


class TestStickiesAPI:
    """Test Stickies API resource."""

    def test_list_stickies(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing stickies."""
        response = client.stickies.list(workspace_slug)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_stickies_with_params(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing stickies with query parameters."""
        params = {"per_page": 5}
        response = client.stickies.list(workspace_slug, params=params)
        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) <= 5


class TestStickiesAPICRUD:
    """Test Stickies API CRUD operations."""

    @pytest.fixture
    def sticky_data(self) -> CreateSticky:
        """Create test sticky data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return CreateSticky(
            name=f"Test Sticky {timestamp}",
            description_html="<p>Test sticky for smoke tests</p>",
        )

    @pytest.fixture
    def sticky(
        self,
        client: PlaneClient,
        workspace_slug: str,
        sticky_data: CreateSticky,
    ):
        """Create a test sticky and yield it, then delete it."""
        sticky = client.stickies.create(workspace_slug, sticky_data)
        yield sticky
        try:
            client.stickies.delete(workspace_slug, sticky.id)
        except Exception:
            pass

    def test_create_sticky(
        self, client: PlaneClient, workspace_slug: str, sticky_data: CreateSticky
    ) -> None:
        """Test creating a sticky."""
        sticky = client.stickies.create(workspace_slug, sticky_data)
        assert sticky is not None
        assert sticky.id is not None
        assert sticky.name == sticky_data.name

        # Cleanup
        try:
            client.stickies.delete(workspace_slug, sticky.id)
        except Exception:
            pass

    def test_retrieve_sticky(
        self, client: PlaneClient, workspace_slug: str, sticky
    ) -> None:
        """Test retrieving a sticky."""
        retrieved = client.stickies.retrieve(workspace_slug, sticky.id)
        assert retrieved is not None
        assert retrieved.id == sticky.id
        assert retrieved.name == sticky.name

    def test_update_sticky(
        self, client: PlaneClient, workspace_slug: str, sticky
    ) -> None:
        """Test updating a sticky."""
        update_data = UpdateSticky(name="Updated Sticky Name")
        updated = client.stickies.update(workspace_slug, sticky.id, update_data)
        assert updated is not None
        assert updated.id == sticky.id
        assert updated.name == "Updated Sticky Name"


