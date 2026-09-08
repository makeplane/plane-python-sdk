"""Live coverage for `ws.permission_schemes`: a read-only list/retrieve surface
over the workspace's built-in and custom schemes. Needs no scope beyond
`workspaces.roles:read`; offline coverage lives in `tests/v2`."""

from __future__ import annotations

import pytest

from plane.api.v2._kernel.errors import PlaneAPIError
from plane.api.v2.permission_schemes import PermissionSchemes
from plane.client import PlaneClient


@pytest.fixture
def permission_schemes(client: PlaneClient) -> PermissionSchemes:
    return client.v2.workspaces.permission_schemes


class TestPermissionSchemes:
    def test_list_includes_system_schemes(
        self, permission_schemes: PermissionSchemes, workspace_slug: str
    ) -> None:
        """Every workspace ships at least the built-in system schemes -- this
        should never come back empty, even in a brand-new workspace."""
        page = permission_schemes.list(workspace_slug)
        assert page.data
        assert any(scheme.is_system for scheme in page.data)

    def test_retrieve_round_trips_a_listed_scheme(
        self, permission_schemes: PermissionSchemes, workspace_slug: str
    ) -> None:
        first = permission_schemes.list(workspace_slug).data[0]
        fetched = permission_schemes.retrieve(workspace_slug, first.id)
        assert fetched.id == first.id

    def test_retrieve_unknown_id_is_404(
        self, permission_schemes: PermissionSchemes, workspace_slug: str
    ) -> None:
        with pytest.raises(PlaneAPIError) as exc_info:
            permission_schemes.retrieve(workspace_slug, "00000000-0000-0000-0000-000000000000")
        assert exc_info.value.status == 404
