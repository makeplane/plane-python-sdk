"""Workspace-scoped work item templates (api_v2). No `use` action here -- it is
only offered on the project-scoped variant (`ProjectWorkItemTemplates.use`)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.work_item_templates import (
    CreateWorkItemTemplate,
    UpdateWorkItemTemplate,
    WorkItemTemplate,
)
from .._generated.constants import (
    WorkspaceWorkItemTemplatesCreateField,
    WorkspaceWorkItemTemplatesListField,
    WorkspaceWorkItemTemplatesListFilters,
    WorkspaceWorkItemTemplatesListOrderBy,
    WorkspaceWorkItemTemplatesPartialUpdateField,
    WorkspaceWorkItemTemplatesRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
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
        slug: str,
        *,
        fields: Sequence[WorkspaceWorkItemTemplatesListField] | None = None,
        order_by: WorkspaceWorkItemTemplatesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkspaceWorkItemTemplatesListFilters],
    ) -> Page[WorkItemTemplate]:
        """One page of workspace-level templates. `**filters` covers
        `is_published`, `short_id`."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceWorkItemTemplatesListField] | None = None,
        order_by: WorkspaceWorkItemTemplatesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkspaceWorkItemTemplatesListFilters],
    ) -> Iterator[WorkItemTemplate]:
        """Every workspace-level template, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )

    def retrieve(
        self,
        slug: str,
        template: str,
        *,
        fields: Sequence[WorkspaceWorkItemTemplatesRetrieveField] | None = None,
    ) -> WorkItemTemplate:
        return self._retrieve(pk=template, params={"fields": fields}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateWorkItemTemplate,
        *,
        fields: Sequence[WorkspaceWorkItemTemplatesCreateField] | None = None,
    ) -> WorkItemTemplate:
        return self._create(data, params={"fields": fields}, slug=slug)

    def update(
        self,
        slug: str,
        template: str,
        data: UpdateWorkItemTemplate,
        *,
        fields: Sequence[WorkspaceWorkItemTemplatesPartialUpdateField] | None = None,
    ) -> WorkItemTemplate:
        return self._update(data, pk=template, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, template: str) -> None:
        return self._delete(pk=template, slug=slug)
