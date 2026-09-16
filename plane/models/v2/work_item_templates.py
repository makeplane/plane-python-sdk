"""Work item template models for api_v2; every read field but `id` is optional."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .work_items import Priority


class WorkItemTemplateData(BaseModel):
    """Seed payload for a template's work item;
    `assignees`/`labels`/`modules`/`properties`/`state`/`type` are schemaless, left as opaque
    JSON."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description_html: str | None = None
    priority: Priority | None = None
    assignees: object | None = None
    labels: object | None = None
    modules: object | None = None
    properties: object | None = None
    state: object | None = None
    type: object | None = None


class WorkItemTemplate(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description_html: str | None = None
    short_description: str | None = None
    short_id: str | None = None
    slug: str | None = None
    template_type: str | None = None
    template_data: dict[str, object] | None = None
    is_published: bool | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateWorkItemTemplate(BaseModel):
    """POST body. `name` and `template_data` are required by the API."""

    model_config = ConfigDict(extra="ignore")

    name: str
    template_data: WorkItemTemplateData
    description_html: str | None = None
    short_description: str | None = None
    is_published: bool | None = None


class UpdateWorkItemTemplate(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    template_data: WorkItemTemplateData | None = None
    description_html: str | None = None
    short_description: str | None = None
    is_published: bool | None = None


class WorkItemTemplateUse(BaseModel):
    """Body for `POST .../work-item-templates/{id}/use/` -- optional overrides.
    Both fields are optional; omit either to take the template's own value (and,
    for `project_id`, the project already named in the URL)."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    project_id: str | None = None
