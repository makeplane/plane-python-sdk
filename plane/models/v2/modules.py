"""Module models for api_v2; `member_ids` is read-only -- module membership management is out of
scope for this resource."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

ModuleStatus = Literal["backlog", "planned", "in-progress", "paused", "completed", "cancelled"]


class Module(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = None
    start_date: date | None = None
    target_date: date | None = None
    status: ModuleStatus | None = None
    lead_id: str | None = None
    member_ids: list[str] | None = None
    sort_order: float | None = None
    logo_props: dict[str, object] | None = None
    external_id: str | None = None
    external_source: str | None = None
    archived_at: datetime | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateModule(BaseModel):
    """POST body. `name` is required by the API; `status` defaults server-side to
    `"planned"` when omitted."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None
    start_date: date | None = None
    target_date: date | None = None
    """Must not be earlier than `start_date`."""
    status: ModuleStatus | None = None
    lead_id: str | None = None
    sort_order: float | None = None
    logo_props: dict[str, object] | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateModule(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description: str | None = None
    start_date: date | None = None
    target_date: date | None = None
    status: ModuleStatus | None = None
    lead_id: str | None = None
    sort_order: float | None = None
    logo_props: dict[str, object] | None = None
    external_id: str | None = None
    external_source: str | None = None
