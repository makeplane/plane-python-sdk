"""`transfer`/`manage_work_items` (`Cycles`) against a real server; they share
one "completed" gate but check opposite directions on `end_date`, so a work
item must be added before a cycle elapses, then the window moved into the past."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.project import Project
from plane.client import PlaneClient
from plane.models.v2.cycles import CreateCycle, UpdateCycle
from plane.models.v2.work_items import CreateWorkItem

from .helpers import unique_name


@pytest.fixture
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Project:
    return client.v2.workspace(workspace_slug).project(project_id)


@pytest.fixture
def completed_cycle(proj: Project) -> Iterator[Any]:
    """A cycle whose date window is already in the past -- the only shape
    `transfer` accepts as a source (server-enforced). Not eligible for
    `manage_work_items(add=...)` -- see the module docstring."""
    now = datetime.now(timezone.utc)
    created = proj.cycles.create(
        CreateCycle(
            name=unique_name("cycle-completed"),
            start_date=now - timedelta(days=14),
            end_date=now - timedelta(days=7),
        ),
    )
    yield created
    try:
        proj.cycles.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def open_cycle(proj: Project) -> Iterator[Any]:
    """A cycle whose window is entirely in the future -- eligible for `add`,
    reliably rejected by `transfer` as a source."""
    now = datetime.now(timezone.utc)
    created = proj.cycles.create(
        CreateCycle(
            name=unique_name("cycle-open"),
            start_date=now + timedelta(days=1),
            end_date=now + timedelta(days=8),
        ),
    )
    yield created
    try:
        proj.cycles.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def destination_cycle(proj: Project) -> Iterator[Any]:
    created = proj.cycles.create(CreateCycle(name=unique_name("cycle-destination")))
    yield created
    try:
        proj.cycles.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def work_item(proj: Project) -> Iterator[Any]:
    created = proj.work_items.create(CreateWorkItem(name=unique_name("wi-cycle-actions")))
    yield created
    try:
        proj.work_items.delete(created.id)
    except Exception:
        pass


def test_manage_work_items_add_then_remove(
    proj: Project,
    open_cycle: Any,
    work_item: Any,
) -> None:
    added = proj.cycles.manage_work_items(open_cycle.id, add=[work_item.id])
    assert work_item.id in (added.added or [])

    removed = proj.cycles.manage_work_items(open_cycle.id, remove=[work_item.id])
    assert work_item.id in (removed.removed or [])


def test_transfer_moves_incomplete_work_items(
    proj: Project,
    destination_cycle: Any,
    work_item: Any,
) -> None:
    now = datetime.now(timezone.utc)
    # Starts open (so the work item can be added), then its window is moved
    # into the past -- only then does the server consider it a valid
    # `transfer` source. See the module docstring.
    source = proj.cycles.create(
        CreateCycle(
            name=unique_name("cycle-transfer-source"),
            start_date=now + timedelta(days=1),
            end_date=now + timedelta(days=8),
        ),
    )
    try:
        proj.cycles.manage_work_items(source.id, add=[work_item.id])

        proj.cycles.update(
            source.id,
            UpdateCycle(
                start_date=now - timedelta(days=14),
                end_date=now - timedelta(days=7),
            ),
        )

        result = proj.cycles.transfer(source.id, destination_cycle.id)
        assert result.new_cycle_id == destination_cycle.id
    finally:
        proj.cycles.delete(source.id)


def test_transfer_from_an_incomplete_cycle_is_rejected(
    proj: Project,
    open_cycle: Any,
    destination_cycle: Any,
) -> None:
    """v1 parity: only a completed source cycle can be transferred; uses
    `open_cycle` (explicit future `end_date`) as the source."""
    with pytest.raises(PlaneAPIError):
        proj.cycles.transfer(open_cycle.id, destination_cycle.id)
