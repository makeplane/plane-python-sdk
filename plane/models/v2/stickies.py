"""Sticky-note models for api_v2 (a workspace member's personal sticky notes)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Sticky(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    color: str | None = None
    background_color: str | None = None
    logo_props: object | None = None
    owner_id: str | None = None
    sort_order: float | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateSticky(BaseModel):
    """POST body. Every field is optional -- an empty body creates a blank sticky."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description_html: str | None = None
    color: str | None = None
    background_color: str | None = None
    logo_props: object | None = None
    sort_order: float | None = None


class UpdateSticky(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description_html: str | None = None
    color: str | None = None
    background_color: str | None = None
    logo_props: object | None = None
    sort_order: float | None = None
