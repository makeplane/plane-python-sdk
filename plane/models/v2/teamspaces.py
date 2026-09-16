"""Teamspace models for api_v2 (a named grouping of members + projects)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Teamspace(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description_html: str | None = None
    lead_id: str | None = None
    logo_props: object | None = None
    member_ids: list[str] | None = None
    project_ids: list[str] | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateTeamspace(BaseModel):
    """POST body. `name` is required by the API."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description_html: str | None = None
    lead_id: str | None = None
    logo_props: object | None = None
    member_ids: list[str] | None = None
    project_ids: list[str] | None = None


class UpdateTeamspace(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description_html: str | None = None
    lead_id: str | None = None
    logo_props: object | None = None
    member_ids: list[str] | None = None
    project_ids: list[str] | None = None
