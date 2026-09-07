"""Intake work items against a real server; requires the project's intake
feature to already be enabled (no v2 toggle exists to verify/enable it here).
Not verified against a live server yet."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.client import PlaneClient
from plane.models.v2.intakes import CreateIntakeWorkItem, UpdateIntakeWorkItem

from .helpers import unique_name


@pytest.fixture
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Any:
    return client.v2.workspace(workspace_slug).project(project_id)


@pytest.fixture
def intake_work_item(proj: Any) -> Iterator[Any]:
    created = proj.intakes.create(CreateIntakeWorkItem(name=unique_name("intake-wi")))
    yield created
    try:
        proj.intakes.delete(created.id)
    except Exception:
        pass


def test_list(proj: Any) -> None:
    page = proj.intakes.list()
    assert isinstance(page.data, list)


def test_create_retrieve_delete(proj: Any, intake_work_item: Any) -> None:
    assert intake_work_item.status == -2  # pending, per IntakeWorkItemStatus

    fetched = proj.intakes.retrieve(intake_work_item.id)
    assert fetched.id == intake_work_item.id


def test_patch_folds_the_status_transition(proj: Any, intake_work_item: Any) -> None:
    """v2 folds v1's separate status endpoint into the same PATCH as any other
    field -- accept the intake item in one call."""
    updated = proj.intakes.update(intake_work_item.id, UpdateIntakeWorkItem(status=1))
    assert updated.status == 1
