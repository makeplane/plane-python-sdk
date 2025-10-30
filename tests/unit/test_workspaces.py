"""Unit tests for Workspaces API resource (smoke tests with real HTTP requests)."""

from plane.client import PlaneClient


class TestWorkspacesAPI:
    """Test Workspaces API resource."""

    def test_get_members(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test getting workspace members."""
        members = client.workspaces.get_members(workspace_slug)
        assert isinstance(members, list)
        if members:
            member = members[0]
            assert hasattr(member, "id")
            assert hasattr(member, "display_name")

