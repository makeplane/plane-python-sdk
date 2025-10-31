from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict

from .enums import ModuleStatusEnum
from .pagination import PaginatedResponse

if TYPE_CHECKING:
    from .work_items import WorkItem, WorkItemExpand


class Module(BaseModel):
    """Module model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    total_issues: int | None = None
    cancelled_issues: int | None = None
    completed_issues: int | None = None
    started_issues: int | None = None
    unstarted_issues: int | None = None
    backlog_issues: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    name: str
    description: str | None = None
    description_text: Any | None = None
    description_html: Any | None = None
    start_date: str | None = None
    target_date: str | None = None
    status: ModuleStatusEnum | None = None
    view_props: Any | None = None
    sort_order: float | None = None
    external_source: str | None = None
    external_id: str | None = None
    archived_at: str | None = None
    logo_props: Any | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None
    lead: str | None = None


class ModuleLite(BaseModel):
    """Lite module information."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    name: str
    description: str | None = None
    description_text: Any | None = None
    description_html: Any | None = None
    start_date: str | None = None
    target_date: str | None = None
    status: ModuleStatusEnum | None = None
    view_props: Any | None = None
    sort_order: float | None = None
    external_source: str | None = None
    external_id: str | None = None
    archived_at: str | None = None
    logo_props: Any | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str
    workspace: str
    lead: str | None = None
    members: list[str] | None = None


class CreateModule(BaseModel):
    """Request model for creating a module."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    start_date: str | None = None
    target_date: str | None = None
    status: ModuleStatusEnum | None = None
    lead: str | None = None
    members: list[str] | None = None
    external_source: str | None = None
    external_id: str | None = None


class UpdateModule(BaseModel):
    """Request model for updating a module."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    start_date: str | None = None
    target_date: str | None = None
    status: ModuleStatusEnum | None = None
    lead: str | None = None
    members: list[str] | None = None
    external_source: str | None = None
    external_id: str | None = None


class ModuleWorkItem(BaseModel):
    """Work item in a module."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    sub_issues_count: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None
    module: str | None = None
    issue: "WorkItemExpand"


class PaginatedModuleResponse(PaginatedResponse):
    """Paginated response for modules."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Module]


class PaginatedArchivedModuleResponse(PaginatedResponse):
    """Paginated response for archived modules."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Module]


class PaginatedModuleWorkItemResponse(PaginatedResponse):
    """Paginated response for module work items."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list["WorkItem"]
