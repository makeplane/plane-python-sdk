"""Offline coverage for `ws.permission_schemes`: a read-only workspace-scoped list (with sparse
`fields`) and retrieve."""

from __future__ import annotations

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.permission_schemes import PermissionSchemes
from plane.config import Configuration

BASE = "https://api.example.com/api/v2"


@pytest.fixture
def permission_schemes(config: Configuration) -> PermissionSchemes:
    return PermissionSchemes(V2Transport(config))


@responses.activate
def test_permission_schemes_list(permission_schemes: PermissionSchemes) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/permission-schemes/",
        json={
            "data": [{"id": "1", "name": "Admin", "namespace": "workspace"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = permission_schemes.list("acme")

    assert page.total_count == 1
    assert page.data[0].namespace == "workspace"
    assert responses.calls[0].request.url.startswith(f"{BASE}/workspaces/acme/permission-schemes/")


@responses.activate
def test_permission_schemes_sparse_fields_leave_rest_none(
    permission_schemes: PermissionSchemes,
) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/permission-schemes/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = permission_schemes.list("acme", fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None
    assert "fields=id" in responses.calls[0].request.url


@responses.activate
def test_permission_schemes_retrieve(permission_schemes: PermissionSchemes) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/permission-schemes/1/",
        json={"id": "1", "name": "Admin", "is_system": True},
    )

    scheme = permission_schemes.retrieve("acme", "1")

    assert scheme.is_system is True
    assert responses.calls[0].request.url == f"{BASE}/workspaces/acme/permission-schemes/1/"


@responses.activate
def test_permission_schemes_iterate_takes_the_workspace_slug(
    permission_schemes: PermissionSchemes,
) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/permission-schemes/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}, "total_count": 1},
    )

    rows = list(permission_schemes.iterate("acme"))

    assert rows[0].id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/workspaces/acme/permission-schemes/")


@responses.activate
def test_permission_schemes_list_per_page_and_offset(
    permission_schemes: PermissionSchemes,
) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/permission-schemes/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    permission_schemes.list("acme", per_page=10, offset=20)

    request_url = responses.calls[0].request.url
    assert "per_page=10" in request_url
    assert "offset=20" in request_url


def test_permission_schemes_unknown_field_rejected(
    permission_schemes: PermissionSchemes,
) -> None:
    """`fields` is validated against the golden's `permission_schemes_list` enum
    -- negative assertion, proven capable of failing below."""
    with pytest.raises(ValueError, match="Unknown field"):
        permission_schemes.list("acme", fields=["not_a_real_field"])
