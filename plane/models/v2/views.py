"""Saved-view models for api_v2; named `View`/`CreateView`/`UpdateView` here though the golden's
schema name is `IssueView`."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

Access = Literal[0, 1]
"""0 = Private, 1 = Public."""


class View(BaseModel):
    """A saved filter/layout. Project-scoped (`Views.project`) or
    workspace-scoped (`Views.workspace`, where the underlying project is NULL) --
    same shape either way."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = None
    query: object | None = None
    filters: object | None = None
    display_filters: object | None = None
    display_properties: object | None = None
    pql_filters: object | None = None
    logo_props: dict[str, object] | None = None
    is_locked: bool | None = None
    access: Access | None = None
    sort_order: float | None = None
    owned_by_id: str | None = None
    archived_at: datetime | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateView(BaseModel):
    """POST body. `name` is the only field the API requires."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None
    query: object | None = None
    filters: object | None = None
    display_filters: object | None = None
    display_properties: object | None = None
    pql_filters: object | None = None
    logo_props: dict[str, object] | None = None
    is_locked: bool | None = None
    access: Access | None = None
    sort_order: float | None = None


class UpdateView(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description: str | None = None
    query: object | None = None
    filters: object | None = None
    display_filters: object | None = None
    display_properties: object | None = None
    pql_filters: object | None = None
    logo_props: dict[str, object] | None = None
    is_locked: bool | None = None
    access: Access | None = None
    sort_order: float | None = None
