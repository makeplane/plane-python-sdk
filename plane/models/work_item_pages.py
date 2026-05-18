from typing import Any

from pydantic import BaseModel, ConfigDict

from .pagination import PaginatedResponse


class WorkItemPageLite(BaseModel):
    """Nested page info returned inside a WorkItemPage response."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None
    is_global: bool | None = None
    logo_props: Any | None = None


class WorkItemPage(BaseModel):
    """Work item to page link."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    page: WorkItemPageLite | None = None
    issue: str | None = None
    project: str | None = None
    workspace: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None


class CreateWorkItemPage(BaseModel):
    """Request model for linking a page to a work item."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    page_id: str


class PaginatedWorkItemPageResponse(PaginatedResponse):
    """Paginated response for work item page links."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[WorkItemPage]
