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

    def summary(self) -> builtins.list[WorklogSummaryEntry]:
        """Per-work-item duration totals for this project.

        Returns a plain array, not an enveloped payload, so parsed by hand here."""
        payload = self.transport.request("GET", self._collection_url())
        return [self.model.model_validate(row) for row in payload]
