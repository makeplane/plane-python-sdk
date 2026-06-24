"""Unit tests for Workspaces API resource (smoke tests with real HTTP requests)."""

from plane.client import PlaneClient
from plane.models.query_params import MemberListQueryParams, MemberQueryParams
from plane.models.workspaces import WorkspaceMember


class TestWorkspacesAPI:
    """Test Workspaces API resource."""

    def test_get_members(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test getting workspace members returns WorkspaceMember objects with role fields."""
        members = client.workspaces.get_members(workspace_slug)
        assert isinstance(members, list)
        for member in members:
            assert isinstance(member, WorkspaceMember)
            assert hasattr(member, "id")
            assert hasattr(member, "display_name")
            assert hasattr(member, "role")
            assert hasattr(member, "role_slug")

    def test_get_members_filter_is_active(self, client: PlaneClient, workspace_slug: str) -> None:
        """Filtering by is_active should only return active members."""
        members = client.workspaces.get_members(
            workspace_slug, params=MemberQueryParams(is_active=True)
        )
        assert isinstance(members, list)
        for member in members:
            assert isinstance(member, WorkspaceMember)
            # is_active may be omitted by older servers; when present it must match
            if member.is_active is not None:
                assert member.is_active is True

    def test_get_members_filter_display_name(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Filtering by a substring of an existing member's display name returns that member."""
        all_members = client.workspaces.get_members(workspace_slug)
        named = next((m for m in all_members if m.display_name), None)
        if named is None:
            return
        fragment = named.display_name[: max(1, len(named.display_name) // 2)]
        filtered = client.workspaces.get_members(
            workspace_slug, params=MemberQueryParams(display_name=fragment)
        )
        assert isinstance(filtered, list)
        assert any(m.id == named.id for m in filtered)

    def test_get_members_lite_paginated(self, client: PlaneClient, workspace_slug: str) -> None:
        """get_members_lite returns a paginated envelope of WorkspaceMember items."""
        page = client.workspaces.get_members_lite(
            workspace_slug, params=MemberListQueryParams(per_page=100)
        )
        assert isinstance(page.results, list)
        assert isinstance(page.total_count, int)
        assert isinstance(page.next_page_results, bool)
        for member in page.results:
            assert isinstance(member, WorkspaceMember)

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
