"""Unit tests for Estimates API resource (smoke tests with real HTTP requests)."""

import time

import pytest
from pydantic import ValidationError

from plane.client import PlaneClient
from plane.models.estimates import (
    CreateEstimate,
    CreateEstimatePoint,
    Estimate,
    EstimatePoint,
    UpdateEstimate,
    UpdateEstimatePoint,
)
from plane.models.projects import Project


class TestEstimatesAPI:
    """Test Estimates API basic operations."""

    def test_create_and_retrieve_estimate(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test creating and retrieving an estimate."""
        data = CreateEstimate(
            name=f"Test Estimate {int(time.time())}",
            description="Test estimate description",
            type="points",
        )
        estimate = client.estimates.create(workspace_slug, project.id, data)
        assert estimate is not None
        assert isinstance(estimate, Estimate)
        assert estimate.id is not None
        assert estimate.name == data.name
        assert estimate.description == data.description

        # Retrieve
        retrieved = client.estimates.retrieve(workspace_slug, project.id)
        assert retrieved is not None
        assert isinstance(retrieved, Estimate)
        assert retrieved.id == estimate.id
        assert retrieved.name == estimate.name

        # Cleanup
        try:
            client.estimates.delete(workspace_slug, project.id)
        except Exception:
            pass


class TestEstimatesAPICRUD:
    """Test Estimates API CRUD operations with fixture-based lifecycle."""

    @pytest.fixture
    def estimate_data(self) -> CreateEstimate:
        """Create test estimate data."""
        return CreateEstimate(
            name=f"Test Estimate {int(time.time())}",
            description="Estimate for testing",
            type="points",
        )

    @pytest.fixture
    def estimate(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        estimate_data: CreateEstimate,
    ):
        """Create a test estimate and yield it, then delete it."""
        estimate = client.estimates.create(workspace_slug, project.id, estimate_data)
        yield estimate
        try:
            client.estimates.delete(workspace_slug, project.id)
        except Exception:
            pass

    def test_update_estimate(
        self, client: PlaneClient, workspace_slug: str, project: Project, estimate
    ) -> None:
        """Test updating an estimate."""
        update_data = UpdateEstimate(name="Updated Estimate Name")
        updated = client.estimates.update(workspace_slug, project.id, update_data)
        assert updated is not None
        assert isinstance(updated, Estimate)
        assert updated.id == estimate.id
        assert updated.name == "Updated Estimate Name"

    def test_delete_estimate(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        estimate_data: CreateEstimate,
    ) -> None:
        """Test deleting an estimate."""
        estimate = client.estimates.create(workspace_slug, project.id, estimate_data)
        assert estimate.id is not None
        result = client.estimates.delete(workspace_slug, project.id)
        assert result is None


class TestEstimatePointsAPI:
    """Test Estimate Points API operations."""

    @pytest.fixture
    def estimate(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
    ):
        """Create a test estimate for points testing."""
        data = CreateEstimate(
            name=f"Points Test Estimate {int(time.time())}",
            type="points",
        )
        estimate = client.estimates.create(workspace_slug, project.id, data)
        yield estimate
        try:
            client.estimates.delete(workspace_slug, project.id)
        except Exception:
            pass

    def test_create_and_list_points(
        self, client: PlaneClient, workspace_slug: str, project: Project, estimate
    ) -> None:
        """Test creating and listing estimate points."""
        points_data = [
            CreateEstimatePoint(value="1", key=0, description="Tiny"),
            CreateEstimatePoint(value="2", key=1, description="Small"),
            CreateEstimatePoint(value="3", key=2, description="Medium"),
        ]
        created_points = client.estimates.create_points(
            workspace_slug, project.id, estimate.id, points_data
        )
        assert created_points is not None
        assert isinstance(created_points, list)
        assert len(created_points) == 3
        for point in created_points:
            assert isinstance(point, EstimatePoint)
            assert point.id is not None
            assert point.value in ["1", "2", "3"]

        # List points
        listed_points = client.estimates.list_points(
            workspace_slug, project.id, estimate.id
        )
        assert listed_points is not None
        assert isinstance(listed_points, list)
        assert len(listed_points) >= 3

    def test_update_point(
        self, client: PlaneClient, workspace_slug: str, project: Project, estimate
    ) -> None:
        """Test updating an estimate point."""
        # Create a point first
        points_data = [CreateEstimatePoint(value="5", key=0)]
        created = client.estimates.create_points(
            workspace_slug, project.id, estimate.id, points_data
        )
        assert len(created) == 1
        point_id = created[0].id

        # Update the point
        update_data = UpdateEstimatePoint(value="8", description="Updated")
        updated = client.estimates.update_point(
            workspace_slug, project.id, estimate.id, point_id, update_data
        )
        assert updated is not None
        assert isinstance(updated, EstimatePoint)
        assert updated.id == point_id
        assert updated.value == "8"

    def test_delete_point(
        self, client: PlaneClient, workspace_slug: str, project: Project, estimate
    ) -> None:
        """Test deleting an estimate point."""
        # Create a point first
        points_data = [CreateEstimatePoint(value="13", key=0)]
        created = client.estimates.create_points(
            workspace_slug, project.id, estimate.id, points_data
        )
        assert len(created) == 1
        point_id = created[0].id

        # Delete it
        result = client.estimates.delete_point(
            workspace_slug, project.id, estimate.id, point_id
        )
        assert result is None


class TestEstimateModels:
    """Test Pydantic model validation for estimates."""

    def test_create_estimate_rejects_extra_fields(self) -> None:
        """Test that CreateEstimate ignores extra fields."""
        data = CreateEstimate(name="Test", unknown_field="value")
        assert not hasattr(data, "unknown_field")

    def test_estimate_allows_extra_fields(self) -> None:
        """Test that Estimate response model accepts unknown fields."""
        data = Estimate.model_validate(
            {"name": "Test", "some_new_api_field": "future_value"}
        )
        assert data.name == "Test"
        assert data.some_new_api_field == "future_value"

    def test_create_estimate_point_value_max_length(self) -> None:
        """Test that CreateEstimatePoint enforces value max_length=20."""
        with pytest.raises(ValidationError):
            CreateEstimatePoint(value="x" * 21)

    def test_create_estimate_point_valid(self) -> None:
        """Test creating a valid estimate point model."""
        point = CreateEstimatePoint(value="5", key=2, description="Medium")
        assert point.value == "5"
        assert point.key == 2
        assert point.description == "Medium"

    def test_update_estimate_all_optional(self) -> None:
        """Test that all UpdateEstimate fields are optional."""
        data = UpdateEstimate()
        dumped = data.model_dump(exclude_none=True)
        assert dumped == {}

    def test_update_estimate_point_all_optional(self) -> None:
        """Test that all UpdateEstimatePoint fields are optional."""
        data = UpdateEstimatePoint()
        dumped = data.model_dump(exclude_none=True)
        assert dumped == {}
