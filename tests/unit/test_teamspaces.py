"""Unit tests for Teamspaces API resource (smoke tests with real HTTP requests)."""

from datetime import datetime

import pytest

from plane.client import PlaneClient
from plane.models.projects import Project
from plane.models.teamspaces import CreateTeamspace, UpdateTeamspace


class TestTeamspacesAPI:
    """Test Teamspaces API resource."""

    def test_list_teamspaces(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing teamspaces."""
        response = client.teamspaces.list(workspace_slug)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_teamspaces_with_params(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing teamspaces with query parameters."""
        params = {"per_page": 5}
        response = client.teamspaces.list(workspace_slug, params=params)
        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) <= 5


class TestTeamspacesAPICRUD:
    """Test Teamspaces API CRUD operations."""

    @pytest.fixture
    def teamspace_data(self) -> CreateTeamspace:
        """Create test teamspace data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return CreateTeamspace(
            name=f"Test Teamspace {timestamp}",
            description_html="<p>Test teamspace for smoke tests</p>",
        )

    @pytest.fixture
    def teamspace(
        self,
        client: PlaneClient,
        workspace_slug: str,
        teamspace_data: CreateTeamspace,
    ):
        """Create a test teamspace and yield it, then delete it."""
        teamspace = client.teamspaces.create(workspace_slug, teamspace_data)
        yield teamspace
        try:
            client.teamspaces.delete(workspace_slug, teamspace.id)
        except Exception:
            pass

    def test_create_teamspace(
        self, client: PlaneClient, workspace_slug: str, teamspace_data: CreateTeamspace
    ) -> None:
        """Test creating a teamspace."""
        teamspace = client.teamspaces.create(workspace_slug, teamspace_data)
        assert teamspace is not None
        assert teamspace.id is not None
        assert teamspace.name == teamspace_data.name

        # Cleanup
        try:
            client.teamspaces.delete(workspace_slug, teamspace.id)
        except Exception:
            pass

    def test_retrieve_teamspace(
        self, client: PlaneClient, workspace_slug: str, teamspace
    ) -> None:
        """Test retrieving a teamspace."""
        retrieved = client.teamspaces.retrieve(workspace_slug, teamspace.id)
        assert retrieved is not None
        assert retrieved.id == teamspace.id
        assert retrieved.name == teamspace.name

    def test_update_teamspace(
        self, client: PlaneClient, workspace_slug: str, teamspace
    ) -> None:
        """Test updating a teamspace."""
        update_data = UpdateTeamspace(name="Updated name")
        updated = client.teamspaces.update(workspace_slug, teamspace.id, update_data)
        assert updated is not None
        assert updated.id == teamspace.id
        assert updated.name == "Updated name"
    
    def test_list_teamspaces_with_params(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing teamspaces with query parameters."""
        params = {"per_page": 5}
        response = client.teamspaces.list(workspace_slug, params=params)
        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) <= 5
        assert hasattr(response.results[0], "id")
        assert hasattr(response.results[0], "name")
        assert hasattr(response.results[0], "description_html")
        assert hasattr(response.results[0], "description_stripped")
        assert hasattr(response.results[0], "description_binary")
        assert hasattr(response.results[0], "logo_props")
        assert hasattr(response.results[0], "lead")
        assert hasattr(response.results[0], "workspace")


class TestTeamspaceMembersAPI:
    """Test Teamspace Members API operations."""

    @pytest.fixture
    def teamspace(
        self,
        client: PlaneClient,
        workspace_slug: str,
    ):
        """Create a test teamspace and yield it, then delete it."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        teamspace_data = CreateTeamspace(
            name=f"Test Teamspace Members {timestamp}",
            description_html="<p>Test teamspace for members operations</p>",
        )
        teamspace = client.teamspaces.create(workspace_slug, teamspace_data)
        yield teamspace
        try:
            client.teamspaces.delete(workspace_slug, teamspace.id)
        except Exception:
            pass

    def test_list_members(
        self, client: PlaneClient, workspace_slug: str, teamspace
    ) -> None:
        """Test listing members in a teamspace."""
        response = client.teamspaces.members.list(workspace_slug, teamspace.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_add_and_remove_members(
        self, client: PlaneClient, workspace_slug: str, teamspace, user_id: str
    ) -> None:
        """Test adding and removing members from a teamspace."""
        # Add member
        added_members = client.teamspaces.members.add(
            workspace_slug, teamspace.id, [user_id]
        )
        assert isinstance(added_members, list)

        # Remove member
        client.teamspaces.members.remove(workspace_slug, teamspace.id, [user_id])


class TestTeamspaceProjectsAPI:
    """Test Teamspace Projects API operations."""

    @pytest.fixture
    def teamspace(
        self,
        client: PlaneClient,
        workspace_slug: str,
    ):
        """Create a test teamspace and yield it, then delete it."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        teamspace_data = CreateTeamspace(
            name=f"Test Teamspace Projects {timestamp}",
            description_html="<p>Test teamspace for projects operations</p>",
        )
        teamspace = client.teamspaces.create(workspace_slug, teamspace_data)
        yield teamspace
        try:
            client.teamspaces.delete(workspace_slug, teamspace.id)
        except Exception:
            pass

    def test_list_projects(
        self, client: PlaneClient, workspace_slug: str, teamspace
    ) -> None:
        """Test listing projects in a teamspace."""
        response = client.teamspaces.projects.list(workspace_slug, teamspace.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_add_and_remove_projects(
        self, client: PlaneClient, workspace_slug: str, teamspace, project: Project
    ) -> None:
        """Test adding and removing projects from a teamspace."""
        # Add project
        added_projects = client.teamspaces.projects.add(
            workspace_slug, teamspace.id, [project.id]
        )
        assert isinstance(added_projects, list)

        # Remove project
        client.teamspaces.projects.remove(workspace_slug, teamspace.id, [project.id])


