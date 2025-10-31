"""Unit tests for Labels API resource (smoke tests with real HTTP requests)."""

import pytest

from plane.client import PlaneClient
from plane.models.labels import CreateLabel, UpdateLabel
from plane.models.projects import Project


class TestLabelsAPI:
    """Test Labels API resource."""

    def test_list_labels(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing labels."""
        response = client.labels.list(workspace_slug, project.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)


class TestLabelsAPICRUD:
    """Test Labels API CRUD operations."""

    @pytest.fixture
    def label_data(self) -> CreateLabel:
        """Create test label data."""
        import time
        return CreateLabel(
            name=f"Test Label {int(time.time())}",
            color="#FF6B6B",
            description="Test label",
        )

    @pytest.fixture
    def label(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        label_data: CreateLabel,
    ):
        """Create a test label and yield it, then delete it."""
        label = client.labels.create(workspace_slug, project.id, label_data)
        yield label
        try:
            client.labels.delete(workspace_slug, project.id, label.id)
        except Exception:
            pass

    def test_create_label(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        label_data: CreateLabel,
    ) -> None:
        """Test creating a label."""
        label = client.labels.create(workspace_slug, project.id, label_data)
        assert label is not None
        assert label.id is not None
        assert label.name == label_data.name
        
        # Cleanup
        try:
            client.labels.delete(workspace_slug, project.id, label.id)
        except Exception:
            pass

    def test_retrieve_label(
        self, client: PlaneClient, workspace_slug: str, project: Project, label
    ) -> None:
        """Test retrieving a label."""
        retrieved = client.labels.retrieve(workspace_slug, project.id, label.id)
        assert retrieved is not None
        assert retrieved.id == label.id
        assert retrieved.name == label.name

    def test_update_label(
        self, client: PlaneClient, workspace_slug: str, project: Project, label
    ) -> None:
        """Test updating a label."""
        update_data = UpdateLabel(description="Updated description")
        updated = client.labels.update(workspace_slug, project.id, label.id, update_data)
        assert updated is not None
        assert updated.id == label.id
        assert updated.description == "Updated description"

