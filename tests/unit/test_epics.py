"""Unit tests for Epics API resource (smoke tests with real HTTP requests)."""

from plane.client import PlaneClient
from plane.models.projects import Project
from plane.models.query_params import PaginatedQueryParams


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

