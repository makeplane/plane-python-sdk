"""State models for api_v2; every read field but `id` is optional."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

StateGroup = Literal["backlog", "unstarted", "started", "completed", "cancelled", "triage"]


class State(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    color: str | None = None
    description: str | None = None
    group: StateGroup | None = None
    is_default: bool | None = None
    is_triage: bool | None = None
    sequence: float | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateState(BaseModel):
    """POST body. `name` and `color` are required by the API."""

    model_config = ConfigDict(extra="ignore")

    name: str
    color: str
    description: str | None = None
    group: StateGroup | None = None
    is_default: bool | None = None
    sequence: float | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateState(BaseModel):
    """PATCH body — every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    color: str | None = None
    description: str | None = None
    group: StateGroup | None = None
    is_default: bool | None = None
    sequence: float | None = None
    external_id: str | None = None
    external_source: str | None = None
