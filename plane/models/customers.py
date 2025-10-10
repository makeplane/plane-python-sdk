from typing import Any

from pydantic import BaseModel, ConfigDict

from .enums import PropertyTypeEnum, RelationTypeEnum


class Customer(BaseModel):
    """Customer model."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

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

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str | None = None
    deleted_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    name: str | None = None
    display_name: str
    description: str | None = None
    logo_props: Any | None = None
    sort_order: float | None = None
    property_type: PropertyTypeEnum
    relation_type: RelationTypeEnum | None = None
    is_required: bool | None = None
    default_value: list[str] | None = None
    settings: Any | None = None
    is_active: bool | None = None
    is_multi: bool | None = None
    validation_rules: Any | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    workspace: str | None = None


class UpdateCustomerProperty(BaseModel):
    """Request model for updating customer property."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    display_name: str | None = None
    description: str | None = None
    logo_props: Any | None = None
    sort_order: float | None = None
    property_type: PropertyTypeEnum | None = None
    relation_type: RelationTypeEnum | None = None
    is_required: bool | None = None
    default_value: list[str] | None = None
    settings: Any | None = None
    is_active: bool | None = None
    is_multi: bool | None = None
    validation_rules: Any | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None


class CustomerRequest(BaseModel):
    """Customer request model."""

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
