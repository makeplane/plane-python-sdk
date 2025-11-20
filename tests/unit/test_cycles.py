"""Unit tests for Cycles API resource (smoke tests with real HTTP requests)."""

from datetime import datetime

import pytest

from plane.client import PlaneClient
from plane.models.cycles import CreateCycle, UpdateCycle
from plane.models.projects import Project, ProjectFeature


class TestCyclesAPI:
    """Test Cycles API resource."""

    def test_list_cycles(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing cycles."""
        response = client.cycles.list(workspace_slug, project.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_archived_cycles(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing archived cycles."""
        response = client.cycles.list_archived(workspace_slug, project.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)


class TestCyclesAPICRUD:
    """Test Cycles API CRUD operations."""

    @pytest.fixture
    def cycle_data(self, project: Project, user_id: str) -> CreateCycle:
        """Create test cycle data."""
        import time
        start_date = datetime.now()
        end_date = datetime.now()
        return CreateCycle(
            name=f"Test Cycle {int(time.time())}",
            description="Test cycle",
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            owned_by=user_id,
            project_id=project.id,
        )

    @pytest.fixture
    def cycle(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        cycle_data: CreateCycle,
    ):
        """Create a test cycle and yield it, then delete it."""
        client.projects.update_features(workspace_slug, project.id, ProjectFeature(cycles=True))
        cycle = client.cycles.create(workspace_slug, project.id, cycle_data)
        yield cycle
        try:
            client.cycles.delete(workspace_slug, project.id, cycle.id)
        except Exception:
            pass

    def test_create_cycle(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        cycle_data: CreateCycle,
    ) -> None:
        """Test creating a cycle."""
        client.projects.update_features(workspace_slug, project.id, ProjectFeature(cycles=True))
        cycle = client.cycles.create(workspace_slug, project.id, cycle_data)
        assert cycle is not None
        assert cycle.id is not None
        assert cycle.name == cycle_data.name
        
        # Cleanup
        try:
            client.cycles.delete(workspace_slug, project.id, cycle.id)
        except Exception:
            pass

    def test_retrieve_cycle(
        self, client: PlaneClient, workspace_slug: str, project: Project, cycle
    ) -> None:
        """Test retrieving a cycle."""
        retrieved = client.cycles.retrieve(workspace_slug, project.id, cycle.id)
        assert retrieved is not None
        assert retrieved.id == cycle.id
        assert retrieved.name == cycle.name

    def test_update_cycle(
        self, client: PlaneClient, workspace_slug: str, project: Project, cycle
    ) -> None:
        """Test updating a cycle."""
        update_data = UpdateCycle(description="Updated description")
        updated = client.cycles.update(workspace_slug, project.id, cycle.id, update_data)
        assert updated is not None
        assert updated.id == cycle.id
        assert updated.description == "Updated description"

    def test_list_work_items(
        self, client: PlaneClient, workspace_slug: str, project: Project, cycle
    ) -> None:
        """Test listing work items in a cycle."""
        response = client.cycles.list_work_items(workspace_slug, project.id, cycle.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

