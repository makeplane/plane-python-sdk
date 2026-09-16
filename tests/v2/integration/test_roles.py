"""Roles against a real server: read-only, no feature gate -- every workspace
has system roles seeded. Not verified against a live server yet.

Flat path, because `Roles` is the one resource whose own filter collides with a path
id: the golden's `?slug=` (a role's slug) would shadow the workspace `slug`, so it is
spelled `role_slug` and the workspace slug stays the positional argument. Writing
both out is the point of the file."""

from __future__ import annotations

from plane.api.v2.roles import Roles
from plane.client import PlaneClient


def test_list_includes_system_roles(client: PlaneClient, workspace_slug: str) -> None:
    roles: Roles = client.v2.workspaces.roles
    page = roles.list(workspace_slug)
    assert page.data
    assert any(row.is_system for row in page.data)


def test_retrieve(client: PlaneClient, workspace_slug: str) -> None:
    roles: Roles = client.v2.workspaces.roles
    first = roles.list(workspace_slug).data[0]
    fetched = roles.retrieve(workspace_slug, first.id)
    assert fetched.id == first.id


def test_find_by_name(client: PlaneClient, workspace_slug: str) -> None:
    # Role names collide across namespaces by design (confirmed live:
    # `MultipleMatchesFound` for "Admin") -- scope both the list and the
    # lookup to one namespace to disambiguate.
    roles: Roles = client.v2.workspaces.roles
    first = roles.list(workspace_slug, namespace="workspace").data[0]
    assert first.name is not None
    found = roles.find_by_name(workspace_slug, first.name, namespace="workspace")
    assert found.id == first.id


def test_find_by_slug_uses_the_renamed_filter(client: PlaneClient, workspace_slug: str) -> None:
    """`role_slug`, not `slug`: the workspace slug owns the positional argument, and
    the golden's own `?slug=` filter is renamed to get out of its way."""
    roles: Roles = client.v2.workspaces.roles
    first = roles.list(workspace_slug, namespace="workspace").data[0]
    assert first.slug is not None
    page = roles.list(workspace_slug, role_slug=first.slug)
    assert all(row.slug == first.slug for row in page.data)


def test_list_filters_by_namespace(client: PlaneClient, workspace_slug: str) -> None:
    roles: Roles = client.v2.workspaces.roles
    page = roles.list(workspace_slug, namespace="workspace")
    assert all(row.namespace == "workspace" for row in page.data)
