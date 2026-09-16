"""Work item type + property models for api_v2; `WorkItemType` carries no
`external_id`/`external_source` output fields despite the write DTO accepting them."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

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


class WorkItemType(BaseModel):
    """Read-only work item type -- authored in the app/admin; v2 only reads it so a
    caller can pick a `type_id` and fetch its writable-field schema via `schema()`."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    is_default: bool | None = None
    is_epic: bool | None = None
    level: float | None = None
    logo_props: Any | None = None
    created_at: datetime | None = None


class CreateWorkItemType(BaseModel):
    """POST body; only name/description/is_active/external_id/external_source are client-writable
    -- `logo_props`/`is_default`/`is_epic`/`level` are server-managed."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None
    is_active: bool | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateWorkItemType(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    external_id: str | None = None
    external_source: str | None = None


class WorkItemTypeImport(BaseModel):
    """Body for `work_item_types_import`: ids of the (global/system) work item
    types to enable on this project."""

    model_config = ConfigDict(extra="ignore")

    work_item_types: list[str]


class WorkItemTypeSchema(BaseModel):
    """The `schema` action's response: writable standard fields plus custom properties for building
    a create/update form; every field is defensively optional."""

    model_config = ConfigDict(extra="allow")

    type_id: str | None = None
    type_name: str | None = None
    type_description: str | None = None
    type_logo_props: Any | None = None
    fields: Any | None = None
    custom_fields: Any | None = None


class WorkItemProperty(BaseModel):
    """Read-only custom property definition attached to a work item type.
    `options` is inlined for OPTION-type properties."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    display_name: str | None = None
    description: str | None = None
    property_type: WorkItemPropertyType | None = None
    relation_type: WorkItemPropertyRelationType | None = None
    is_active: bool | None = None
    is_multi: bool | None = None
    is_required: bool | None = None
    default_value: list[str] | None = None
    options: list[Any] | None = None
    settings: Any | None = None
    validation_rules: Any | None = None
    logo_props: Any | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class WorkItemPropertyAttach(BaseModel):
    """Body for attaching one or more existing property definitions to a work item
    type (project- or workspace-scoped -- same shape both places)."""

    model_config = ConfigDict(extra="ignore")

    properties: list[str]


class WorkItemPropertyAttachResult(BaseModel):
    """Response of an attach call: the full set of property ids now attached."""

    model_config = ConfigDict(extra="allow")

    properties: list[str] = Field(default_factory=list)
