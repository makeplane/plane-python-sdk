"""Project-scoped work item templates (api_v2)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_item_templates import (
    CreateWorkItemTemplate,
    UpdateWorkItemTemplate,
    WorkItemTemplate,
    WorkItemTemplateUse,
)
from ....models.v2.work_items import WorkItem
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class ProjectWorkItemTemplates(
    V2Resource[WorkItemTemplate, CreateWorkItemTemplate, UpdateWorkItemTemplate]
):
    """Project-scoped work item templates, plus `use` (instantiate a work item
    from a template in one call)."""

    path = "/workspaces/{slug}/projects/{project_id}/work-item-templates/"
    model = WorkItemTemplate
    operations = {
        "list": "project_work_item_templates_list",
        "retrieve": "project_work_item_templates_retrieve",
        "create": "project_work_item_templates_create",
        "update": "project_work_item_templates_partial_update",
        "use": "work_items_use",
        "delete": "project_work_item_templates_destroy",
    }

    def list(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Page[WorkItemTemplate]:
        """One page of templates in this project. `**filters` covers
        `is_published`, `short_id`."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[WorkItemTemplate]:
        """Every template in this project, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self, template_id: str, *, fields: Sequence[str] | None = None
    ) -> WorkItemTemplate:
        return self._retrieve(pk=template_id, params={"fields": fields})

    def create(self, data: CreateWorkItemTemplate) -> WorkItemTemplate:
        return self._create(data)

    def update(self, template_id: str, data: UpdateWorkItemTemplate) -> WorkItemTemplate:
        return self._update(data, pk=template_id)

    def delete(self, template_id: str) -> None:
        return self._delete(pk=template_id)

    # -- Custom action --------------------------------------------------------
    # Not an `_action` call: `use` returns a `WorkItem`, not this resource's own `model`.

    def use(
        self,
        template_id: str,
        data: WorkItemTemplateUse | None = None,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItem:
        """Instantiate a work item from this template. `data` optionally overrides
        `name`/`project_id`; omit for the template's own values."""
        payload = self.transport.request(
            "POST",
            f"{self._detail_url(template_id)}use/",
            params=self._query({"fields": fields, "expand": expand}, action="use"),
            json=data.model_dump(mode="json", exclude_none=True) if data is not None else None,
        )
        return WorkItem.model_validate(payload)
