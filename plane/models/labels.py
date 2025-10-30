from pydantic import BaseModel, ConfigDict

from .pagination import PaginatedResponse


class Label(BaseModel):
    """Label model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    name: str
    description: str | None = None
    color: str | None = None
    sort_order: float | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    workspace: str | None = None
    project: str | None = None
    parent: str | None = None


class CreateLabel(BaseModel):
    """Request model for creating a label."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    color: str | None = None
    description: str | None = None
    external_source: str | None = None
    external_id: str | None = None
    parent: str | None = None
    sort_order: float | None = None


class UpdateLabel(BaseModel):
    """Request model for updating a label."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    color: str | None = None
    description: str | None = None
    external_source: str | None = None
    external_id: str | None = None
    parent: str | None = None
    sort_order: float | None = None


class PaginatedLabelResponse(PaginatedResponse):
    """Paginated response for labels."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Label]
