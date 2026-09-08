"""`transfer`/`.work_items.add`/`.remove` (`Cycles`) against a real server; they
share one "completed" gate but check opposite directions on `end_date`, so a
work item must be added before a cycle elapses, then the window moved into
the past.

Two levels of loaded row, and deliberately so: the cycles come off the loaded
`project`, and the membership bridge comes off each loaded *cycle*
(`open_cycle.work_items.add([...])`). `project.cycles.work_items` is not a route --
it would be an untyped hop past a row that was never fetched, and it now refuses
rather than dropping the project id (`tests/v2/test_owned_sub_resources.py`)."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError
from plane.models.v2.cycles import CreateCycle, UpdateCycle
from plane.models.v2.work_items import CreateWorkItem

from .helpers import unique_name


@pytest.fixture
def completed_cycle(project: LoadedProject) -> Iterator[Any]:
    """A cycle whose date window is already in the past -- the only shape
    `transfer` accepts as a source (server-enforced). Not eligible for
    `.work_items.add(...)` -- see the module docstring."""
    now = datetime.now(timezone.utc)
    created = project.cycles.create(
        CreateCycle(
            name=unique_name("cycle-completed"),
            start_date=now - timedelta(days=14),
            end_date=now - timedelta(days=7),
        ),
    )
    yield created
    try:
        project.cycles.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def open_cycle(project: LoadedProject) -> Iterator[Any]:
    """A cycle whose window is entirely in the future -- eligible for `add`,
    reliably rejected by `transfer` as a source."""
    now = datetime.now(timezone.utc)
    created = project.cycles.create(
        CreateCycle(
            name=unique_name("cycle-open"),
            start_date=now + timedelta(days=1),
            end_date=now + timedelta(days=8),
        ),
    )
    yield created
    try:
        project.cycles.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def destination_cycle(project: LoadedProject) -> Iterator[Any]:
    created = project.cycles.create(CreateCycle(name=unique_name("cycle-destination")))
    yield created
    try:
        project.cycles.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def work_item(project: LoadedProject) -> Iterator[Any]:
    created = project.work_items.create(CreateWorkItem(name=unique_name("wi-cycle-actions")))
    yield created
    try:
        project.work_items.delete(created.id)
    except Exception:
        pass


def test_work_items_add_then_remove(open_cycle: Any, work_item: Any) -> None:
    added = open_cycle.work_items.add([work_item.id])
    assert work_item.id in added

    removed = open_cycle.work_items.remove([work_item.id])
    assert work_item.id in removed


def test_transfer_moves_incomplete_work_items(
    project: LoadedProject,
    destination_cycle: Any,
    work_item: Any,
) -> None:
    now = datetime.now(timezone.utc)
    # Starts open (so the work item can be added), then its window is moved
    # into the past -- only then does the server consider it a valid
    # `transfer` source. See the module docstring.
    source = project.cycles.create(
        CreateCycle(
            name=unique_name("cycle-transfer-source"),
            start_date=now + timedelta(days=1),
            end_date=now + timedelta(days=8),
        ),
    )
    try:
        source.work_items.add([work_item.id])

        project.cycles.update(
            source.id,
            UpdateCycle(
                start_date=now - timedelta(days=14),
                end_date=now - timedelta(days=7),
            ),
        )

        result = project.cycles.transfer(source.id, destination_cycle.id)
        assert result.new_cycle_id == destination_cycle.id
    finally:
        project.cycles.delete(source.id)


def test_transfer_from_an_incomplete_cycle_is_rejected(
    project: LoadedProject,
    open_cycle: Any,
    destination_cycle: Any,
) -> None:
    """v1 parity: only a completed source cycle can be transferred; uses
    `open_cycle` (explicit future `end_date`) as the source."""
    with pytest.raises(PlaneAPIError):
        project.cycles.transfer(open_cycle.id, destination_cycle.id)
