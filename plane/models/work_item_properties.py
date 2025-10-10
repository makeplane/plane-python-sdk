from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from .enums import PropertyType, RelationType
from .work_item_property_configurations import (
    DateAttributeSettings,
    TextAttributeSettings,
)

# Settings type used by TEXT and DATETIME properties
PropertySettings = TextAttributeSettings | DateAttributeSettings | None


class WorkItemProperty(BaseModel):
    """Work item property model."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str | None = None
    deleted_at: str | None = None
    relation_type: RelationType | None = None
    created_at: str | None = None
    updated_at: str | None = None
    name: str | None = None
    display_name: str
    description: str | None = None
    logo_props: Any | None = None
    sort_order: float | None = None
    property_type: PropertyType
    is_required: bool | None = None
    default_value: list[str] | None = None
    settings: PropertySettings = None
    is_active: bool | None = None
    is_multi: bool | None = None
    validation_rules: Any | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    workspace: str | None = None
    project: str | None = None
    issue_type: str | None = None

    @field_serializer("property_type")
    def serialize_property_type(self, value: PropertyType) -> str:
        return value.value if value else None

    @field_serializer("relation_type")
    def serialize_relation_type(self, value: RelationType) -> str:
        return value.value if value else None


class CreateWorkItemProperty(BaseModel):
    """Request model for creating a work item property."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    relation_type: RelationType | None = None
    display_name: str
    description: str | None = None
    property_type: PropertyType
    is_required: bool | None = None
    default_value: list[str] | None = None
    settings: PropertySettings = None
    is_active: bool | None = None
    is_multi: bool | None = None
    validation_rules: Any | None = None
    external_source: str | None = None
    external_id: str | None = None

    @field_serializer("property_type")
    def serialize_property_type(self, value: PropertyType) -> str:
        return value.value if value else None

    @field_serializer("relation_type")
    def serialize_relation_type(self, value: RelationType) -> str:
        return value.value if value else None


class UpdateWorkItemProperty(BaseModel):
    """Request model for updating a work item property."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    relation_type: RelationType | None = None
    display_name: str | None = None
    description: str | None = None
    property_type: PropertyType | None = None
    is_required: bool | None = None
    default_value: list[str] | None = None
    settings: PropertySettings = None
    is_active: bool | None = None
    is_multi: bool | None = None
    validation_rules: Any | None = None
    external_source: str | None = None
    external_id: str | None = None

    @field_serializer("property_type")
    def serialize_property_type(self, value: PropertyType) -> str:
        return value.value if value else None

    @field_serializer("relation_type")
    def serialize_relation_type(self, value: RelationType) -> str:
        return value.value if value else None


class WorkItemPropertyOption(BaseModel):
    """Work item property option model."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str | None = None
    deleted_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    name: str
    sort_order: float | None = None
    description: str | None = None
    logo_props: Any | None = None
    is_active: bool | None = None
    is_default: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    workspace: str | None = None
    project: str | None = None
    property: str | None = None
    parent: str | None = None


class CreateWorkItemPropertyOption(BaseModel):
    """Request model for creating a work item property option."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    is_active: bool | None = None
    is_default: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    parent: str | None = None


class UpdateWorkItemPropertyOption(BaseModel):
    """Request model for updating a work item property option."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    is_default: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    parent: str | None = None


class WorkItemPropertyValue(BaseModel):
    """Work item property value model."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str | None = None
    deleted_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    value_text: str | None = None
    value_boolean: bool | None = None
    value_decimal: float | None = None
    value_datetime: str | None = None
    value_uuid: str | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    workspace: str | None = None
    project: str | None = None
    issue: str
    property: str
    value_option: str | None = None


class CreateWorkItemPropertyValue(BaseModel):
    """Request model for creating/updating work item property values.

    Matches API shape: { "values": [ { "value": str, "external_id"?: str, "external_source"?: str } ] }
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    class ValueItem(BaseModel):
        model_config = ConfigDict(extra="ignore", populate_by_name=True)

        value: str
        external_id: str | None = None
        external_source: str | None = None

    values: list[ValueItem]


class WorkItemPropertyValueDetail(BaseModel):
    """Detailed work item property value."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    property_id: str = Field(..., description="The ID of the issue property")
    values: list[str] = Field(
        ...,
        description="List of aggregated property values for the given property",
    )
