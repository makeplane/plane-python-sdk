from typing import Any

from pydantic import BaseModel, ConfigDict

from .enums import PriorityEnum
from .pagination import PaginatedResponse


class Epic(BaseModel):
    """Epic model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    deleted_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    point: int | None = None
    name: str
    description: Any | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    description_binary: str | None = None
    priority: PriorityEnum | None = None
    start_date: str | None = None
    target_date: str | None = None
    sequence_id: int | None = None
    sort_order: float | None = None
    completed_at: str | None = None
    archived_at: str | None = None
    is_draft: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str
    workspace: str
    parent: str | None = None
    state: str | None = None
    estimate_point: str | None = None
    type: str | None = None
    assignees: list[str] | None = None
    labels: list[str] | None = None


class PaginatedEpicResponse(PaginatedResponse):
    """Paginated response for epics."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Epic]
