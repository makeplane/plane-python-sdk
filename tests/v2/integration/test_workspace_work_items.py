"""`client.v2.workspaces.work_items` against a real server: workspace-wide listing
plus `retrieve_by_identifier` (the "ENG-12"-style lookup); split out from
`test_work_items.py` since its operationId prefix differs.

Loaded workspace for the reads, and that is as far as loading goes here:
`WorkspaceWorkItems` is the one class in the package that answers *plain* rows, on
purpose. Its URL band has no project segment, so a `LoadedWorkItem`'s children --
which need `("slug", "project", "work_item")` -- have nothing to bind the middle id
from, and reading it off the row's `project_id` field would make navigation depend on
the caller's `?fields=` projection. The last test asserts that, so the exemption is
covered rather than merely written down."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedProject, LoadedWorkspace
from plane.models.v2.work_items import CreateWorkItem

from .helpers import unique_name


@pytest.fixture
def work_item(project: LoadedProject) -> Iterator[Any]:
    """One freshly created work item, deleted afterwards."""
    created = project.work_items.create(CreateWorkItem(name=unique_name("wi")))
    yield created
    try:
        project.work_items.delete(created.id)
    except Exception:
        pass


def test_list_includes_the_work_item(
    workspace: LoadedWorkspace, project_id: str, work_item: Any
) -> None:
    page = workspace.work_items.list(project_id=project_id)
    assert any(row.id == work_item.id for row in page.data)


def test_iterate_includes_the_work_item(
    workspace: LoadedWorkspace, project_id: str, work_item: Any
) -> None:
    rows = list(workspace.work_items.iterate(project_id=project_id))
    assert any(row.id == work_item.id for row in rows)


def test_retrieve_by_identifier_matches_the_uuid_lookup(
    workspace: LoadedWorkspace, work_item: Any
) -> None:
    assert work_item.identifier is not None
    fetched = workspace.work_items.retrieve_by_identifier(work_item.identifier)
    assert fetched.id == work_item.id


def test_workspace_wide_rows_are_plain_and_do_not_navigate(
    workspace: LoadedWorkspace, project_id: str, work_item: Any
) -> None:
    """The documented structural exemption, asserted rather than trusted.

    A row from the workspace-wide listing has no project segment in the URL it came
    from, so it cannot reach a work item's children -- navigation for these goes back
    through the project band. If this ever starts passing, `WorkspaceWorkItems` has
    quietly become navigable and the exemption needs revisiting, not deleting."""
    row = next(
        r for r in workspace.work_items.list(project_id=project_id).data if r.id == work_item.id
    )

    with pytest.raises(AttributeError):
        _ = row.comments  # type: ignore[attr-defined]

    # The route that does work, for the same row.
    assert workspace.projects.retrieve(project_id).work_items.retrieve(row.id).id == row.id
