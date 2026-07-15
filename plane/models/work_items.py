from typing import TYPE_CHECKING, Any, Literal

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
    name: str | None = None
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
    project: str | dict | None = None
    workspace: str | None = None
    parent: str | None = None
    state: str | StateLite | None = None
    estimate_point: str | None = None
    type: str | dict | None = None


class WorkItemDetail(BaseModel):
    """Detailed work item with expanded relationships."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    # The API returns these as either a list of UUID strings or a list of
    # expanded objects (depending on ?expand=), so accept both — mirroring
    # WorkItemExpand. A bare list[UserLite]/list[Label] rejected the string
    # form and raised a ValidationError on retrieve().
    assignees: list[str] | list[UserLite] = Field(default_factory=list)
    labels: list[str] | list[Label] = Field(default_factory=list)
    type_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    point: int | None = None
    name: str | None = None
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
    project: str | dict | None = None
    workspace: str | None = None
    parent: str | None = None
    state: str | StateLite | None = None
    estimate_point: str | None = None
    type: str | dict | None = None


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
    name: str | None = None
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
    project: str | dict | None = None
    workspace: str | None = None
    parent: str | None = None
    estimate_point: str | None = None
    type: str | dict | None = None


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
    sequence_id: int = Field(..., description="Issue sequence ID")
    project__identifier: str = Field(..., description="Project identifier")
    project_id: str = Field(..., description="Project ID")
    workspace__slug: str = Field(..., description="Workspace slug")


class WorkItemSearch(BaseModel):
    """Work item search results."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    issues: list[WorkItemSearchItem]


class AdvancedSearchWorkItem(BaseModel):
    """Request model for advanced work item search with filters.

    Filters support recursive AND/OR groups. Each filter condition is a
    single key-value dict (e.g. ``{"state_id": "..."}``). Groups are nested
    using ``"and"`` / ``"or"`` keys whose values are lists of conditions or
    sub-groups.

    Example::

        AdvancedSearchWorkItem(
            query="new",
            project_id="project-uuid",
            workspace_search=True,
            filters={
                "and": [
                    {"state_id": "abc-123"},
                    {"or": [
                        {"priority": "high"},
                        {"state_id": "def-456"},
                    ]},
                ]
            },
            limit=100,
        )
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    query: str | None = None
    filters: dict[str, Any] | None = None
    limit: int | None = None
    project_id: str | None = None
    workspace_search: bool | None = None


class AdvancedSearchResult(BaseModel):
    """Advanced search result item."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str
    sequence_id: int
    project_identifier: str
    project_id: str
    workspace_id: str
    type_id: str | None = None
    state_id: str | None = None
    priority: str | None = None
    target_date: str | None = None
    start_date: str | None = None


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
    title: str | None = None


class UpdateWorkItemLink(BaseModel):
    """Request model for updating a work item link."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    url: str | None = None
    title: str | None = None


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


class WorkItemAttachmentCreateResponse(BaseModel):
    """Response from creating a work item attachment.

    Plane returns a wrapper containing both the created attachment record and
    the S3 multipart-POST policy needed to upload the file bytes. After the
    upload completes, the caller should call ``WorkItemAttachments.update``
    with ``is_uploaded=True`` to mark the attachment ready.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attachment: WorkItemAttachment
    upload_data: dict[str, Any]
    asset_id: str | None = None
    asset_url: str | None = None


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


DependencyTypeEnum = Literal[
    "blocking",
    "blocked_by",
    "start_before",
    "start_after",
    "finish_before",
    "finish_after",
]


class WorkItemWithRelationType(BaseModel):
    """Work item with an injected relation_type label."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    sequence_id: int | None = None
    project_id: str | None = None
    state_id: str | None = None
    priority: str | None = None
    type_id: str | None = None
    is_epic: bool | None = None
    label_ids: list[str] = Field(default_factory=list)
    assignee_ids: list[str] = Field(default_factory=list)
    sort_order: float | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    relation_type: str | None = None


class WorkItemDependencyResponse(BaseModel):
    """Response model for GET /relation-dependencies/."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    blocking: list[WorkItemWithRelationType] = Field(default_factory=list)
    blocked_by: list[WorkItemWithRelationType] = Field(default_factory=list)
    start_before: list[WorkItemWithRelationType] = Field(default_factory=list)
    start_after: list[WorkItemWithRelationType] = Field(default_factory=list)
    finish_before: list[WorkItemWithRelationType] = Field(default_factory=list)
    finish_after: list[WorkItemWithRelationType] = Field(default_factory=list)


class CreateWorkItemDependency(BaseModel):
    """Request model for creating work item dependency relations."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    relation_type: DependencyTypeEnum = Field(
        ...,
        description="Dependency direction from the perspective of this work item",
    )
    work_item_ids: list[str] = Field(
        ...,
        description="UUIDs of work items to create dependencies with",
        min_length=1,
    )


class RemoveWorkItemDependency(BaseModel):
    """Request model for removing a work item dependency."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    work_item_id: str = Field(
        ...,
        description="UUID of the related work item whose dependency should be removed",
    )


class CreateWorkItemCustomRelation(BaseModel):
    """Request model for creating a custom (definition-based) work item relation."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    relation_definition_id: str = Field(
        ...,
        description="UUID of the workspace relation definition",
    )
    relation_definition_type: str = Field(
        ...,
        description="The outward or inward label of the definition (controls directionality)",
    )
    work_item_ids: list[str] = Field(
        ...,
        description="UUIDs of work items to create the relation with",
        min_length=1,
    )


class RemoveWorkItemCustomRelation(BaseModel):
    """Request model for removing a custom work item relation."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    work_item_id: str = Field(
        ...,
        description="UUID of the related work item whose custom relation should be removed",
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


class WorkItemSubGroupCountEntry(BaseModel):
    """Count for a single sub-group inside a sub-grouped count response."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int


class WorkItemGroupCountEntry(BaseModel):
    """Count entry for a single group in a grouped count response.

    Shape depends on whether ``sub_group_by`` was supplied:

    * **Flat** (``group_by`` only): ``{"count": N}``
    * **Nested** (``group_by`` + ``sub_group_by``):
      ``{"count": N, "sub_grouped_counts": {sub_key: {"count": N}}}``
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int

    sub_grouped_counts: dict[str, WorkItemSubGroupCountEntry] | None = None


class WorkItemGroupedCountResponse(BaseModel):
    """Response from the workspace work item count endpoint.

    Returned for all calls to ``GET /workspaces/<slug>/work-items/count``.

    **No** ``group_by``::

        {"grouped_by": null, "sub_grouped_by": null, "total_count": N, "grouped_counts": {}}

    **With** ``group_by`` only — ``grouped_counts`` values are ``{"count": N}``::

        {
            "grouped_by": "priority",
            "sub_grouped_by": null,
            "total_count": 42,
            "grouped_counts": {"urgent": {"count": 3}, "None": {"count": 6}}
        }

    **With** ``group_by`` and ``sub_group_by`` — values carry ``count``
    and a nested ``sub_grouped_counts`` dict::

        {
            "grouped_by": "priority",
            "sub_grouped_by": "state_id",
            "total_count": 42,
            "grouped_counts": {
                "urgent": {
                    "count": 3,
                    "sub_grouped_counts": {
                        "949645da-a9dd-4a90-94b0-6c8fa16245ee": {"count": 2},
                        "94d35657-a48c-44fd-bed8-87d895386ba4": {"count": 1}
                    }
                }
            }
        }

    ``grouped_counts`` keys are raw ORM field values: UUID strings for FK/M2M
    dimensions, plain strings for ``priority`` / ``state__group``, and
    ISO-date strings for ``target_date`` / ``start_date``.  The special
    key ``"None"`` represents work items with no value in that dimension.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    grouped_by: str | None = None
    sub_grouped_by: str | None = None
    total_count: int
    grouped_counts: dict[str, WorkItemGroupCountEntry] = Field(default_factory=dict)


WorkItemCountResponse = WorkItemGroupedCountResponse
