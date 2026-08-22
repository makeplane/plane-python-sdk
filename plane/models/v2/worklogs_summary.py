"""Per-work-item worklog duration totals for api_v2
(`GET .../projects/{project_id}/worklogs/summary/`).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class WorklogSummaryEntry(BaseModel):
    """One summary row; `work_item_id` is the only identity (no `id` field), and both fields are
    required (no `fields=` support)."""

    model_config = ConfigDict(extra="allow")

    work_item_id: str
    duration: int
