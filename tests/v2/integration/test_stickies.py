"""Sticky notes against a real server. No feature gate observed. Not verified
against a live server yet."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2.stickies import Stickies
from plane.client import PlaneClient
from plane.models.v2.stickies import CreateSticky, UpdateSticky

from .helpers import unique_name


@pytest.fixture(scope="module")
def stickies(client: PlaneClient) -> Stickies:
    return client.v2.workspaces.stickies


@pytest.fixture
def sticky(stickies: Stickies, workspace_slug: str) -> Iterator[Any]:
    created = stickies.create(workspace_slug, CreateSticky(name=unique_name("sticky")))
    yield created
    try:
        stickies.delete(workspace_slug, created.id)
    except Exception:
        pass


def test_list(stickies: Stickies, workspace_slug: str) -> None:
    page = stickies.list(workspace_slug)
    assert isinstance(page.data, list)


def test_create_with_empty_body(stickies: Stickies, workspace_slug: str) -> None:
    created = stickies.create(workspace_slug, CreateSticky())
    try:
        assert created.id
    finally:
        stickies.delete(workspace_slug, created.id)


def test_retrieve_patch_delete(stickies: Stickies, sticky: Any, workspace_slug: str) -> None:
    fetched = stickies.retrieve(workspace_slug, sticky.id)
    assert fetched.id == sticky.id

    updated = stickies.update(workspace_slug, sticky.id, UpdateSticky(color="#336699"))
    assert updated.color == "#336699"
