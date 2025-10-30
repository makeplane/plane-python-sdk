from pydantic import BaseModel, ConfigDict

from .enums import GroupEnum
from .pagination import PaginatedResponse


class State(BaseModel):
    """State model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    name: str
    description: str | None = None
    color: str
    sequence: int | None = None
    group: GroupEnum | None = None
    is_triage: bool | None = None
    default: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None


class StateLite(BaseModel):
    """Lite state information."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    color: str | None = None
    group: GroupEnum | None = None


class CreateState(BaseModel):
    """Request model for creating a state."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    color: str
    sequence: int | None = None
    group: GroupEnum | None = None
    is_triage: bool | None = None
    default: bool | None = None
    external_source: str | None = None
    external_id: str | None = None


class UpdateState(BaseModel):
    """Request model for updating a state."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    color: str | None = None
    sequence: int | None = None
    group: GroupEnum | None = None
    is_triage: bool | None = None
    default: bool | None = None
    external_source: str | None = None
    external_id: str | None = None


class PaginatedStateResponse(PaginatedResponse):
    """Paginated response for states."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[State]
