"""Teamspaces against a real server; requires the workspace's
`is_teams_enabled` feature flag, else the endpoint 403s/404s. Not
verified against a live server yet."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedWorkspace
from plane.models.v2.teamspaces import CreateTeamspace, UpdateTeamspace

from .helpers import unique_name


@pytest.fixture
def teamspace(workspace: LoadedWorkspace) -> Iterator[Any]:
    created = workspace.teamspaces.create(CreateTeamspace(name=unique_name("team")))
    yield created
    try:
        workspace.teamspaces.delete(created.id)
    except Exception:
        pass


def test_list(workspace: LoadedWorkspace) -> None:
    page = workspace.teamspaces.list()
    assert isinstance(page.data, list)


def test_create_retrieve_patch_delete(workspace: LoadedWorkspace, teamspace: Any) -> None:
    fetched = workspace.teamspaces.retrieve(teamspace.id)
    assert fetched.id == teamspace.id

    updated = workspace.teamspaces.update(
        teamspace.id, UpdateTeamspace(description_html="<p>desc</p>")
    )
    assert updated.description_html == "<p>desc</p>"


def test_find_by_name(workspace: LoadedWorkspace, teamspace: Any) -> None:
    found = workspace.teamspaces.find_by_name(teamspace.name)
    assert found.id == teamspace.id


def test_list_expand_lead(workspace: LoadedWorkspace, teamspace: Any) -> None:
    page = workspace.teamspaces.list(expand=["lead"])
    assert isinstance(page.data, list)
