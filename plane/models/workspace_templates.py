"""Models for workspace-level templates.

Work item and page template models are reused from project_templates.
This module provides project template models which are workspace-specific.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict


class WorkItemTemplate(BaseModel):
    """Workspace work item template response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    description: str | None = None
    description_html: str | None = None
    template_data: Any | None = None
    logo_props: Any | None = None
    created_at: str | None = None
    updated_at: str | None = None
    workspace: str | None = None


class CreateWorkItemTemplate(BaseModel):
    """Request model for creating a workspace work item template."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    description_html: str | None = None
    template_data: Any | None = None
    logo_props: Any | None = None


class UpdateWorkItemTemplate(BaseModel):
    """Request model for updating a workspace work item template."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    description_html: str | None = None
    template_data: Any | None = None
    logo_props: Any | None = None


class ProjectTemplate(BaseModel):
    """Workspace project template response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    description: str | None = None
    logo_props: Any | None = None
    template_data: Any | None = None
    created_at: str | None = None
    updated_at: str | None = None
    workspace: str | None = None


class CreateProjectTemplate(BaseModel):
    """Request model for creating a workspace project template."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    logo_props: Any | None = None
    template_data: Any | None = None


class UpdateProjectTemplate(BaseModel):
    """Request model for updating a workspace project template."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    logo_props: Any | None = None
    template_data: Any | None = None


class PageTemplate(BaseModel):
    """Workspace page template response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    description: str | None = None
    description_html: str | None = None
    template_data: Any | None = None
    logo_props: Any | None = None
    created_at: str | None = None
    updated_at: str | None = None
    workspace: str | None = None


class CreatePageTemplate(BaseModel):
    """Request model for creating a workspace page template."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    description_html: str | None = None
    template_data: Any | None = None
    logo_props: Any | None = None


class UpdatePageTemplate(BaseModel):
    """Request model for updating a workspace page template."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    description_html: str | None = None
    template_data: Any | None = None
    logo_props: Any | None = None
