"""Unit tests for States API resource (smoke tests with real HTTP requests)."""

import pytest

from plane.client import PlaneClient
from plane.models.projects import Project
from plane.models.states import CreateState, UpdateState


class TestStatesAPI:
    """Test States API resource."""

    def test_list_states(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing states."""
        response = client.states.list(workspace_slug, project.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)


class TestStatesAPICRUD:
    """Test States API CRUD operations."""

    @pytest.fixture
    def state_data(self) -> CreateState:
        """Create test state data."""
        import time
        return CreateState(
            name=f"Test State {int(time.time())}",
            color="#4ECDC4",
            description="Test state",
        )

    @pytest.fixture
    def state(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        state_data: CreateState,
    ):
        """Create a test state and yield it, then delete it."""
        state = client.states.create(workspace_slug, project.id, state_data)
        yield state
        try:
            client.states.delete(workspace_slug, project.id, state.id)
        except Exception:
            pass

    def test_create_state(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        state_data: CreateState,
    ) -> None:
        """Test creating a state."""
        state = client.states.create(workspace_slug, project.id, state_data)
        assert state is not None
        assert state.id is not None
        assert state.name == state_data.name
        
        # Cleanup
        try:
            client.states.delete(workspace_slug, project.id, state.id)
        except Exception:
            pass

    def test_retrieve_state(
        self, client: PlaneClient, workspace_slug: str, project: Project, state
    ) -> None:
        """Test retrieving a state."""
        retrieved = client.states.retrieve(workspace_slug, project.id, state.id)
        assert retrieved is not None
        assert retrieved.id == state.id
        assert retrieved.name == state.name

    def test_update_state(
        self, client: PlaneClient, workspace_slug: str, project: Project, state
    ) -> None:
        """Test updating a state."""
        update_data = UpdateState(description="Updated description")
        updated = client.states.update(workspace_slug, project.id, state.id, update_data)
        assert updated is not None
        assert updated.id == state.id
        assert updated.description == "Updated description"

