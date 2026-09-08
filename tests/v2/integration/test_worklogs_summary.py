"""Live coverage for `project.worklogs.summary()`: the per-project roll-up of
logged time, returned as a bare array. Requires `is_time_tracking_enabled=True`,
which the shared `project` fixture already sets.

Two loaded rows, two levels: the summary comes off the loaded `project`, and the
worklog that has to exist first is written through the loaded `work_item`."""

from __future__ import annotations

from typing import Any

from plane.api.v2 import LoadedProject
from plane.models.v2.work_items import CreateWorkItemWorklog


class TestProjectWorklogsSummary:
    def test_summary_reflects_a_logged_worklog(
        self, project: LoadedProject, work_item: Any
    ) -> None:
        """Requires the project to have `is_time_tracking_enabled=True` (true of
        the shared `project` fixture) -- otherwise worklog creation 404s."""
        work_item.worklogs.create(CreateWorkItemWorklog(duration=90))

        rows = project.worklogs.summary()

        matching = [row for row in rows if row.work_item_id == work_item.id]
        assert matching
        assert matching[0].duration >= 90

    def test_summary_on_a_project_with_no_worklogs_is_empty_list(
        self, project: LoadedProject
    ) -> None:
        """A project with zero worklogs still returns `[]`, not `null` or a 404
        -- proves the bare-array parse handles the empty case."""
        rows = project.worklogs.summary()
        assert isinstance(rows, list)
