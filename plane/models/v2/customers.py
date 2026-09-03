"""Customer models for api_v2; unlike work items, every write field here is id-based with no
readable-name companions."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Customer(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: Any | None = None
    description_html: str | None = None
    domain: str | None = None
    email: str | None = None
    employees: int | None = None
    revenue: str | None = None
    stage: str | None = None
    contract_status: str | None = None
    website_url: str | None = None
    logo_asset_id: str | None = None
    logo_props: Any | None = None
    logo_url: str | None = None
    customer_request_count: int | None = None
    archived_at: datetime | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateCustomer(BaseModel):
    """POST body. `name` is the only field the API requires."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: Any | None = None
    description_html: str | None = None
    domain: str | None = None
    email: str | None = None
    employees: int | None = None
    revenue: str | None = None
    stage: str | None = None
    contract_status: str | None = None
    website_url: str | None = None
    logo_props: Any | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateCustomer(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description: Any | None = None
    description_html: str | None = None
    domain: str | None = None
    email: str | None = None
    employees: int | None = None
    revenue: str | None = None
    stage: str | None = None
    contract_status: str | None = None
    website_url: str | None = None
    logo_props: Any | None = None
    external_id: str | None = None
    external_source: str | None = None


class CustomerRequest(BaseModel):
    """A request a customer has raised, optionally linked to work items via
    `CreateCustomerRequest.work_item_ids` (write-only -- not echoed back here)."""

    model_config = ConfigDict(extra="allow")

    id: str
    customer_id: str | None = None
    name: str | None = None
    description: Any | None = None
    description_html: str | None = None
    link: str | None = None
    archived_at: datetime | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateCustomerRequest(BaseModel):
    """POST body; `name` is required, `work_item_ids` links work items on create (write-only)."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: Any | None = None
    description_html: str | None = None
    link: str | None = None
    work_item_ids: list[str] | None = None


class UpdateCustomerRequest(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description: Any | None = None
    description_html: str | None = None
    link: str | None = None
    work_item_ids: list[str] | None = None


class CustomerPropertyValueMap(BaseModel):
    """Property values keyed by property id (dynamic mapping, access via `.model_extra`); every
    value serializes as `list[str]`."""

    model_config = ConfigDict(extra="allow")


class CreateCustomerPropertyValues(BaseModel):
    """POST body for `customer_property_values_create`: bulk-set. Acts as an
    upsert -- the properties named are given these values, replacing any they
    already held; properties absent from `values` are untouched."""

    model_config = ConfigDict(extra="ignore")

    values: dict[str, list[str]]


class CustomerWorkItemManageRequest(BaseModel):
    """Body of the `Customers.work_items` bridge (`add`/`remove`): work item ids
    to link/unlink from this customer. Both lists are optional; omit either to
    leave that side unchanged."""

    model_config = ConfigDict(extra="ignore")

    add: list[str] | None = None
    remove: list[str] | None = None


class CustomerWorkItemManageResponse(BaseModel):
    """The ids actually added/removed by a `Customers.work_items` bridge call."""

    model_config = ConfigDict(extra="allow")

    added: list[str] = []
    removed: list[str] = []
