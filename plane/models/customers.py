from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer, model_validator

from .enums import PropertyType, RelationType
from .pagination import PaginatedResponse
from .work_item_property_configurations import (
    DateAttributeSettings,
    TextAttributeSettings,
)

PropertySettings = TextAttributeSettings | DateAttributeSettings | None


class Customer(BaseModel):
    """Customer model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    deleted_at: str | None = None
    customer_request_count: int | None = None
    logo_url: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    name: str
    description: Any | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    description_binary: str | None = None
    email: str | None = None
    website_url: str | None = None
    logo_props: Any | None = None
    domain: str | None = None
    employees: int | None = None
    stage: str | None = None
    contract_status: str | None = None
    revenue: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    logo_asset: str | None = None
    workspace: str | None = None


class CreateCustomer(BaseModel):
    """Request model for creating a customer."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: Any | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    email: str | None = None
    website_url: str | None = None
    logo_props: Any | None = None
    domain: str | None = None
    employees: int | None = None
    stage: str | None = None
    contract_status: str | None = None
    revenue: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    logo_asset: str | None = None


class UpdateCustomer(BaseModel):
    """Request model for updating a customer."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: Any | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    email: str | None = None
    website_url: str | None = None
    logo_props: Any | None = None
    domain: str | None = None
    employees: int | None = None
    stage: str | None = None
    contract_status: str | None = None
    revenue: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    logo_asset: str | None = None


class CustomerProperty(BaseModel):
    """Customer property model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    deleted_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    name: str | None = None
    display_name: str
    description: str | None = None
    logo_props: Any | None = None
    sort_order: float | None = None
    property_type: PropertyType
    relation_type: RelationType | None = None
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

    @field_serializer("property_type")
    def serialize_property_type(self, value: PropertyType) -> str:
        return value.value if value else None

    @field_serializer("relation_type")
    def serialize_relation_type(self, value: RelationType) -> str:
        return value.value if value else None


class CreateCustomerProperty(BaseModel):
    """Request model for creating a customer property."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    display_name: str
    description: str | None = None
    logo_props: Any | None = None
    sort_order: float | None = None
    property_type: PropertyType
    relation_type: RelationType | None = None
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
    def validate_settings_and_relation_type(self) -> "CreateCustomerProperty":
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


class UpdateCustomerProperty(BaseModel):
    """Request model for updating customer property."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    display_name: str | None = None
    description: str | None = None
    logo_props: Any | None = None
    sort_order: float | None = None
    property_type: PropertyType | None = None
    relation_type: RelationType | None = None
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

    @field_serializer("property_type")
    def serialize_property_type(self, value: PropertyType) -> str:
        return value.value if value else None

    @field_serializer("relation_type")
    def serialize_relation_type(self, value: RelationType) -> str:
        return value.value if value else None

    @model_validator(mode="after")
    def validate_settings_and_relation_type(self) -> "UpdateCustomerProperty":
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


class CustomerRequest(BaseModel):
    """Customer request model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str
    description: Any | None = None
    description_html: str | None = None
    link: str | None = None
    work_item_ids: list[str] | None = None


class UpdateCustomerRequest(BaseModel):
    """Request model for updating customer request."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: Any | None = None
    description_html: str | None = None
    link: str | None = None
    work_item_ids: list[str] | None = None


class PaginatedCustomerResponse(PaginatedResponse):
    """Paginated response for customers list endpoint.

    All pagination fields from PaginatedResponse are required.
    The results field contains the list of Customer objects.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Customer]


class PaginatedCustomerPropertyResponse(PaginatedResponse):
    """Paginated response for customer properties list endpoint.

    All pagination fields from PaginatedResponse are required.
    The results field contains the list of CustomerProperty objects.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[CustomerProperty]
