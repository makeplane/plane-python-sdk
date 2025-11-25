from pydantic import BaseModel, ConfigDict

from .pagination import PaginatedResponse


class Sticky(BaseModel):
    """Response model for a sticky."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str | None = None
    description: dict | str | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    description_binary: bytes | None = None
    logo_props: dict | None = None
    color: str | None = None
    background_color: str | None = None
    workspace: str
    owner: str
    sort_order: float | None = None
    created_at: str | None = None
    updated_at: str | None = None


class CreateSticky(BaseModel):
    """Request model for creating a sticky."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: dict | str | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    description_binary: bytes | None = None
    logo_props: dict | None = None
    color: str | None = None
    background_color: str | None = None


class UpdateSticky(BaseModel):
    """Request model for updating a sticky."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: dict | str | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    description_binary: bytes | None = None
    logo_props: dict | None = None
    color: str | None = None
    background_color: str | None = None


class PaginatedStickyResponse(PaginatedResponse):
    """Paginated response for stickies."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Sticky]
