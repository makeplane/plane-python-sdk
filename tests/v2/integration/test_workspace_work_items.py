"""`client.v2.workspace(...).work_items` against a real server: workspace-wide
listing plus `retrieve_by_identifier` (the "ENG-12"-style lookup); split out
from `test_work_items.py` since its operationId prefix differs."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.client import PlaneClient
from plane.models.v2.work_items import CreateWorkItem

from .helpers import unique_name


@pytest.fixture
def work_item(client: PlaneClient, workspace_slug: str, project_id: str) -> Iterator[Any]:
    """One freshly created work item, deleted afterwards."""
    proj = client.v2.workspace(workspace_slug).project(project_id)
    created = proj.work_items.create(CreateWorkItem(name=unique_name("wi")))
    yield created
    try:
        proj.work_items.delete(created.id)
    except Exception:
        pass


def test_list_includes_the_work_item(
    client: PlaneClient, workspace_slug: str, project_id: str, work_item: Any
) -> None:
    ws = client.v2.workspace(workspace_slug)
    page = ws.work_items.list(project_id=project_id)
    assert any(row.id == work_item.id for row in page.data)


def test_iterate_includes_the_work_item(
    client: PlaneClient, workspace_slug: str, project_id: str, work_item: Any
) -> None:
    ws = client.v2.workspace(workspace_slug)
    rows = list(ws.work_items.iterate(project_id=project_id))
    assert any(row.id == work_item.id for row in rows)


def test_retrieve_by_identifier_matches_the_uuid_lookup(
    client: PlaneClient, workspace_slug: str, project_id: str, work_item: Any
) -> None:
    ws = client.v2.workspace(workspace_slug)
    assert work_item.identifier is not None
    fetched = ws.work_items.retrieve_by_identifier(work_item.identifier)
    assert fetched.id == work_item.id

    url = f"/workspaces/{workspace_slug}/work-items/{work_item.identifier}/"
    # Sanity: this really is the workspace-level, non-project-scoped route.
    assert "projects" not in url
