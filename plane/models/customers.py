from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator

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
    external_source: str | None = None
    external_id: str | None = None
    archived_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    logo_asset: str | None = None
    workspace: str | None = None


class CreateCustomer(BaseModel):
    """Request model for creating a customer.

    The create endpoint is an upsert. When `external_id` and `external_source`
    are both set, an existing customer matching them is updated; otherwise a
    customer with the same `name` is updated. Only when neither matches is a new
    customer created.
    """

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
    external_source: str | None = None
    external_id: str | None = None
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
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    logo_asset: str | None = None


class CustomerPropertyOption(BaseModel):
    """Customer property option model (values of an OPTION property)."""

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
    property: str | None = None
    parent: str | None = None


class CreateCustomerPropertyOption(BaseModel):
    """Request model for an OPTION property's option, sent inline on create."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    is_default: bool | None = None


class UpdateCustomerPropertyOption(BaseModel):
    """Request model for an OPTION property's option, sent inline on update.

    Set `id` to update an existing option; omit it to create a new one.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    description: str | None = None
    is_default: bool | None = None


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
    options: list[CustomerPropertyOption] | None = None

    @field_serializer("property_type")
    def serialize_property_type(self, value: PropertyType) -> str | None:
        return value.value if value else None

    @field_serializer("relation_type")
    def serialize_relation_type(self, value: RelationType) -> str | None:
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
    options: list[CreateCustomerPropertyOption] | None = None

    @field_serializer("property_type")
    def serialize_property_type(self, value: PropertyType) -> str | None:
        return value.value if value else None

    @field_serializer("relation_type")
    def serialize_relation_type(self, value: RelationType) -> str | None:
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
                    "settings with DateAttributeSettings is required for DATETIME properties"
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
    options: list[UpdateCustomerPropertyOption] | None = None

    @field_serializer("property_type")
    def serialize_property_type(self, value: PropertyType) -> str | None:
        return value.value if value else None

    @field_serializer("relation_type")
    def serialize_relation_type(self, value: RelationType) -> str | None:
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
    attachment_count: int | None = None
    created_at: str | None = None


class CreateCustomerRequest(BaseModel):
    """Request model for creating a customer request.

    `work_item_ids` links work items to the customer at creation time. It is
    write-only — the created request echoed back does not include it.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

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


class CustomerWorkItem(BaseModel):
    """A work item linked to a customer."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str | None = None
    state_id: str | None = None
    priority: str | None = None
    sequence_id: int | None = None
    project_id: str | None = None
    project_identifier: str | None = Field(None, alias="project__identifier")
    created_at: str | None = None
    updated_at: str | None = None


class LinkCustomerWorkItems(BaseModel):
    """Request model for linking work items to a customer."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    work_item_ids: list[str] = Field(..., alias="issue_ids")


class LinkedCustomerWorkItem(BaseModel):
    """A work item as echoed back by the link endpoint."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str | None = None
    sequence_id: int | None = None
    project_id: str | None = None
    project_identifier: str | None = Field(None, alias="project__identifier")


class LinkCustomerWorkItemsResponse(BaseModel):
    """Response returned when linking work items to a customer."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    message: str | None = None
    linked_work_items: list[LinkedCustomerWorkItem] = Field(
        default_factory=list, alias="linked_issues"
    )


class SetCustomerPropertyValues(BaseModel):
    """Request model for setting several customer property values at once.

    Maps property id to its list of values. Every value is sent as a string
    regardless of the property's type.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    customer_property_values: dict[str, list[str]]


class SetCustomerPropertyValue(BaseModel):
    """Request model for setting a single customer property's values."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    values: list[str]


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


class PaginatedCustomerRequestResponse(PaginatedResponse):
    """Paginated response for customer requests list endpoint.

    All pagination fields from PaginatedResponse are required.
    The results field contains the list of CustomerRequest objects.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[CustomerRequest]
