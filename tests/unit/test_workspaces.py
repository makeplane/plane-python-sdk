"""Unit tests for Workspaces API resource (smoke tests with real HTTP requests)."""

import json
from unittest.mock import MagicMock

import pytest

from plane.client import PlaneClient
from plane.errors.errors import HttpError
from plane.models.query_params import MemberListQueryParams, MemberQueryParams
from plane.models.workspaces import (
    ProjectRoleDistributionEntry,
    WorkspaceAssetDownload,
    WorkspaceMember,
)


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
        paginated_members = client.workspaces.get_members_lite(
            workspace_slug, params=MemberListQueryParams(per_page=100)
        )
        assert isinstance(paginated_members.results, list)
        assert isinstance(paginated_members.total_count, int)
        assert isinstance(paginated_members.next_page_results, bool)
        for member in paginated_members.results:
            assert isinstance(member, WorkspaceMember)

    def test_get_project_role_distribution(self, client: PlaneClient, workspace_slug: str) -> None:
        """get_project_role_distribution returns aggregate role counts."""
        distribution = client.workspaces.get_project_role_distribution(workspace_slug)
        assert isinstance(distribution.total_memberships, int)
        assert isinstance(distribution.total_distinct_members, int)
        assert isinstance(distribution.roles, list)
        for entry in distribution.roles:
            assert isinstance(entry, ProjectRoleDistributionEntry)
            assert hasattr(entry, "slug")
            assert hasattr(entry, "membership_count")
            assert hasattr(entry, "distinct_member_count")

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


class TestWorkspaceAssetsOffline:
    """Workspaces.get_asset against a stubbed HTTP session (no network, no credentials)."""

    ASSET_ID = "0b1f6d1e-6f0e-4f0a-9d63-2f3c1f6f2a11"

    @pytest.fixture
    def offline_client(self) -> PlaneClient:
        return PlaneClient(base_url="https://plane.test", api_key="test-key")

    @staticmethod
    def _response(status_code: int, body: dict | None = None, reason: str = "OK") -> MagicMock:
        resp = MagicMock()
        resp.status_code = status_code
        resp.reason = reason
        resp.content = json.dumps(body).encode() if body is not None else b""
        resp.text = json.dumps(body) if body is not None else ""
        resp.headers = {"content-type": "application/json"}
        resp.json.return_value = body
        return resp

    def test_get_asset_returns_download_details(self, offline_client: PlaneClient) -> None:
        body = {
            "asset_id": self.ASSET_ID,
            "asset_url": "https://bucket.s3.example/signed?X-Amz-Signature=abc",
            "asset_name": "screenshot.png",
            "asset_type": "image/png",
        }
        session_get = MagicMock(return_value=self._response(200, body))
        offline_client.workspaces.session.get = session_get

        asset = offline_client.workspaces.get_asset("acme", self.ASSET_ID)

        assert isinstance(asset, WorkspaceAssetDownload)
        assert asset.asset_id == self.ASSET_ID
        assert asset.asset_url == body["asset_url"]
        assert asset.asset_name == "screenshot.png"
        assert asset.asset_type == "image/png"

    def test_get_asset_hits_workspace_asset_detail_route(self, offline_client: PlaneClient) -> None:
        body = {"asset_id": self.ASSET_ID, "asset_url": "https://signed.example/x"}
        session_get = MagicMock(return_value=self._response(200, body))
        offline_client.workspaces.session.get = session_get

        offline_client.workspaces.get_asset("acme", self.ASSET_ID)

        (url,), kwargs = session_get.call_args
        assert url.endswith(f"/api/v1/workspaces/acme/assets/{self.ASSET_ID}/")
        assert kwargs["headers"]["X-Api-Key"] == "test-key"

    def test_get_asset_tolerates_a_null_url(self, offline_client: PlaneClient) -> None:
        """The server answers 200 with a null url when presigning fails."""
        body = {"asset_id": self.ASSET_ID, "asset_url": None}
        offline_client.workspaces.session.get = MagicMock(return_value=self._response(200, body))

        assert offline_client.workspaces.get_asset("acme", self.ASSET_ID).asset_url is None

    def test_get_asset_optional_fields_default_to_none(self, offline_client: PlaneClient) -> None:
        body = {"asset_id": self.ASSET_ID, "asset_url": "https://signed.example/x"}
        offline_client.workspaces.session.get = MagicMock(return_value=self._response(200, body))

        asset = offline_client.workspaces.get_asset("acme", self.ASSET_ID)

        assert asset.asset_name is None
        assert asset.asset_type is None

    @pytest.mark.parametrize("status_code, reason", [(400, "Bad Request"), (404, "Not Found")])
    def test_get_asset_error_raises_http_error(
        self, offline_client: PlaneClient, status_code: int, reason: str
    ) -> None:
        body = {"error": "Asset not yet uploaded"}
        offline_client.workspaces.session.get = MagicMock(
            return_value=self._response(status_code, body, reason)
        )

        with pytest.raises(HttpError) as exc_info:
            offline_client.workspaces.get_asset("acme", self.ASSET_ID)

        assert exc_info.value.status_code == status_code
