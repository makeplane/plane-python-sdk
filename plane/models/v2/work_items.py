"""Work item models for api_v2; `CreateWorkItem`/`UpdateWorkItem` accept both `*_id`/`*_ids` and
readable-name forms for state/assignees/labels/parent/type -- prefer readable."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

Priority = Literal["none", "low", "medium", "high", "urgent"]
CommentAccess = Literal["INTERNAL", "EXTERNAL"]
DependencyRelationType = Literal[
    "blocked_by", "blocking", "start_before", "start_after", "finish_before", "finish_after"
]


class WorkItem(BaseModel):
    """A work item. `identifier` (e.g. `"ENG-12"`) is the human-readable key --
    see `WorkItems.retrieve_by_identifier` to fetch by it directly."""

    model_config = ConfigDict(extra="allow")

    id: str
    archived_at: datetime | None = None
    assignee_ids: list[str] | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    custom_fields: dict[str, object] | None = None
    cycle_id: str | None = None
    identifier: str | None = None
    is_draft: bool | None = None
    label_ids: list[str] | None = None
    module_ids: list[str] | None = None
    name: str | None = None
    parent_id: str | None = None
    priority: Priority | None = None
    project_id: str | None = None
    sequence_id: int | None = None
    start_date: date | None = None
    state_id: str | None = None
    target_date: date | None = None
    type_id: str | None = None


class CreateWorkItem(BaseModel):
    """POST body; `name` is the only required field -- prefer readable fields (`state`,
    `assignees`, `labels`, `parent`, `type`) over their id counterparts."""

    model_config = ConfigDict(extra="ignore")

    name: str
    assignee_ids: list[str] | None = None
    assignees: list[str] | None = None
    """Readable form of `assignee_ids`: member emails (or other identifying values
    the API resolves)."""
    custom_fields: dict[str, object] | None = None
    cycle_id: str | None = None
    description_html: str | None = None
    estimate: str | None = None
    estimate_point_id: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    label_ids: list[str] | None = None
    labels: list[str] | None = None
    """Readable form of `label_ids`: label names."""
    module_ids: list[str] | None = None
    parent: str | None = None
    """Readable form of `parent_id`: the parent work item's `identifier` (e.g.
    `"ENG-3"`)."""
    parent_id: str | None = None
    priority: Priority | None = None
    start_date: date | None = None
    state: str | None = None
    """Readable form of `state_id`: the state's name."""
    state_id: str | None = None
    target_date: date | None = None
    type: str | None = None
    """Readable form of `type_id`: the work item type's name."""
    type_id: str | None = None


class UpdateWorkItem(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT. Same readable/`*_id`
    field pairs as `CreateWorkItem`."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    assignee_ids: list[str] | None = None
    assignees: list[str] | None = None
    custom_fields: dict[str, object] | None = None
    cycle_id: str | None = None
    description_html: str | None = None
    estimate: str | None = None
    estimate_point_id: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    label_ids: list[str] | None = None
    labels: list[str] | None = None
    module_ids: list[str] | None = None
    parent: str | None = None
    parent_id: str | None = None
    priority: Priority | None = None
    start_date: date | None = None
    state: str | None = None
    state_id: str | None = None
    target_date: date | None = None
    type: str | None = None
    type_id: str | None = None


# -- Comments -----------------------------------------------------------------


class WorkItemComment(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    access: CommentAccess | None = None
    actor_id: str | None = None
    comment_html: str | None = None
    comment_stripped: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    edited_at: datetime | None = None
    external_id: str | None = None
    external_source: str | None = None
    work_item_id: str | None = None


class CreateWorkItemComment(BaseModel):
    model_config = ConfigDict(extra="ignore")

    comment_html: str
    access: CommentAccess | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateWorkItemComment(BaseModel):
    model_config = ConfigDict(extra="ignore")

    comment_html: str | None = None
    access: CommentAccess | None = None
    external_id: str | None = None
    external_source: str | None = None


# -- Attachments ----------------------------------------------------------------


class WorkItemAttachment(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    asset_url: str | None = None
    attributes: dict[str, object] | None = None
    content_type: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_uploaded: bool | None = None
    name: str | None = None
    size: float | None = None
    work_item_id: str | None = None


class CreateWorkItemAttachment(BaseModel):
    """POST body. This registers the attachment's metadata (name, size, content
    type); the returned `asset_url` is where the caller then uploads the file
    itself, and a follow-up PATCH (`WorkItemAttachmentConfirm`) marks it uploaded."""

    model_config = ConfigDict(extra="ignore")

    name: str
    size: int
    type: str | None = None
    external_id: str | None = None
    external_source: str | None = None


class WorkItemAttachmentConfirm(BaseModel):
    """PATCH body -- confirms the out-of-band upload completed."""

    model_config = ConfigDict(extra="ignore")

    is_uploaded: bool | None = None


class WorkItemAttachmentUploadResult(BaseModel):
    """The real response to `POST .../attachments/`: the golden documents a bare
    `WorkItemAttachment`, but the live server returns `{upload_data, attachment}`."""

    model_config = ConfigDict(extra="allow")

    asset_id: str
    asset_url: str
    upload_data: dict[str, object]
    attachment: WorkItemAttachment


# -- Links ------------------------------------------------------------------


class WorkItemLink(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    created_at: datetime | None = None
    created_by_id: str | None = None
    metadata: dict[str, object] | None = None
    title: str | None = None
    url: str | None = None
    work_item_id: str | None = None


class CreateWorkItemLink(BaseModel):
    model_config = ConfigDict(extra="ignore")

    url: str
    title: str | None = None
    metadata: dict[str, object] | None = None


class UpdateWorkItemLink(BaseModel):
    model_config = ConfigDict(extra="ignore")

    url: str | None = None
    title: str | None = None
    metadata: dict[str, object] | None = None


# -- Worklogs -----------------------------------------------------------------


class WorkItemWorklog(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    created_at: datetime | None = None
    created_by_id: str | None = None
    description: str | None = None
    duration: int | None = None
    logged_by_id: str | None = None
    updated_at: datetime | None = None
    work_item_id: str | None = None


class CreateWorkItemWorklog(BaseModel):
    model_config = ConfigDict(extra="ignore")

    duration: int
    description: str | None = None


class UpdateWorkItemWorklog(BaseModel):
    model_config = ConfigDict(extra="ignore")

    duration: int | None = None
    description: str | None = None


# -- Activities (read-only) ------------------------------------------------------


class WorkItemActivity(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    actor_id: str | None = None
    comment: str | None = None
    created_at: datetime | None = None
    duration: int | None = None
    epoch: float | None = None
    external_id: str | None = None
    external_source: str | None = None
    field: str | None = None
    issue_comment_id: str | None = None  # upstream field name, passed through verbatim
    new_identifier_id: str | None = None
    new_value: str | None = None
    old_identifier_id: str | None = None
    old_value: str | None = None
    verb: str | None = None
    work_item_id: str | None = None


# -- Relations ----------------------------------------------------------------


class WorkItemRelationList(BaseModel):
    """Related work item ids grouped by direction label (dynamic mapping, access via
    `.model_extra`); each value is a `list[str]` of ids."""

    model_config = ConfigDict(extra="allow")


class WorkItemRelationCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    direction: str
    relation_definition_id: str
    work_item_ids: list[str]


# -- Dependencies ---------------------------------------------------------------


class WorkItemDependencyList(BaseModel):
    """The six fixed dependency directions. Always present in the response, each
    a (possibly empty) list of related work item ids."""

    model_config = ConfigDict(extra="allow")

    blocked_by: list[str] = []
    blocking: list[str] = []
    start_after: list[str] = []
    start_before: list[str] = []
    finish_after: list[str] = []
    finish_before: list[str] = []


class WorkItemDependencyCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    relation_type: DependencyRelationType
    work_item_ids: list[str]
