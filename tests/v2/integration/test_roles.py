"""Roles against a real server: read-only, no feature gate -- every workspace
has system roles seeded. Not verified against a live server yet."""

from __future__ import annotations

from plane.api.v2.roles import Roles
from plane.client import PlaneClient


def test_list_includes_system_roles(client: PlaneClient, workspace_slug: str) -> None:
    roles: Roles = client.v2.workspace(workspace_slug).roles
    page = roles.list()
    assert page.data
    assert any(row.is_system for row in page.data)


def test_retrieve(client: PlaneClient, workspace_slug: str) -> None:
    roles: Roles = client.v2.workspace(workspace_slug).roles
    first = roles.list().data[0]
    fetched = roles.retrieve(first.id)
    assert fetched.id == first.id


def test_find_by_name(client: PlaneClient, workspace_slug: str) -> None:
    # Role names collide across namespaces by design (confirmed live:
    # `MultipleMatchesFound` for "Admin") -- scope both the list and the
    # lookup to one namespace to disambiguate.
    roles: Roles = client.v2.workspace(workspace_slug).roles
    first = roles.list(namespace="workspace").data[0]
    assert first.name is not None
    found = roles.find_by_name(first.name, namespace="workspace")
    assert found.id == first.id


def test_list_filters_by_namespace(client: PlaneClient, workspace_slug: str) -> None:
    roles: Roles = client.v2.workspace(workspace_slug).roles
    page = roles.list(namespace="workspace")
    assert all(row.namespace == "workspace" for row in page.data)
