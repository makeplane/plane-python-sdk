"""Offline coverage for `ws.permission_schemes`: list (with sparse `fields`), retrieve, the
custom-scheme writes, and `impact`."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.permission_schemes import PermissionSchemes
from plane.config import Configuration
from plane.models.v2.permission_schemes import CreatePermissionScheme, UpdatePermissionScheme

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


# -- Custom-scheme writes and impact ----------------------------------------------

SCHEMES = f"{BASE}/workspaces/acme/permission-schemes"


@responses.activate
def test_permission_schemes_create_posts_the_body(permission_schemes: PermissionSchemes) -> None:
    responses.post(
        f"{SCHEMES}/",
        json={"id": "s1", "permissions": ["project:view", "workitem:edit", "workitem:view"]},
    )

    created = permission_schemes.create(
        "acme",
        CreatePermissionScheme(name="Triage", namespace="project", permissions=["workitem:edit"]),
    )

    assert created.permissions == ["project:view", "workitem:edit", "workitem:view"]
    assert json.loads(responses.calls[0].request.body) == {
        "name": "Triage",
        "namespace": "project",
        "permissions": ["workitem:edit"],
    }


@responses.activate
def test_permission_schemes_update_patches_the_detail_url(
    permission_schemes: PermissionSchemes,
) -> None:
    responses.patch(f"{SCHEMES}/s1/", json={"id": "s1", "name": "Renamed"})

    updated = permission_schemes.update("acme", "s1", UpdatePermissionScheme(name="Renamed"))

    assert updated.name == "Renamed"
    assert json.loads(responses.calls[0].request.body) == {"name": "Renamed"}


@responses.activate
def test_permission_schemes_delete(permission_schemes: PermissionSchemes) -> None:
    responses.delete(f"{SCHEMES}/s1/", status=204)

    assert permission_schemes.delete("acme", "s1") is None
    assert responses.calls[0].request.url == f"{SCHEMES}/s1/"


@responses.activate
def test_permission_schemes_impact_gets_the_counts(permission_schemes: PermissionSchemes) -> None:
    responses.get(f"{SCHEMES}/s1/impact/", json={"roles": 2, "users": 7, "projects": 3})

    impact = permission_schemes.impact("acme", "s1")

    assert (impact.roles, impact.users, impact.projects) == (2, 7, 3)
    assert responses.calls[0].request.method == "GET"
