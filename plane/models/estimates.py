from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Estimate(BaseModel):
    """Estimate response model.

    Represents the sizing scale configured for a project
    (categories, points, or time).
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str
    description: str | None = None
    type: str | None = None  # "categories" | "points" | "time"
    last_used: bool | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None


class CreateEstimate(BaseModel):
    """Request model for creating an estimate."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    type: str | None = None  # "categories" | "points" | "time"
    last_used: bool = True
    external_id: str | None = None
    external_source: str | None = None


class UpdateEstimate(BaseModel):
    """Request model for updating an estimate.

    Only name, description, external_id, and external_source are updatable.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None


class EstimatePoint(BaseModel):
    """Estimate point response model.

    Represents an individual value within an estimate scale
    (e.g., "1", "2", "3" for story points).
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    estimate: str | None = None
    key: int | None = None
    value: str
    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None


class CreateEstimatePoint(BaseModel):
    """Request model for creating a single estimate point.

    Used inside a list when calling create_points().
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    value: str = Field(..., max_length=20)
    key: int | None = None
    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateEstimatePoint(BaseModel):
    """Request model for updating an estimate point."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    key: int | None = None
    value: str | None = Field(default=None, max_length=20)
    description: str | None = None
    external_id: str | None = None
    external_source: str | None = None
