"""Models for releases."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class Release(BaseModel):
    """Release response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    description: str | None = None
    start_date: str | None = None
    release_date: str | None = None
    status: str | None = None
    logo_props: Any | None = None
    created_at: str | None = None
    updated_at: str | None = None
    workspace: str | None = None


class CreateRelease(BaseModel):
    """Request model for creating a release."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    start_date: str | None = None
    release_date: str | None = None
    status: str | None = None
    logo_props: Any | None = None


class UpdateRelease(BaseModel):
    """Request model for updating a release."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    start_date: str | None = None
    release_date: str | None = None
    status: str | None = None
    logo_props: Any | None = None


class ReleaseTag(BaseModel):
    """Release tag response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    color: str | None = None
    sort_order: float | None = None
    workspace: str | None = None


class CreateReleaseTag(BaseModel):
    """Request model for creating a release tag."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    color: str | None = None


class ReleaseLabel(BaseModel):
    """Release label response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    color: str | None = None
    sort_order: float | None = None
    workspace: str | None = None


class CreateReleaseLabel(BaseModel):
    """Request model for creating a release label."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    color: str | None = None


class AddReleaseItemLabel(BaseModel):
    """Request model for adding labels to a release item."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    label_ids: list[str]
