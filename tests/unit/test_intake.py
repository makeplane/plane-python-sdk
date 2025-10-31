"""Unit tests for Intake API resource (smoke tests with real HTTP requests)."""

import pytest

from plane.client import PlaneClient
from plane.models.intake import CreateIntakeWorkItem
from plane.models.projects import Project


class TestIntakeAPI:
    """Test Intake API resource."""

    @pytest.fixture
    def project_with_intake(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> Project:
        """Enable intake view on the shared project."""
        from plane.models.projects import UpdateProject
        
        # Enable intake view on the project
        update_data = UpdateProject(intake_view=True)
        project = client.projects.update(workspace_slug, project.id, update_data)
        return project

    def test_list_intake_work_items(
        self, client: PlaneClient, workspace_slug: str, project_with_intake
    ) -> None:
        """Test listing intake work items."""
        response = client.intake.list(workspace_slug, project_with_intake.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)


class TestIntakeAPICRUD:
    """Test Intake API CRUD operations."""

    @pytest.fixture
    def project_with_intake(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> Project:
        """Enable intake view on the shared project."""
        from plane.models.projects import UpdateProject
        
        # Enable intake view on the project
        update_data = UpdateProject(intake_view=True)
        project = client.projects.update(workspace_slug, project.id, update_data)
        return project

    @pytest.fixture
    def intake_work_item_data(self) -> CreateIntakeWorkItem:
        """Create test intake work item data."""
        import time

        from plane.models.work_items import WorkItemForIntakeRequest
        return CreateIntakeWorkItem(
            issue=WorkItemForIntakeRequest(
                name=f"Test Intake Work Item {int(time.time())}",
                description_html="<p>Test intake work item</p>",
                priority="medium",
            ),
        )

    @pytest.fixture
    def intake_work_item(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_with_intake,
        intake_work_item_data: CreateIntakeWorkItem,
    ):
        """Create a test intake work item and yield it, then delete it."""
        intake_wi = client.intake.create(
            workspace_slug, project_with_intake.id, intake_work_item_data
        )
        yield intake_wi
        try:
            if intake_wi.issue:
                client.intake.delete(workspace_slug, project_with_intake.id, intake_wi.issue)
        except Exception:
            pass

    def test_create_intake_work_item(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_with_intake,
        intake_work_item_data: CreateIntakeWorkItem,
    ) -> None:
        """Test creating an intake work item."""
        intake_wi = client.intake.create(
            workspace_slug, project_with_intake.id, intake_work_item_data
        )
        assert intake_wi is not None
        assert hasattr(intake_wi, "issue")
        
        # Cleanup
        try:
            if hasattr(intake_wi, "issue") and intake_wi.issue:
                client.intake.delete(workspace_slug, project_with_intake.id, intake_wi.issue)
        except Exception:
            pass

    def test_retrieve_intake_work_item(
        self, client: PlaneClient, workspace_slug: str, project_with_intake, intake_work_item
    ) -> None:
        """Test retrieving an intake work item."""
        if hasattr(intake_work_item, "issue") and intake_work_item.issue:
            retrieved = client.intake.retrieve(
                workspace_slug, project_with_intake.id, intake_work_item.issue
            )
            assert retrieved is not None
            assert hasattr(retrieved, "issue")

