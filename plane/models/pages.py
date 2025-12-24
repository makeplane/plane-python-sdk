from typing import Any

from pydantic import BaseModel, ConfigDict

from .enums import PageCreateAPIAccessEnum
from .pagination import PaginatedResponse


class Page(BaseModel):
    """Page model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    description_stripped: str | None = None
    description_html: str | None = None
    description_binary: str | None = None
    description: dict | str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    owned_by: str | None = None
    anchor: str | None = None
    workspace: str | None = None
    projects: list[str] | None = None


class CreatePage(BaseModel):
    """Request model for creating a page."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description_html: str
    access: PageCreateAPIAccessEnum | None = None
    color: str | None = None
    is_locked: bool | None = None
    archived_at: str | None = None
    view_props: Any | None = None
    logo_props: Any | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdatePage(BaseModel):
    """Request model for updating a page."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description_html: str | None = None
    access: PageCreateAPIAccessEnum | None = None
    color: str | None = None
    is_locked: bool | None = None
    archived_at: str | None = None
    view_props: Any | None = None
    logo_props: Any | None = None
    external_id: str | None = None
    external_source: str | None = None


class PaginatedPageResponse(PaginatedResponse):
    """Paginated response for pages."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Page]

