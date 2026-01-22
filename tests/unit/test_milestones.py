"""Unit tests for Milestones API resource (smoke tests with real HTTP requests)."""

from datetime import datetime

import pytest

from plane.client import PlaneClient
from plane.models.milestones import CreateMilestone, UpdateMilestone
from plane.models.projects import Project, ProjectFeature


class TestMilestonesAPI:
    """Test Milestones API resource."""

    def test_list_milestones(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing milestones."""
        response = client.milestones.list(workspace_slug, project.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)


class TestMilestonesAPICRUD:
    """Test Milestones API CRUD operations."""

    @pytest.fixture
    def milestone_data(self) -> CreateMilestone:
        """Create test milestone data."""
        import time
        end_date = datetime.now()
        return CreateMilestone(
            title=f"Test Milestone {int(time.time())}",
            target_date=end_date.strftime("%Y-%m-%d"),
        )

    @pytest.fixture
    def milestone(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        milestone_data: CreateMilestone,
    ):
        """Create a test milestone and yield it, then delete it."""
        client.projects.update_features(workspace_slug, project.id, ProjectFeature(modules=True))
        milestone = client.milestones.create(workspace_slug, project.id, milestone_data)
        yield milestone
        try:
            client.milestones.delete(workspace_slug, project.id, milestone.id)
        except Exception:
            pass

    def test_create_milestone(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        milestone_data: CreateMilestone,
    ) -> None:
        """Test creating a milestone."""
        client.projects.update_features(workspace_slug, project.id, ProjectFeature(modules=True))
        milestone = client.milestones.create(workspace_slug, project.id, milestone_data)
        assert milestone is not None
        assert milestone.id is not None
        assert milestone.title == milestone_data.title

        # Cleanup
        try:
            client.milestones.delete(workspace_slug, project.id, milestone.id)
        except Exception:
            pass

    def test_retrieve_milestone(
        self, client: PlaneClient, workspace_slug: str, project: Project, milestone
    ) -> None:
        """Test retrieving a milestone."""
        retrieved = client.milestones.retrieve(workspace_slug, project.id, milestone.id)
        assert retrieved is not None
        assert retrieved.id == milestone.id
        assert retrieved.title == milestone.title

    def test_update_milestone(
        self, client: PlaneClient, workspace_slug: str, project: Project, milestone
    ) -> None:
        """Test updating a milestone."""
        update_data = UpdateMilestone(title="Updated Milestone Title")
        updated = client.milestones.update(workspace_slug, project.id, milestone.id, update_data)
        assert updated is not None
        assert updated.id == milestone.id
        assert updated.title == "Updated Milestone Title"

    def test_list_work_items(
        self, client: PlaneClient, workspace_slug: str, project: Project, milestone
    ) -> None:
        """Test listing work items in a milestone."""
        response = client.milestones.list_work_items(workspace_slug, project.id, milestone.id)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)
