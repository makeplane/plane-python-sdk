"""Cycle models for api_v2; every read field but `id` is optional."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Cycle(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    owned_by_id: str | None = None
    sort_order: float | None = None
    timezone: str | None = None
    logo_props: dict[str, object] | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateCycle(BaseModel):
    """POST body. `name` is required by the API."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    """Must not be earlier than `start_date`."""
    sort_order: float | None = None
    timezone: str | None = None
    logo_props: dict[str, object] | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateCycle(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    sort_order: float | None = None
    timezone: str | None = None
    logo_props: dict[str, object] | None = None
    external_id: str | None = None
    external_source: str | None = None
