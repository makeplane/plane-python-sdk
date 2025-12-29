from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator

from .enums import PropertyType, RelationType
from .work_item_property_configurations import (
    DateAttributeSettings,
    TextAttributeSettings,
)

# Settings type used by TEXT and DATETIME properties
PropertySettings = TextAttributeSettings | DateAttributeSettings | None


class WorkItemProperty(BaseModel):
    """Work item property model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

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
    settings: PropertySettings | dict = None
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
    options: list["WorkItemPropertyOption"] | None = None

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
    options: list["CreateWorkItemPropertyOption"] | None = None

    @field_serializer("property_type")
    def serialize_property_type(self, value: PropertyType) -> str:
        return value.value if value else None

    @field_serializer("relation_type")
    def serialize_relation_type(self, value: RelationType) -> str:
        return value.value if value else None

    @model_validator(mode="after")
    def validate_settings_and_relation_type(self) -> "CreateWorkItemProperty":
        """Validate settings and relation_type based on property_type."""
        prop_type = self.property_type
        settings = self.settings
        relation_type = self.relation_type

        # TEXT properties require TextAttributeSettings
        if prop_type == PropertyType.TEXT:
            if settings is None:
                raise ValueError(
                    "settings with TextAttributeSettings is required for TEXT properties"
                )
            if not isinstance(settings, TextAttributeSettings):
                raise ValueError("settings must be TextAttributeSettings for TEXT properties")

        # DATETIME properties require DateAttributeSettings
        if prop_type == PropertyType.DATETIME:
            if settings is None:
                raise ValueError(
                    "settings with DateAttributeSettings is required for DATETIME " "properties"
                )
            if not isinstance(settings, DateAttributeSettings):
                raise ValueError("settings must be DateAttributeSettings for DATETIME properties")

        # RELATION properties require relation_type
        if prop_type == PropertyType.RELATION:
            if relation_type is None:
                raise ValueError("relation_type is required for RELATION properties")

        return self


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

    @model_validator(mode="after")
    def validate_settings_and_relation_type(self) -> "UpdateWorkItemProperty":
        """Validate settings and relation_type when property_type is updated."""
        prop_type = self.property_type
        settings = self.settings
        relation_type = self.relation_type

        # Only validate if property_type is being updated
        if prop_type is None:
            return self

        # TEXT properties require TextAttributeSettings
        if prop_type == PropertyType.TEXT:
            if settings is None:
                raise ValueError(
                    "settings with TextAttributeSettings is required when updating to "
                    "TEXT property_type"
                )
            if not isinstance(settings, TextAttributeSettings):
                raise ValueError("settings must be TextAttributeSettings for TEXT properties")

        # DATETIME properties require DateAttributeSettings
        if prop_type == PropertyType.DATETIME:
            if settings is None:
                raise ValueError(
                    "settings with DateAttributeSettings is required when updating to "
                    "DATETIME property_type"
                )
            if not isinstance(settings, DateAttributeSettings):
                raise ValueError("settings must be DateAttributeSettings for DATETIME properties")

        # RELATION properties require relation_type
        if prop_type == PropertyType.RELATION:
            if relation_type is None:
                raise ValueError(
                    "relation_type is required when updating to RELATION property_type"
                )

        return self


class WorkItemPropertyOption(BaseModel):
    """Work item property option model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

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

    model_config = ConfigDict(extra="allow", populate_by_name=True)

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
    """Request model for creating/updating a work item property value.

    The value type depends on the property type:
    - TEXT/URL/EMAIL/FILE: string
    - DATETIME: string (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
    - DECIMAL: number (int or float)
    - BOOLEAN: boolean (true/false)
    - OPTION/RELATION (single): string (UUID)
    - OPTION/RELATION (multi, when is_multi=True): list of strings (UUIDs) or single string

    For multi-value properties (is_multi=True):
    - Accept either a single UUID string or a list of UUID strings
    - Multiple IssuePropertyValue records are created
    - Response will be a list of values

    For single-value properties:
    - Only one value is allowed per work item/property combination
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    value: str | bool | int | float | list[str] = Field(
        ..., description="The value to set for the property (type depends on property type)"
    )
    external_id: str | None = Field(None, description="Optional external identifier for syncing")
    external_source: str | None = Field(
        None, description="Optional external source (e.g., 'github', 'jira')"
    )


class WorkItemPropertyValueDetail(BaseModel):
    """Detailed work item property value response.

    Provides a clean response structure with the value extracted
    and formatted according to property type.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(..., description="Unique identifier for this property value")
    property_id: str = Field(..., description="ID of the property")
    issue_id: str = Field(..., description="ID of the work item")
    value: str | bool | float | None = Field(
        ..., description="The actual value, formatted according to property type"
    )
    value_type: str | None = Field(None, description="Type of the value")
    external_id: str | None = Field(
        None, description="External identifier if synced with external system"
    )
    external_source: str | None = Field(
        None, description="External source identifier (e.g., 'github', 'jira')"
    )
    created_at: str | None = Field(None, description="Timestamp when created")
    updated_at: str | None = Field(None, description="Timestamp when last updated")
