"""Estimate + estimate point models for api_v2; every read field but `id` is optional."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

EstimateType = Literal["categories", "points", "time"]


class EstimatePoint(BaseModel):
    """One point/category/time value belonging to an estimate."""

    model_config = ConfigDict(extra="allow")

    id: str
    key: int | None = None
    value: str | None = None
    description: str | None = None
    estimate_id: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class Estimate(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = None
    type: EstimateType | None = None
    last_used: bool | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    points: list[EstimatePoint] | None = None
    """Populated only when the request set `expand=["points"]`."""


class CreateEstimate(BaseModel):
    """POST body. `name` is required by the API."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None
    type: EstimateType | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateEstimate(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description: str | None = None
    type: EstimateType | None = None
    external_id: str | None = None
    external_source: str | None = None


class CreateEstimatePoint(BaseModel):
    """POST body. `value` is required by the API."""

    model_config = ConfigDict(extra="ignore")

    value: str
    key: int | None = None
    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateEstimatePoint(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    value: str | None = None
    key: int | None = None
    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None
