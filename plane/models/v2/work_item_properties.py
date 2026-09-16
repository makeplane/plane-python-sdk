"""Work item property models for api_v2 -- properties/options/contexts split project-scoped vs
workspace-scoped; `issue_type_ids` is the golden's own upstream field name."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

WorkItemPropertyType = Literal[
    "TEXT",
    "DATETIME",
    "DECIMAL",
    "BOOLEAN",
    "OPTION",
    "RELATION",
    "URL",
    "EMAIL",
    "FILE",
    "FORMULA",
]
WorkItemPropertyRelationType = Literal["ISSUE", "USER", "RELEASE", "RICH_TEXT"]


class WorkItemProperty(BaseModel):
    """A custom property definition. `options` is inlined for OPTION-type
    properties -- see also `WorkItemPropertyOptions` for managing them directly."""

    model_config = ConfigDict(extra="allow")

    id: str
    created_at: datetime | None = None
    default_value: list[str] | None = None
    description: str | None = None
    display_name: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_active: bool | None = None
    is_multi: bool | None = None
    is_required: bool | None = None
    logo_props: Any | None = None
    name: str | None = None
    options: list[Any] | None = None
    property_type: WorkItemPropertyType | None = None
    relation_type: WorkItemPropertyRelationType | None = None
    settings: Any | None = None
    validation_rules: Any | None = None


class CreateWorkItemPropertyOption(BaseModel):
    """POST body for a standalone option, or one entry of
    `CreateWorkItemProperty.options` seeding OPTION values on create."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_default: bool | None = None


class CreateWorkItemProperty(BaseModel):
    """POST body; `display_name`/`property_type` required, `options` (write-only) seeds OPTION
    values on create."""

    model_config = ConfigDict(extra="ignore")

    display_name: str
    property_type: WorkItemPropertyType
    default_value: list[str] | None = None
    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_active: bool | None = None
    is_multi: bool | None = None
    is_required: bool | None = None
    options: list[CreateWorkItemPropertyOption] | None = None
    relation_type: WorkItemPropertyRelationType | None = None
    settings: Any | None = None
    validation_rules: Any | None = None


class UpdateWorkItemProperty(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    default_value: list[str] | None = None
    description: str | None = None
    display_name: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_active: bool | None = None
    is_multi: bool | None = None
    is_required: bool | None = None
    options: list[CreateWorkItemPropertyOption] | None = None
    property_type: WorkItemPropertyType | None = None
    relation_type: WorkItemPropertyRelationType | None = None
    settings: Any | None = None
    validation_rules: Any | None = None


class WorkItemPropertyOption(BaseModel):
    """An OPTION-type property's choice."""

    model_config = ConfigDict(extra="allow")

    id: str
    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_default: bool | None = None
    name: str | None = None
    sort_order: float | None = None


class UpdateWorkItemPropertyOption(BaseModel):
    """PATCH body -- every field optional."""

    model_config = ConfigDict(extra="ignore")

    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_default: bool | None = None
    name: str | None = None


class WorkItemPropertyContext(BaseModel):
    """Read shape: a workspace property's per-scope override (which projects and
    work item types it applies to, plus its default value/requiredness there) with
    the resolved project/type/option lists inlined."""

    model_config = ConfigDict(extra="allow")

    id: str
    applies_to_all_projects: bool | None = None
    applies_to_all_work_item_types: bool | None = None
    created_at: datetime | None = None
    default_value: list[str] | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_default: bool | None = None
    is_multi: bool | None = None
    is_required: bool | None = None
    issue_type_ids: list[Any] | None = None  # golden's own field name; pass-through
    name: str | None = None
    options: list[Any] | None = None
    project_ids: list[Any] | None = None
    settings: Any | None = None
    sort_order: float | None = None


class WorkItemPropertyContextOptionInput(BaseModel):
    """One entry of `CreateWorkItemPropertyContext.options`. `id` reconciles an
    existing option; omit it to create a new one from `name`."""

    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    name: str | None = None
    description: str | None = None
    is_default: bool | None = None
    sort_order: float | None = None


class CreateWorkItemPropertyContext(BaseModel):
    """POST body. `issue_type_ids` (golden's own field name) and `project_ids` are
    write-only id lists; leave both unset, or set the matching `applies_to_all_*`
    flag, to apply everywhere."""

    model_config = ConfigDict(extra="ignore")

    applies_to_all_projects: bool | None = None
    applies_to_all_work_item_types: bool | None = None
    default_value: list[str] | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_multi: bool | None = None
    is_required: bool | None = None
    issue_type_ids: list[str] | None = None
    name: str | None = None
    options: list[WorkItemPropertyContextOptionInput] | None = None
    project_ids: list[str] | None = None
    settings: Any | None = None
    sort_order: float | None = None


class UpdateWorkItemPropertyContext(BaseModel):
    """PATCH body -- same shape as `CreateWorkItemPropertyContext`; v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    applies_to_all_projects: bool | None = None
    applies_to_all_work_item_types: bool | None = None
    default_value: list[str] | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_multi: bool | None = None
    is_required: bool | None = None
    issue_type_ids: list[str] | None = None
    name: str | None = None
    options: list[WorkItemPropertyContextOptionInput] | None = None
    project_ids: list[str] | None = None
    settings: Any | None = None
    sort_order: float | None = None
