"""Unit tests for WorkItemTypes API resource (smoke tests with real HTTP requests)."""

import pytest

from plane.client import PlaneClient
from plane.models.projects import Project
from plane.models.work_item_types import CreateWorkItemType, UpdateWorkItemType


class TestWorkItemTypesAPI:
    """Test WorkItemTypes API resource."""

    def test_list_work_item_types(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing work item types."""
        work_item_types = client.work_item_types.list(workspace_slug, project.id)
        assert isinstance(work_item_types, list)
        if work_item_types:
            work_item_type = work_item_types[0]
            assert hasattr(work_item_type, "id")
            assert hasattr(work_item_type, "name")


class TestWorkItemTypesAPICRUD:
    """Test WorkItemTypes API CRUD operations."""

    @pytest.fixture
    def work_item_type_data(self) -> CreateWorkItemType:
        """Create test work item type data."""
        import time
        return CreateWorkItemType(
            name=f"Test Type {int(time.time())}",
            description="Test work item type",
            is_epic=False,
            is_active=True,
        )

    @pytest.fixture
    def work_item_type(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type_data: CreateWorkItemType,
    ):
        """Create a test work item type and yield it, then delete it."""
        work_item_type = client.work_item_types.create(
            workspace_slug, project.id, work_item_type_data
        )
        yield work_item_type
        try:
            client.work_item_types.delete(workspace_slug, project.id, work_item_type.id)
        except Exception:
            pass

    def test_create_work_item_type(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type_data: CreateWorkItemType,
    ) -> None:
        """Test creating a work item type."""
        work_item_type = client.work_item_types.create(
            workspace_slug, project.id, work_item_type_data
        )
        assert work_item_type is not None
        assert work_item_type.id is not None
        assert work_item_type.name == work_item_type_data.name
        
        # Cleanup
        try:
            client.work_item_types.delete(workspace_slug, project.id, work_item_type.id)
        except Exception:
            pass

    def test_retrieve_work_item_type(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test retrieving a work item type."""
        retrieved = client.work_item_types.retrieve(
            workspace_slug, project.id, work_item_type.id
        )
        assert retrieved is not None
        assert retrieved.id == work_item_type.id
        assert retrieved.name == work_item_type.name

    def test_update_work_item_type(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item_type
    ) -> None:
        """Test updating a work item type."""
        update_data = UpdateWorkItemType(description="Updated description")
        updated = client.work_item_types.update(
            workspace_slug, project.id, work_item_type.id, update_data
        )
        assert updated is not None
        assert updated.id == work_item_type.id
        assert updated.description == "Updated description"

