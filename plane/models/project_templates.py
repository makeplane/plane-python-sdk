from typing import Any

from pydantic import BaseModel, ConfigDict


class WorkItemTemplate(BaseModel):
    """Work item template model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str
    short_description: str | None = None
    template_data: dict[str, Any] | None = None
    template_type: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    project: str | None = None
    workspace: str | None = None


class CreateWorkItemTemplate(BaseModel):
    """Request model for creating a work item template."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    short_description: str | None = None
    template_data: dict[str, Any] | None = None


class UpdateWorkItemTemplate(BaseModel):
    """Request model for updating a work item template."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    short_description: str | None = None
    template_data: dict[str, Any] | None = None


class PageTemplate(BaseModel):
    """Page template model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str
    short_description: str | None = None
    template_data: dict[str, Any] | None = None
    template_type: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    project: str | None = None
    workspace: str | None = None


class CreatePageTemplate(BaseModel):
    """Request model for creating a page template."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    short_description: str | None = None
    template_data: dict[str, Any] | None = None


class UpdatePageTemplate(BaseModel):
    """Request model for updating a page template."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    short_description: str | None = None
    template_data: dict[str, Any] | None = None
