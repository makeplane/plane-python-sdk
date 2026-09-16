"""Milestone models for api_v2; the golden's identifying field is `title`, but `?name=` is the list
filter (aliased server-side)."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class Milestone(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    title: str | None = None
    target_date: date | None = None
    external_id: str | None = None
    external_source: str | None = None
    archived_at: datetime | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateMilestone(BaseModel):
    """POST body. `title` is required by the API."""

    model_config = ConfigDict(extra="ignore")

    title: str
    target_date: date | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateMilestone(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    title: str | None = None
    target_date: date | None = None
    external_id: str | None = None
    external_source: str | None = None
