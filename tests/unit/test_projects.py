"""Unit tests for Projects API resource (smoke tests with real HTTP requests)."""

from datetime import datetime

import pytest

from plane.client import PlaneClient
from plane.models.projects import (
    CreateProject,
    Project,
    ProjectLite,
    ProjectMember,
    UpdateProject,
)
from plane.models.query_params import (
    LiteListQueryParams,
    MemberListQueryParams,
    MemberQueryParams,
    PaginatedQueryParams,
)


class TestProjectsAPI:
    """Test Projects API resource."""

    def test_list_projects(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing projects."""
        response = client.projects.list(workspace_slug)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_projects_with_params(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing projects with query parameters."""
        params = PaginatedQueryParams(per_page=5)
        response = client.projects.list(workspace_slug, params=params)
        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) <= 5

    def test_list_lite(self, client: PlaneClient, workspace_slug: str) -> None:
        """list_lite returns a paginated envelope of ProjectLite items."""
        response = client.projects.list_lite(workspace_slug)
        assert isinstance(response.results, list)
        assert isinstance(response.total_count, int)
        assert isinstance(response.next_page_results, bool)
        for project in response.results:
            assert isinstance(project, ProjectLite)
            assert project.name is not None
            assert project.identifier is not None

    def test_list_lite_with_params(self, client: PlaneClient, workspace_slug: str) -> None:
        """list_lite honors ordering + cursor pagination params."""
        params = LiteListQueryParams(per_page=5, order_by="-created_at")
        response = client.projects.list_lite(workspace_slug, params=params)
        assert isinstance(response.results, list)
        assert len(response.results) <= 5


class TestProjectsAPICRUD:
    """Test Projects API CRUD operations."""

    @pytest.fixture
    def project_data(self) -> CreateProject:
        """Create test project data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return CreateProject(
            name=f"Test Project {timestamp}",
            description="Test project for smoke tests",
            identifier=f"TP{timestamp[-6:]}",
        )

    @pytest.fixture
    def project(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_data: CreateProject,
    ) -> Project:
        """Create a test project and yield it, then delete it."""
        project = client.projects.create(workspace_slug, project_data)
        yield project
        try:
            client.projects.delete(workspace_slug, project.id)
        except Exception:
            pass  # Cleanup failed, but don't fail the test

    def test_create_project(
        self, client: PlaneClient, workspace_slug: str, project_data: CreateProject
    ) -> None:
        """Test creating a project."""
        project = client.projects.create(workspace_slug, project_data)
        assert project is not None
        assert project.id is not None
        assert project.name == project_data.name

        # Cleanup
        try:
            client.projects.delete(workspace_slug, project.id)
        except Exception:
            pass

    def test_retrieve_project(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test retrieving a project."""
        retrieved = client.projects.retrieve(workspace_slug, project.id)
        assert retrieved is not None
        assert retrieved.id == project.id
        assert retrieved.name == project.name

    def test_update_project(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test updating a project."""
        update_data = UpdateProject(description="Updated description")
        updated = client.projects.update(workspace_slug, project.id, update_data)
        assert updated is not None
        assert updated.id == project.id
        assert updated.description == "Updated description"

    def test_get_members(self, client: PlaneClient, workspace_slug: str, project: Project) -> None:
        """Test getting project members returns ProjectMember objects with role fields."""
        members = client.projects.get_members(workspace_slug, project.id)
        assert isinstance(members, list)
        for member in members:
            assert isinstance(member, ProjectMember)
            # role and role_slug should be present (may be None only on very old servers)
            assert hasattr(member, "role")
            assert hasattr(member, "role_slug")
            assert hasattr(member, "id")
            assert hasattr(member, "email")

    def test_get_members_typed_filter(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """get_members accepts a typed MemberQueryParams and filters by is_active."""
        members = client.projects.get_members(
            workspace_slug, project.id, params=MemberQueryParams(is_active=True)
        )
        assert isinstance(members, list)
        for member in members:
            assert isinstance(member, ProjectMember)

    def test_get_members_dict_filter_backcompat(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """get_members accepts a raw mapping; bool values are normalized to true/false."""
        members = client.projects.get_members(
            workspace_slug, project.id, params={"is_active": True, "role_slug": "admin"}
        )
        assert isinstance(members, list)
        for member in members:
            assert isinstance(member, ProjectMember)

    def test_get_members_lite_paginated(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """get_members_lite returns a paginated envelope of ProjectMember items."""
        paginated_members = client.projects.get_members_lite(
            workspace_slug, project.id, params=MemberListQueryParams(per_page=100)
        )
        assert isinstance(paginated_members.results, list)
        assert isinstance(paginated_members.total_count, int)
        assert isinstance(paginated_members.next_page_results, bool)
        for member in paginated_members.results:
            assert isinstance(member, ProjectMember)

    def test_get_features(self, client: PlaneClient, workspace_slug: str, project: Project) -> None:
        """Test getting project features."""
        features = client.projects.get_features(workspace_slug, project.id)
        assert features is not None
        assert hasattr(features, "cycles")
        assert hasattr(features, "modules")
        assert hasattr(features, "views")
        assert hasattr(features, "pages")
        assert hasattr(features, "intakes")
        assert hasattr(features, "epics")
        assert hasattr(features, "work_item_types")
        assert hasattr(features, "workflows")
        assert hasattr(features, "parallel_cycles")
        assert hasattr(features, "project_updates")

    def test_update_features(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test updating project features."""
        # Get current features first
        features = client.projects.get_features(workspace_slug, project.id)

        # Update features
        features.cycles = True
        updated = client.projects.update_features(workspace_slug, project.id, features)
        assert updated is not None
        assert updated.cycles is True
        assert hasattr(updated, "cycles")
        assert hasattr(updated, "modules")
        assert hasattr(updated, "views")
        assert hasattr(updated, "pages")
        assert hasattr(updated, "intakes")
        assert hasattr(updated, "epics")
        assert hasattr(updated, "work_item_types")
        assert hasattr(updated, "workflows")
        assert hasattr(updated, "parallel_cycles")
        assert hasattr(updated, "project_updates")
