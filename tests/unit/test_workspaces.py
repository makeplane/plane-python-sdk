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

    def test_get_features(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test getting workspace features."""
        features = client.workspaces.get_features(workspace_slug)
        assert features is not None
        assert hasattr(features, "initiatives")
        assert hasattr(features, "project_grouping")
        assert hasattr(features, "teams")
        assert hasattr(features, "customers")
        assert hasattr(features, "wiki")
        assert hasattr(features, "pi")

    def test_update_features(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test updating workspace features."""
        # Get current features first
        features = client.workspaces.get_features(workspace_slug)
        
        # Update features
        features.initiatives = True
        updated = client.workspaces.update_features(workspace_slug, features)
        assert updated is not None
        assert hasattr(updated, "initiatives")
        assert updated.initiatives is True

