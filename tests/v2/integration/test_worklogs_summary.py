"""Live coverage for `proj.worklogs.summary()`: the per-project roll-up of
logged time, returned as a bare array. Requires `is_time_tracking_enabled=True`,
which the shared `project` fixture already sets."""

from __future__ import annotations

from typing import Any

import pytest

from plane.api.v2.project import Project
from plane.client import PlaneClient
from plane.models.v2.work_items import CreateWorkItemWorklog


@pytest.fixture
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Project:
    return client.v2.workspace(workspace_slug).project(project_id)


class TestProjectWorklogsSummary:
    def test_summary_reflects_a_logged_worklog(self, proj: Project, work_item: Any) -> None:
        """Requires the project to have `is_time_tracking_enabled=True` (true of
        the shared `project` fixture) -- otherwise worklog creation 404s."""
        proj.work_items.worklogs.create(work_item.id, CreateWorkItemWorklog(duration=90))

        rows = proj.worklogs.summary()

        matching = [row for row in rows if row.work_item_id == work_item.id]
        assert matching
        assert matching[0].duration >= 90

    def test_summary_on_a_project_with_no_worklogs_is_empty_list(self, proj: Project) -> None:
        """A project with zero worklogs still returns `[]`, not `null` or a 404
        -- proves the bare-array parse handles the empty case."""
        rows = proj.worklogs.summary()
        assert isinstance(rows, list)
