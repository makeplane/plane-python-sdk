"""Initiative models for api_v2; `InitiativeLabel` is workspace-level (not nested under an
initiative) -- use `Initiatives.manage_labels` to attach/detach."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

InitiativeState = Literal["DRAFT", "PLANNED", "ACTIVE", "COMPLETED", "CLOSED"]


class Initiative(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = None
    description_html: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    state: InitiativeState | None = None
    lead_id: str | None = None
    label_ids: list[str] | None = None
    project_ids: list[str] | None = None
    logo_props: Any | None = None
    archived_at: datetime | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateInitiative(BaseModel):
    """POST body. `name` is the only field the API requires. `end_date` must not
    be earlier than `start_date` (server-enforced)."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None
    description_html: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    state: InitiativeState | None = None
    lead_id: str | None = None
    project_ids: list[str] | None = None
    logo_props: Any | None = None


class UpdateInitiative(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description: str | None = None
    description_html: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    state: InitiativeState | None = None
    lead_id: str | None = None
    project_ids: list[str] | None = None
    logo_props: Any | None = None


class InitiativeLabel(BaseModel):
    """A workspace-level initiative label -- see the module docstring for why this
    is not nested under an initiative id."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    color: str | None = None
    description: str | None = None
    sort_order: float | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateInitiativeLabel(BaseModel):
    """POST body. `name` is the only field the API requires."""

    model_config = ConfigDict(extra="ignore")

    name: str
    color: str | None = None
    description: str | None = None
    sort_order: float | None = None


class UpdateInitiativeLabel(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    color: str | None = None
    description: str | None = None
    sort_order: float | None = None


class InitiativeChildManageRequest(BaseModel):
    """POST body shared by `Initiatives.manage_labels` / `.manage_projects` /
    `.manage_work_items`: ids to add/remove from that child collection. Both
    lists are optional; omit either to leave that side unchanged."""

    model_config = ConfigDict(extra="ignore")

    add: list[str] | None = None
    remove: list[str] | None = None


class InitiativeChildManageResponse(BaseModel):
    """The ids actually added/removed by one of the `Initiatives` manage-child
    actions."""

    model_config = ConfigDict(extra="allow")

    added: list[str] = []
    removed: list[str] = []
