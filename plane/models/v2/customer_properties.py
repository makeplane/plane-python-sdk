"""Customer property models for api_v2 -- custom-field definitions on Customer; every read field
but `id` is optional."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

CustomerPropertyType = Literal[
    "TEXT", "DATETIME", "DECIMAL", "BOOLEAN", "OPTION", "RELATION", "URL", "EMAIL", "FILE"
]
CustomerPropertyRelationType = Literal["ISSUE", "USER"]


class CreateCustomerPropertyOption(BaseModel):
    """One entry of `CreateCustomerProperty.options` / `UpdateCustomerProperty.options`
    (write-only -- the read side returns `options` as an opaque list)."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_default: bool | None = None


class CustomerProperty(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    display_name: str | None = None
    description: str | None = None
    property_type: CustomerPropertyType | None = None
    relation_type: CustomerPropertyRelationType | None = None
    is_active: bool | None = None
    is_multi: bool | None = None
    is_required: bool | None = None
    default_value: list[str] | None = None
    options: list[Any] | None = None
    logo_props: Any | None = None
    settings: Any | None = None
    validation_rules: Any | None = None
    sort_order: float | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateCustomerProperty(BaseModel):
    """POST body. `display_name` and `property_type` are required by the API."""

    model_config = ConfigDict(extra="ignore")

    display_name: str
    property_type: CustomerPropertyType
    description: str | None = None
    is_active: bool | None = None
    is_multi: bool | None = None
    is_required: bool | None = None
    default_value: list[str] | None = None
    options: list[CreateCustomerPropertyOption] | None = None
    relation_type: CustomerPropertyRelationType | None = None
    settings: Any | None = None
    logo_props: Any | None = None
    validation_rules: Any | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateCustomerProperty(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    display_name: str | None = None
    property_type: CustomerPropertyType | None = None
    description: str | None = None
    is_active: bool | None = None
    is_multi: bool | None = None
    is_required: bool | None = None
    default_value: list[str] | None = None
    options: list[CreateCustomerPropertyOption] | None = None
    relation_type: CustomerPropertyRelationType | None = None
    settings: Any | None = None
    logo_props: Any | None = None
    validation_rules: Any | None = None
    external_id: str | None = None
    external_source: str | None = None
