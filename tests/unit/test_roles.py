"""Unit tests for Roles API resource (smoke tests with real HTTP requests)."""

from plane.client import PlaneClient
from plane.models.roles import Role


class TestRolesAPI:
    """Test Roles API resource."""

    def test_list_roles(self, client: PlaneClient, workspace_slug: str) -> None:
        """Listing roles returns a paginated envelope of Role objects."""
        page = client.roles.list(workspace_slug)
        assert isinstance(page.results, list)
        assert isinstance(page.next_page_results, bool)
        for role in page.results:
            assert isinstance(role, Role)
            assert role.slug is not None
            assert role.namespace in ("workspace", "project")

    def test_list_roles_namespace_workspace(self, client: PlaneClient, workspace_slug: str) -> None:
        """Filtering by namespace=workspace returns only workspace-level roles."""
        page = client.roles.list(workspace_slug, namespace="workspace")
        assert isinstance(page.results, list)
        for role in page.results:
            assert role.namespace == "workspace"

    def test_list_roles_namespace_project(self, client: PlaneClient, workspace_slug: str) -> None:
        """Filtering by namespace=project returns only project-level roles."""
        page = client.roles.list(workspace_slug, namespace="project")
        assert isinstance(page.results, list)
        for role in page.results:
            assert role.namespace == "project"

    def test_retrieve_role(self, client: PlaneClient, workspace_slug: str) -> None:
        """Retrieving a role by id returns a single Role matching the listed one."""
        page = client.roles.list(workspace_slug, per_page=1)
        if not page.results:
            return
        listed = page.results[0]
        role_id = getattr(listed, "id", None)
        if role_id is None:
            return
        retrieved = client.roles.retrieve(workspace_slug, role_id)
        assert isinstance(retrieved, Role)
        assert retrieved.slug == listed.slug
        assert retrieved.namespace == listed.namespace
