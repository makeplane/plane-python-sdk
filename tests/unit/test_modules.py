"""Unit tests for Modules API resource (smoke tests with real HTTP requests)."""

from datetime import datetime

import pytest

from plane.client import PlaneClient
from plane.models.enums import ModuleStatus
from plane.models.modules import CreateModule, UpdateModule
from plane.models.projects import Project, ProjectFeature


class TestModulesAPI:
    """Test Modules API resource."""

    def test_list_modules(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing modules."""
        response = client.modules.list(workspace_slug, project.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_archived_modules(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing archived modules."""
        response = client.modules.list_archived(workspace_slug, project.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)


class TestModulesAPICRUD:
    """Test Modules API CRUD operations."""

    @pytest.fixture
    def module_data(self, user_id: str) -> CreateModule:
        """Create test module data."""
        import time
        start_date = datetime.now()
        end_date = datetime.now()
        return CreateModule(
            name=f"Test Module {int(time.time())}",
            description="Test module",
            start_date=start_date.strftime("%Y-%m-%d"),
            target_date=end_date.strftime("%Y-%m-%d"),
            status=ModuleStatus.PLANNED.value,
            lead=user_id,
        )

    @pytest.fixture
    def module(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        module_data: CreateModule,
    ):
        """Create a test module and yield it, then delete it."""
        client.projects.update_features(workspace_slug, project.id, ProjectFeature(modules=True))
        module = client.modules.create(workspace_slug, project.id, module_data)
        yield module
        try:
            client.modules.delete(workspace_slug, project.id, module.id)
        except Exception:
            pass

    def test_create_module(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        module_data: CreateModule,
    ) -> None:
        """Test creating a module."""
        client.projects.update_features(workspace_slug, project.id, ProjectFeature(modules=True))
        module = client.modules.create(workspace_slug, project.id, module_data)
        assert module is not None
        assert module.id is not None
        assert module.name == module_data.name
        
        # Cleanup
        try:
            client.modules.delete(workspace_slug, project.id, module.id)
        except Exception:
            pass

    def test_retrieve_module(
        self, client: PlaneClient, workspace_slug: str, project: Project, module
    ) -> None:
        """Test retrieving a module."""
        retrieved = client.modules.retrieve(workspace_slug, project.id, module.id)
        assert retrieved is not None
        assert retrieved.id == module.id
        assert retrieved.name == module.name

    def test_update_module(
        self, client: PlaneClient, workspace_slug: str, project: Project, module
    ) -> None:
        """Test updating a module."""
        update_data = UpdateModule(description="Updated description")
        updated = client.modules.update(workspace_slug, project.id, module.id, update_data)
        assert updated is not None
        assert updated.id == module.id
        assert updated.description == "Updated description"

    def test_list_work_items(
        self, client: PlaneClient, workspace_slug: str, project: Project, module
    ) -> None:
        """Test listing work items in a module."""
        response = client.modules.list_work_items(workspace_slug, project.id, module.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

