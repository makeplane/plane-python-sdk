"""Workspace-scoped work item templates (api_v2). No `use` action here -- it is
only offered on the project-scoped variant (`ProjectWorkItemTemplates.use`)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_item_templates import (
    CreateWorkItemTemplate,
    UpdateWorkItemTemplate,
    WorkItemTemplate,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkspaceWorkItemTemplates(
    V2Resource[WorkItemTemplate, CreateWorkItemTemplate, UpdateWorkItemTemplate]
):
    path = "/workspaces/{slug}/work-item-templates/"
    model = WorkItemTemplate
    operations = {
        "list": "workspace_work_item_templates_list",
        "retrieve": "workspace_work_item_templates_retrieve",
        "create": "workspace_work_item_templates_create",
        "update": "workspace_work_item_templates_partial_update",
        "delete": "workspace_work_item_templates_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItemTemplate]:
        """One page of workspace-level templates. `**filters` covers
        `is_published`, `short_id`."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkItemTemplate]:
        """Every workspace-level template, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self,
        template_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WorkItemTemplate:
        return self._retrieve(pk=template_id, params={"fields": fields})

    def create(self, data: CreateWorkItemTemplate) -> WorkItemTemplate:
        return self._create(data)

    def update(self, template_id: str, data: UpdateWorkItemTemplate) -> WorkItemTemplate:
        return self._update(data, pk=template_id)

    def delete(self, template_id: str) -> None:
        return self._delete(pk=template_id)
