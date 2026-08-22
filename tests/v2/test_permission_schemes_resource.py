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
    return PermissionSchemes(V2Transport(config), slug="acme")


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

    page = permission_schemes.list()

    assert page.total_count == 1
    assert page.data[0].namespace == "workspace"


@responses.activate
def test_permission_schemes_sparse_fields_leave_rest_none(
    permission_schemes: PermissionSchemes,
) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/permission-schemes/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = permission_schemes.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None


@responses.activate
def test_permission_schemes_retrieve(permission_schemes: PermissionSchemes) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/permission-schemes/1/",
        json={"id": "1", "name": "Admin", "is_system": True},
    )

    scheme = permission_schemes.retrieve("1")

    assert scheme.is_system is True


def test_permission_schemes_unknown_field_rejected(
    permission_schemes: PermissionSchemes,
) -> None:
    """`fields` is validated against the golden's `permission_schemes_list` enum
    -- negative assertion, proven capable of failing below."""
    with pytest.raises(ValueError, match="Unknown field"):
        permission_schemes.list(fields=["not_a_real_field"])
