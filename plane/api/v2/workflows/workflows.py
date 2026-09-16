"""Workflows (api_v2) -- a project's per-work-item-type workflow configuration,
with nested `.states`/`.transitions`. No `upsert`/bulk operations -- CRUD-only. A
fetched row comes back `Loaded` (`LoadedWorkflow`), reaching `.states` and
`.transitions` without repeating ids."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.workflows import CreateWorkflow, UpdateWorkflow, Workflow
from .._generated.constants import (
    WorkflowsCreateField,
    WorkflowsListField,
    WorkflowsListFilters,
    WorkflowsListOrderBy,
    WorkflowsPartialUpdateField,
    WorkflowsRetrieveField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.workflow import LoadedWorkflow
from .states import WorkflowStates
from .transitions import WorkflowTransitions

__all__ = ["WorkflowStates", "WorkflowTransitions", "Workflows"]


class Workflows(
    V2Resource[Workflow, CreateWorkflow, UpdateWorkflow],
    LoadsNavigableRows[LoadedWorkflow],
):
    path = "/workspaces/{slug}/projects/{project_id}/workflows/"
    model = Workflow
    loaded_model = LoadedWorkflow
    loaded_names = ("slug", "project", "workflow")
    operations = {
        "list": "workflows_list",
        "retrieve": "workflows_retrieve",
        "create": "workflows_create",
        "update": "workflows_partial_update",
        "delete": "workflows_destroy",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.states = WorkflowStates(transport)
        self.transitions = WorkflowTransitions(transport)

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[WorkflowsListField] | None = None,
        order_by: WorkflowsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkflowsListFilters],
    ) -> Page[LoadedWorkflow]:
        """One page of workflows in this project.

        `**filters` covers `search`."""
        page = self._list(
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
            project_id=project,
        )
        return self._load_page(page, slug, project, fields=fields)

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[WorkflowsListField] | None = None,
        order_by: WorkflowsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkflowsListFilters],
    ) -> Iterator[LoadedWorkflow]:
        """Every workflow in this project, following pages automatically."""
        rows = self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
            project_id=project,
        )
        return (self._load(row, slug, project, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        project: str,
        workflow: str,
        *,
        fields: Sequence[WorkflowsRetrieveField] | None = None,
    ) -> LoadedWorkflow:
        row = self._retrieve(pk=workflow, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def find_by_name(self, slug: str, project: str, name: str) -> LoadedWorkflow:
        """The one workflow with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug, project_id=project)
        return self._load(row, slug, project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateWorkflow,
        *,
        fields: Sequence[WorkflowsCreateField] | None = None,
    ) -> LoadedWorkflow:
        row = self._create(data, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def update(
        self,
        slug: str,
        project: str,
        workflow: str,
        data: UpdateWorkflow,
        *,
        fields: Sequence[WorkflowsPartialUpdateField] | None = None,
    ) -> LoadedWorkflow:
        row = self._update(
            data, pk=workflow, params={"fields": fields}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def delete(self, slug: str, project: str, workflow: str) -> None:
        return self._delete(pk=workflow, slug=slug, project_id=project)
