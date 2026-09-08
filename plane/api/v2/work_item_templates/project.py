"""Project-scoped work item templates (api_v2)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.work_item_templates import (
    CreateWorkItemTemplate,
    UpdateWorkItemTemplate,
    WorkItemTemplate,
    WorkItemTemplateUse,
)
from ....models.v2.work_items import WorkItem
from .._generated.constants import (
    ProjectWorkItemTemplatesCreateField,
    ProjectWorkItemTemplatesListField,
    ProjectWorkItemTemplatesListFilters,
    ProjectWorkItemTemplatesListOrderBy,
    ProjectWorkItemTemplatesPartialUpdateField,
    ProjectWorkItemTemplatesRetrieveField,
    WorkItemsUseField,
)
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
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectWorkItemTemplatesListField] | None = None,
        order_by: ProjectWorkItemTemplatesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[ProjectWorkItemTemplatesListFilters],
    ) -> Page[WorkItemTemplate]:
        """One page of templates in this project. `**filters` covers
        `is_published`, `short_id`."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
            project_id=project,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectWorkItemTemplatesListField] | None = None,
        order_by: ProjectWorkItemTemplatesListOrderBy | None = None,
        **filters: Unpack[ProjectWorkItemTemplatesListFilters],
    ) -> Iterator[WorkItemTemplate]:
        """Every template in this project, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        template: str,
        *,
        fields: Sequence[ProjectWorkItemTemplatesRetrieveField] | None = None,
    ) -> WorkItemTemplate:
        return self._retrieve(pk=template, params={"fields": fields}, slug=slug, project_id=project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateWorkItemTemplate,
        *,
        fields: Sequence[ProjectWorkItemTemplatesCreateField] | None = None,
    ) -> WorkItemTemplate:
        return self._create(data, params={"fields": fields}, slug=slug, project_id=project)

    def update(
        self,
        slug: str,
        project: str,
        template: str,
        data: UpdateWorkItemTemplate,
        *,
        fields: Sequence[ProjectWorkItemTemplatesPartialUpdateField] | None = None,
    ) -> WorkItemTemplate:
        return self._update(
            data, pk=template, params={"fields": fields}, slug=slug, project_id=project
        )

    def delete(self, slug: str, project: str, template: str) -> None:
        return self._delete(pk=template, slug=slug, project_id=project)

    # -- Custom action --------------------------------------------------------
    # Not an `_action` call: `use` returns a `WorkItem`, not this resource's own `model`.

    def use(
        self,
        slug: str,
        project: str,
        template: str,
        data: WorkItemTemplateUse | None = None,
        *,
        fields: Sequence[WorkItemsUseField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItem:
        """Instantiate a work item from this template. `data` optionally overrides
        `name`/`project_id`; omit for the template's own values."""
        return self._custom_action(
            "use",
            model=WorkItem,
            pk=template,
            data=data,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )
