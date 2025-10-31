from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field

from .enums import AccessEnum, PriorityEnum, WorkItemRelationTypeEnum
from .labels import Label
from .pagination import PaginatedResponse
from .states import StateLite
from .users import UserLite

if TYPE_CHECKING:
    from .modules import ModuleLite


class WorkItem(BaseModel):
    """Work item model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    type_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    point: int | None = None
    name: str
    description_html: str | None = None
    description_stripped: str | None = None
    description_binary: str | None = None
    priority: PriorityEnum | None = None
    start_date: str | None = None
    target_date: str | None = None
    sequence_id: int | None = None
    sort_order: float | None = None
    completed_at: str | None = None
    archived_at: str | None = None
    is_draft: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None
    parent: str | None = None
    state: str | None = None
    estimate_point: str | None = None
    type: str | None = None


class WorkItemDetail(BaseModel):
    """Detailed work item with expanded relationships."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    assignees: list[UserLite]
    labels: list[Label]
    type_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    point: int | None = None
    name: str
    description_html: str | None = None
    description_stripped: str | None = None
    description_binary: str | None = None
    priority: PriorityEnum | None = None
    start_date: str | None = None
    target_date: str | None = None
    sequence_id: int | None = None
    sort_order: float | None = None
    completed_at: str | None = None
    archived_at: str | None = None
    is_draft: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None
    parent: str | None = None
    state: str | StateLite | None = None
    estimate_point: str | None = None
    type: str | None = None


class WorkItemExpand(BaseModel):
    """Expanded work item with nested objects."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    cycle: Any | None = None  # historical placeholder
    module: "ModuleLite | None" = None
    labels: list[str] | list[Label] | None = None
    assignees: list[str] | list[UserLite] | None = None
    state: StateLite | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    point: int | None = None
    name: str
    description: Any | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    description_binary: str | None = None
    priority: PriorityEnum | None = None
    start_date: str | None = None
    target_date: str | None = None
    sequence_id: int | None = None
    sort_order: float | None = None
    completed_at: str | None = None
    archived_at: str | None = None
    is_draft: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None
    parent: str | None = None
    estimate_point: str | None = None
    type: str | None = None


class CreateWorkItem(BaseModel):
    """Request model for creating a work item."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    assignees: list[str] | None = None
    labels: list[str] | None = None
    type_id: str | None = None
    deleted_at: str | None = None
    point: int | None = None
    name: str
    description_html: str | None = None
    description_stripped: str | None = None
    priority: PriorityEnum | None = None
    start_date: str | None = None
    target_date: str | None = None
    sequence_id: int | None = None
    sort_order: float | None = None
    completed_at: str | None = None
    archived_at: str | None = None
    is_draft: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    parent: str | None = None
    state: str | None = None
    estimate_point: str | None = None
    type: str | None = None


class UpdateWorkItem(BaseModel):
    """Request model for updating a work item."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    assignees: list[str] | None = None
    labels: list[str] | None = None
    type_id: str | None = None
    deleted_at: str | None = None
    point: int | None = None
    name: str | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    priority: PriorityEnum | None = None
    start_date: str | None = None
    target_date: str | None = None
    sequence_id: int | None = None
    sort_order: float | None = None
    completed_at: str | None = None
    archived_at: str | None = None
    is_draft: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    parent: str | None = None
    state: str | None = None
    estimate_point: str | None = None
    type: str | None = None


class WorkItemForIntakeRequest(BaseModel):
    """Work item data for intake requests."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: Any | None = None
    description_html: str | None = None
    priority: PriorityEnum | None = None


class WorkItemSearchItem(BaseModel):
    """Work item search result item."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(..., description="Issue ID")
    name: str = Field(..., description="Issue name")
    sequence_id: str = Field(..., description="Issue sequence ID")
    project__identifier: str = Field(..., description="Project identifier")
    project_id: str = Field(..., description="Project ID")
    workspace__slug: str = Field(..., description="Workspace slug")


class WorkItemSearch(BaseModel):
    """Work item search results."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    issues: list[WorkItemSearchItem]


class WorkItemActivity(BaseModel):
    """Work item activity model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    verb: str | None = None
    field: str | None = None
    old_value: str | None = None
    new_value: str | None = None
    comment: str | None = None
    attachments: list[str] | None = None
    old_identifier: str | None = None
    new_identifier: str | None = None
    epoch: int | None = None
    project: str
    workspace: str
    issue: str | None = None
    issue_comment: str | None = None
    actor: str | None = None


class WorkItemComment(BaseModel):
    """Work item comment model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    is_member: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    comment_stripped: str | None = None
    comment_html: str | None = None
    attachments: list[str] | None = None
    access: AccessEnum | None = None
    external_source: str | None = None
    external_id: str | None = None
    edited_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None
    issue: str | None = None
    actor: str | None = None


class CreateWorkItemComment(BaseModel):
    """Request model for creating a work item comment."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    comment_json: Any | None = None
    comment_html: str | None = None
    access: AccessEnum | None = None
    external_source: str | None = None
    external_id: str | None = None


class UpdateWorkItemComment(BaseModel):
    """Request model for updating a work item comment."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    comment_json: Any | None = None
    comment_html: str | None = None
    access: AccessEnum | None = None
    external_source: str | None = None
    external_id: str | None = None


class WorkItemLink(BaseModel):
    """Work item link model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    title: str | None = None
    url: str
    metadata: Any | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None
    issue: str | None = None


class CreateWorkItemLink(BaseModel):
    """Request model for creating a work item link."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    url: str


class UpdateWorkItemLink(BaseModel):
    """Request model for updating a work item link."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    url: str | None = None


class WorkItemAttachment(BaseModel):
    """Work item attachment model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    attributes: Any | None = None
    asset: str
    entity_type: str | None = None
    entity_identifier: str | None = None
    is_deleted: bool | None = None
    is_archived: bool | None = None
    external_id: str | None = None
    external_source: str | None = None
    size: int | None = None
    is_uploaded: bool | None = None
    storage_metadata: Any | None = None
    created_by: str | None = None
    updated_by: str | None = None
    user: str | None = None
    workspace: str | None = None
    draft_issue: str | None = None
    project: str | None = None
    issue: str | None = None
    comment: str | None = None
    page: str | None = None


class WorkItemAttachmentUploadRequest(BaseModel):
    """Request model for uploading work item attachments."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str = Field(..., description="Original filename of the asset")
    type: str | None = Field(None, description="MIME type of the file")
    size: int = Field(..., description="File size in bytes")
    external_id: str | None = Field(
        None,
        description="External identifier for the asset",
    )
    external_source: str | None = Field(
        None,
        description="External source system",
    )


class UpdateWorkItemAttachment(BaseModel):
    """Request model for updating a work item attachment."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    is_uploaded: bool | None = Field(
        None,
        description="Mark attachment as uploaded",
    )


class WorkItemRelation(BaseModel):
    """Work item relation model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    project_id: str | None = None
    sequence_id: int | None = None
    relation_type: str | None = None
    name: str | None = None
    type_id: str | None = None
    is_epic: bool | None = None
    state_id: str | None = None
    priority: str | None = None
    created_by: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    updated_by: str | None = None


class CreateWorkItemRelation(BaseModel):
    """Request model for creating work item relations."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    relation_type: WorkItemRelationTypeEnum = Field(
        ...,
        description="Type of relationship between work items",
    )
    issues: list[str] = Field(
        ...,
        description="Array of work item IDs to create relations with",
    )


class RemoveWorkItemRelation(BaseModel):
    """Request model for removing work item relation."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    related_issue: str = Field(
        ...,
        description="ID of the related work item to remove relation with",
    )


class WorkItemRelationResponse(BaseModel):
    """Response model for work item relations."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    blocking: list[str] = Field(
        ...,
        description="List of issue IDs that are blocking this issue",
    )
    blocked_by: list[str] = Field(
        ...,
        description="List of issue IDs that this issue is blocked by",
    )
    duplicate: list[str] = Field(
        ...,
        description="List of issue IDs that are duplicates of this issue",
    )
    relates_to: list[str] = Field(
        ...,
        description="List of issue IDs that relate to this issue",
    )
    start_after: list[str] = Field(
        ...,
        description="List of issue IDs that start after this issue",
    )
    start_before: list[str] = Field(
        ...,
        description="List of issue IDs that start before this issue",
    )
    finish_after: list[str] = Field(
        ...,
        description="List of issue IDs that finish after this issue",
    )
    finish_before: list[str] = Field(
        ...,
        description="List of issue IDs that finish before this issue",
    )


class WorkItemWorkLog(BaseModel):
    """Work item work log model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    description: str | None = None
    duration: int | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project_id: str | None = None
    workspace_id: str | None = None
    logged_by: str | None = None


class CreateWorkItemWorkLog(BaseModel):
    """Request model for creating a work item work log."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    description: str | None = None
    duration: int | None = None
    created_by: str | None = None
    updated_by: str | None = None


class UpdateWorkItemWorkLog(BaseModel):
    """Request model for updating a work item work log."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    description: str | None = None
    duration: int | None = None
    created_by: str | None = None
    updated_by: str | None = None


class PaginatedWorkItemResponse(PaginatedResponse):
    """Paginated response for work items."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[WorkItem]


class PaginatedWorkItemActivityResponse(PaginatedResponse):
    """Paginated response for work item activities."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[WorkItemActivity]


class PaginatedWorkItemCommentResponse(PaginatedResponse):
    """Paginated response for work item comments."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[WorkItemComment]


class PaginatedWorkItemLinkResponse(PaginatedResponse):
    """Paginated response for work item links."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[WorkItemLink]
