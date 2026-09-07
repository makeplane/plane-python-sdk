"""Workspace model for api_v2; every read field but `id` is optional (`?fields=` and
collection deferral can omit any of them). No write DTOs: `workspaces_create` and
`workspaces_partial_update` were cut at Gate A and do not exist."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Workspace(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    slug: str | None = None
    logo_url: str | None = None
    organization_size: str | None = None
    owner_id: str | None = None
    timezone: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
