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
def stickies(client: PlaneClient, workspace_slug: str) -> Stickies:
    return client.v2.workspace(workspace_slug).stickies


@pytest.fixture
def sticky(stickies: Stickies) -> Iterator[Any]:
    created = stickies.create(CreateSticky(name=unique_name("sticky")))
    yield created
    try:
        stickies.delete(created.id)
    except Exception:
        pass


def test_list(stickies: Stickies) -> None:
    page = stickies.list()
    assert isinstance(page.data, list)


def test_create_with_empty_body(stickies: Stickies) -> None:
    created = stickies.create(CreateSticky())
    try:
        assert created.id
    finally:
        stickies.delete(created.id)


def test_retrieve_patch_delete(stickies: Stickies, sticky: Any) -> None:
    fetched = stickies.retrieve(sticky.id)
    assert fetched.id == sticky.id

    updated = stickies.update(sticky.id, UpdateSticky(color="#336699"))
    assert updated.color == "#336699"
