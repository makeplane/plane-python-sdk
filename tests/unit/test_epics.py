"""Unit tests for Epics API resource (smoke tests with real HTTP requests)."""

from datetime import datetime

import pytest

from plane.client import PlaneClient
from plane.models.epics import AddEpicWorkItems, CreateEpic, Epic, UpdateEpic
from plane.models.projects import Project, ProjectFeature
from plane.models.query_params import PaginatedQueryParams
from plane.models.work_items import CreateWorkItem


class TestEpicsAPI:
    """Test Epics API resource."""

    def test_list_epics(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing epics."""
        response = client.epics.list(workspace_slug, project.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_epics_with_params(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing epics with query parameters."""
        params = PaginatedQueryParams(per_page=10)
        response = client.epics.list(workspace_slug, project.id, params=params)
        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) <= 10


class TestEpicsAPICRUD:
    """Test Epics API CRUD operations."""

    @pytest.fixture
    def epic(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> Epic:
        """Create a test epic and yield it, then delete it."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        data = CreateEpic(name=f"Test Epic {timestamp}", priority="high")
        epic = client.epics.create(workspace_slug, project.id, data)
        yield epic
        try:
            client.epics.delete(workspace_slug, project.id, epic.id)
        except Exception:
            pass

    def test_create_epic(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test creating an epic."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        data = CreateEpic(name=f"Test Epic {timestamp}")
        client.projects.update_features(workspace_slug, project.id, ProjectFeature(epics=True))
        epic = client.epics.create(workspace_slug, project.id, data)
        assert epic is not None
        assert epic.id is not None
        assert epic.name == data.name

    def test_retrieve_epic(
        self, client: PlaneClient, workspace_slug: str, project: Project, epic: Epic
    ) -> None:
        """Test retrieving an epic."""
        retrieved = client.epics.retrieve(workspace_slug, project.id, epic.id)
        assert retrieved is not None
        assert retrieved.id == epic.id
        assert retrieved.name == epic.name

    def test_update_epic(
        self, client: PlaneClient, workspace_slug: str, project: Project, epic: Epic
    ) -> None:
        """Test updating an epic."""
        update_data = UpdateEpic(name="Updated Epic Name")
        updated = client.epics.update(workspace_slug, project.id, epic.id, update_data)
        assert updated is not None
        assert updated.id == epic.id
        assert updated.name == "Updated Epic Name"

    def test_list_epic_issues(
        self, client: PlaneClient, workspace_slug: str, project: Project, epic: Epic
    ) -> None:
        """Test listing work items under an epic."""
        response = client.epics.list_issues(workspace_slug, project.id, epic.id)
        assert response is not None
        assert hasattr(response, "results")
        assert isinstance(response.results, list)

    def test_add_issues_to_epic(
        self, client: PlaneClient, workspace_slug: str, project: Project, epic: Epic
    ) -> None:
        """Test adding work items to an epic."""
        work_item = client.work_items.create(
            workspace_slug,
            project.id,
            CreateWorkItem(name="Test Work Item for Epic"),
        )
        try:
            data = AddEpicWorkItems(work_item_ids=[work_item.id])
            added = client.epics.add_issues(workspace_slug, project.id, epic.id, data)
            assert added is not None
            assert isinstance(added, list)
            assert len(added) == 1
            assert added[0].parent == epic.id
        finally:
            try:
                client.work_items.delete(workspace_slug, project.id, work_item.id)
            except Exception:
                pass
