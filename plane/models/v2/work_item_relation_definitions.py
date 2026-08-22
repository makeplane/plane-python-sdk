"""Work item relation definitions (e.g. `blocks`/`blocked_by`); `is_default` is system-managed and
absent from write DTOs."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkItemRelationDefinition(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    inward: str | None = None
    outward: str | None = None
    color: str | None = None
    description: str | None = None
    is_active: bool | None = None
    is_default: bool | None = None
    logo_props: object | None = None
    sort_order: float | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateWorkItemRelationDefinition(BaseModel):
    """POST body. `name`, `inward` and `outward` are required by the API."""

    model_config = ConfigDict(extra="ignore")

    name: str
    inward: str
    outward: str
    color: str | None = None
    description: str | None = None
    is_active: bool | None = None
    logo_props: object | None = None
    sort_order: float | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateWorkItemRelationDefinition(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    inward: str | None = None
    outward: str | None = None
    color: str | None = None
    description: str | None = None
    is_active: bool | None = None
    logo_props: object | None = None
    sort_order: float | None = None
    external_id: str | None = None
    external_source: str | None = None
