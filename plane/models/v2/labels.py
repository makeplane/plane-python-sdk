"""Label models for api_v2. Read fields are optional for the same reason as states."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Label(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    color: str | None = None
    description: str | None = None
    parent_id: str | None = None
    sort_order: float | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateLabel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    color: str | None = None
    description: str | None = None
    parent_id: str | None = None
    sort_order: float | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateLabel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    color: str | None = None
    description: str | None = None
    parent_id: str | None = None
    sort_order: float | None = None
    external_id: str | None = None
    external_source: str | None = None
