"""Project worklog duration summary (api_v2). Single read-only report endpoint,
not a paginated collection: response is a bare JSON array, one row per work item."""

from __future__ import annotations

import builtins

from ...models.v2.worklogs_summary import WorklogSummaryEntry
from ._kernel.resource import V2Resource


class ProjectWorklogs(V2Resource[WorklogSummaryEntry, WorklogSummaryEntry, WorklogSummaryEntry]):
    path = "/workspaces/{slug}/projects/{project_id}/worklogs/summary/"
    model = WorklogSummaryEntry
    # No `fields=` support on this operation -- it is not in the golden's FIELDS
    # map at all.
    operations = {
        "summary": "project_worklogs_summary",
    }

    def summary(self, slug: str, project: str) -> builtins.list[WorklogSummaryEntry]:
        """Per-work-item duration totals for this project.

        Returns a plain array, not an enveloped payload, so parsed via the
        kernel's `_custom_action_list` rather than a hand-built URL."""
        return self._custom_action_list(
            "summary",
            model=WorklogSummaryEntry,
            method="GET",
            slug=slug,
            project_id=project,
        )
