"""Teamspaces against a real server; requires the workspace's
`is_teams_enabled` feature flag, else the endpoint 403s/404s. Not
verified against a live server yet."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2.teamspaces import Teamspaces
from plane.client import PlaneClient
from plane.models.v2.teamspaces import CreateTeamspace, UpdateTeamspace

from .helpers import unique_name


@pytest.fixture(scope="module")
def teamspaces(client: PlaneClient, workspace_slug: str) -> Teamspaces:
    return client.v2.workspace(workspace_slug).teamspaces


@pytest.fixture
def teamspace(teamspaces: Teamspaces) -> Iterator[Any]:
    created = teamspaces.create(CreateTeamspace(name=unique_name("team")))
    yield created
    try:
        teamspaces.delete(created.id)
    except Exception:
        pass


def test_list(teamspaces: Teamspaces) -> None:
    page = teamspaces.list()
    assert isinstance(page.data, list)


def test_create_retrieve_patch_delete(teamspaces: Teamspaces, teamspace: Any) -> None:
    fetched = teamspaces.retrieve(teamspace.id)
    assert fetched.id == teamspace.id

    updated = teamspaces.update(teamspace.id, UpdateTeamspace(description_html="<p>desc</p>"))
    assert updated.description_html == "<p>desc</p>"


def test_find_by_name(teamspaces: Teamspaces, teamspace: Any) -> None:
    found = teamspaces.find_by_name(teamspace.name)
    assert found.id == teamspace.id


def test_list_expand_lead(teamspaces: Teamspaces, teamspace: Any) -> None:
    page = teamspaces.list(expand=["lead"])
    assert isinstance(page.data, list)
