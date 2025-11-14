"""Unit tests for Initiatives API resource (smoke tests with real HTTP requests)."""

from datetime import datetime

import pytest

from plane.client import PlaneClient
from plane.models.initiatives import (
    CreateInitiative,
    CreateInitiativeLabel,
    UpdateInitiative,
    UpdateInitiativeLabel,
)
from plane.models.projects import Project


class TestInitiativesAPI:
    """Test Initiatives API resource."""

    def test_list_initiatives(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing initiatives."""
        response = client.initiatives.list(workspace_slug)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_initiatives_with_params(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing initiatives with query parameters."""
        params = {"per_page": 5}
        response = client.initiatives.list(workspace_slug, params=params)
        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) <= 5


class TestInitiativesAPICRUD:
    """Test Initiatives API CRUD operations."""

    @pytest.fixture
    def initiative_data(self) -> CreateInitiative:
        """Create test initiative data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return CreateInitiative(
            name=f"Test Initiative {timestamp}",
            description="Test initiative for smoke tests",
        )

    @pytest.fixture
    def initiative(
        self,
        client: PlaneClient,
        workspace_slug: str,
        initiative_data: CreateInitiative,
    ):
        """Create a test initiative and yield it, then delete it."""
        initiative = client.initiatives.create(workspace_slug, initiative_data)
        yield initiative
        try:
            client.initiatives.delete(workspace_slug, initiative.id)
        except Exception:
            pass

    def test_create_initiative(
        self,
        client: PlaneClient,
        workspace_slug: str,
        initiative_data: CreateInitiative,
    ) -> None:
        """Test creating an initiative."""
        initiative = client.initiatives.create(workspace_slug, initiative_data)
        assert initiative is not None
        assert initiative.id is not None
        assert initiative.name == initiative_data.name

        # Cleanup
        try:
            client.initiatives.delete(workspace_slug, initiative.id)
        except Exception:
            pass

    def test_retrieve_initiative(
        self, client: PlaneClient, workspace_slug: str, initiative
    ) -> None:
        """Test retrieving an initiative."""
        retrieved = client.initiatives.retrieve(workspace_slug, initiative.id)
        assert retrieved is not None
        assert retrieved.id == initiative.id
        assert retrieved.name == initiative.name

    def test_update_initiative(self, client: PlaneClient, workspace_slug: str, initiative) -> None:
        """Test updating an initiative."""
        update_data = UpdateInitiative(description="Updated description")
        updated = client.initiatives.update(workspace_slug, initiative.id, update_data)
        assert updated is not None
        assert updated.id == initiative.id
        assert updated.description == "Updated description"


class TestInitiativeLabelsAPI:
    """Test Initiative Labels API operations."""

    @pytest.fixture
    def initiative(
        self,
        client: PlaneClient,
        workspace_slug: str,
    ):
        """Create a test initiative and yield it, then delete it."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        initiative_data = CreateInitiative(
            name=f"Test Initiative Labels {timestamp}",
            description="Test initiative for labels operations",
        )
        initiative = client.initiatives.create(workspace_slug, initiative_data)
        yield initiative
        try:
            client.initiatives.delete(workspace_slug, initiative.id)
        except Exception:
            pass

    def test_list_labels(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing initiative labels."""
        response = client.initiatives.labels.list(workspace_slug)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_create_and_delete_label(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test creating and deleting an initiative label."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        label_data = CreateInitiativeLabel(
            name=f"Test Label {timestamp}",
            color="#FF0000",
        )
        label = client.initiatives.labels.create(workspace_slug, label_data)
        assert label is not None
        assert label.id is not None
        assert label.name == label_data.name

        # Cleanup
        try:
            client.initiatives.labels.delete(workspace_slug, label.id)
        except Exception:
            pass

    def test_retrieve_label(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test retrieving an initiative label."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        label_data = CreateInitiativeLabel(
            name=f"Test Label {timestamp}",
            color="#00FF00",
        )
        label = client.initiatives.labels.create(workspace_slug, label_data)

        retrieved = client.initiatives.labels.retrieve(workspace_slug, label.id)
        assert retrieved is not None
        assert retrieved.id == label.id
        assert retrieved.name == label.name

        # Cleanup
        try:
            client.initiatives.labels.delete(workspace_slug, label.id)
        except Exception:
            pass

    def test_update_label(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test updating an initiative label."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        label_data = CreateInitiativeLabel(
            name=f"Test Label {timestamp}",
            color="#0000FF",
        )
        label = client.initiatives.labels.create(workspace_slug, label_data)

        update_data = UpdateInitiativeLabel(name="Updated Label Name")
        updated = client.initiatives.labels.update(workspace_slug, label.id, update_data)
        assert updated is not None
        assert updated.id == label.id
        assert updated.name == "Updated Label Name"

        # Cleanup
        try:
            client.initiatives.labels.delete(workspace_slug, label.id)
        except Exception:
            pass

    def test_list_labels_for_initiative(
        self, client: PlaneClient, workspace_slug: str, initiative
    ) -> None:
        """Test listing labels for a specific initiative."""
        response = client.initiatives.labels.list_labels(workspace_slug, initiative.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_add_and_remove_labels(
        self, client: PlaneClient, workspace_slug: str, initiative
    ) -> None:
        """Test adding and removing labels from an initiative."""
        # Create a label first
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        label_data = CreateInitiativeLabel(
            name=f"Test Label {timestamp}",
            color="#FFFF00",
        )
        label = client.initiatives.labels.create(workspace_slug, label_data)

        try:
            # Add label to initiative
            added_labels = client.initiatives.labels.add_labels(
                workspace_slug, initiative.id, [label.id]
            )
            assert isinstance(added_labels, list)

            # Remove label from initiative
            client.initiatives.labels.remove_labels(workspace_slug, initiative.id, [label.id])
        finally:
            # Cleanup
            try:
                client.initiatives.labels.delete(workspace_slug, label.id)
            except Exception:
                pass


class TestInitiativeProjectsAPI:
    """Test Initiative Projects API operations."""

    @pytest.fixture
    def initiative(
        self,
        client: PlaneClient,
        workspace_slug: str,
    ):
        """Create a test initiative and yield it, then delete it."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        initiative_data = CreateInitiative(
            name=f"Test Initiative Projects {timestamp}",
            description="Test initiative for projects operations",
        )
        initiative = client.initiatives.create(workspace_slug, initiative_data)
        yield initiative
        try:
            client.initiatives.delete(workspace_slug, initiative.id)
        except Exception:
            pass

    def test_list_projects(self, client: PlaneClient, workspace_slug: str, initiative) -> None:
        """Test listing projects in an initiative."""
        response = client.initiatives.projects.list(workspace_slug, initiative.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_add_and_remove_projects(
        self, client: PlaneClient, workspace_slug: str, initiative, project: Project
    ) -> None:
        """Test adding and removing projects from an initiative."""
        # Add project
        added_projects = client.initiatives.projects.add(
            workspace_slug, initiative.id, [project.id]
        )
        assert isinstance(added_projects, list)

        # Remove project
        client.initiatives.projects.remove(workspace_slug, initiative.id, [project.id])


class TestInitiativeEpicsAPI:
    """Test Initiative Epics API operations."""

    @pytest.fixture
    def initiative(
        self,
        client: PlaneClient,
        workspace_slug: str,
    ):
        """Create a test initiative and yield it, then delete it."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        initiative_data = CreateInitiative(
            name=f"Test Initiative Epics {timestamp}",
            description="Test initiative for epics operations",
        )
        initiative = client.initiatives.create(workspace_slug, initiative_data)
        yield initiative
        try:
            client.initiatives.delete(workspace_slug, initiative.id)
        except Exception:
            pass

    def test_list_epics(self, client: PlaneClient, workspace_slug: str, initiative) -> None:
        """Test listing epics in an initiative."""
        response = client.initiatives.epics.list(workspace_slug, initiative.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)
