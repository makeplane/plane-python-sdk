"""Work item types (api_v2) -- `WorkItemTypes` (project-scoped) and
`WorkspaceWorkItemTypes` (workspace-scoped) are a different path template, not a
filtered view of each other -- each has its own operationIds. Both expose
`.properties`; `enable`/`import_types`/`schema` are project-only, and two of them
(`enable`, `import_types`) hand no `{pk}` -- they go through the kernel's
`_custom_action`/`_custom_request` against a collection-level `extra_paths`
override, not `_action`. A fetched row comes back `Loaded`
(`LoadedWorkItemType`/`LoadedWorkspaceWorkItemType`), reaching `.properties`
without repeating ids."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.work_item_types import (
    CreateWorkItemType,
    UpdateWorkItemType,
    WorkItemType,
    WorkItemTypeImport,
    WorkItemTypeSchema,
)
from .._generated.constants import (
    WorkItemTypesCreateField,
    WorkItemTypesEnableField,
    WorkItemTypesListField,
    WorkItemTypesListFilters,
    WorkItemTypesListOrderBy,
    WorkItemTypesMarkDefaultField,
    WorkItemTypesPartialUpdateField,
    WorkItemTypesRetrieveField,
    WorkItemTypesSchemaFilters,
    WorkspaceWorkItemTypesCreateField,
    WorkspaceWorkItemTypesListField,
    WorkspaceWorkItemTypesListFilters,
    WorkspaceWorkItemTypesListOrderBy,
    WorkspaceWorkItemTypesMarkDefaultField,
    WorkspaceWorkItemTypesPartialUpdateField,
    WorkspaceWorkItemTypesRetrieveField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.work_item_type import LoadedWorkItemType, LoadedWorkspaceWorkItemType
from .properties import WorkItemTypeProperties, WorkspaceWorkItemTypeProperties

__all__ = [
    "WorkItemTypeProperties",
    "WorkItemTypes",
    "WorkspaceWorkItemTypeProperties",
    "WorkspaceWorkItemTypes",
]


class WorkItemTypes(
    V2Resource[WorkItemType, CreateWorkItemType, UpdateWorkItemType],
    LoadsNavigableRows[LoadedWorkItemType],
):
    path = "/workspaces/{slug}/projects/{project_id}/work-item-types/"
    model = WorkItemType
    loaded_model = LoadedWorkItemType
    loaded_names = ("slug", "project", "type")
    extra_paths = {
        "enable": "/workspaces/{slug}/projects/{project_id}/work-item-types/enable/",
        "import_types": "/workspaces/{slug}/projects/{project_id}/work-item-types/import/",
    }
    operations = {
        "list": "work_item_types_list",
        "retrieve": "work_item_types_retrieve",
        "create": "work_item_types_create",
        "update": "work_item_types_partial_update",
        "delete": "work_item_types_destroy",
        "enable": "work_item_types_enable",
        "import_types": "work_item_types_import",
        "mark-default": "work_item_types_mark_default",
        "schema": "work_item_types_schema",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.properties = WorkItemTypeProperties(transport)

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[WorkItemTypesListField] | None = None,
        order_by: WorkItemTypesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkItemTypesListFilters],
    ) -> Page[LoadedWorkItemType]:
        """One page of work item types in this project."""
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
        fields: Sequence[WorkItemTypesListField] | None = None,
        order_by: WorkItemTypesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkItemTypesListFilters],
    ) -> Iterator[LoadedWorkItemType]:
        """Every work item type in this project, following pages automatically."""
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
        type: str,
        *,
        fields: Sequence[WorkItemTypesRetrieveField] | None = None,
    ) -> LoadedWorkItemType:
        row = self._retrieve(pk=type, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def find_by_name(self, slug: str, project: str, name: str) -> LoadedWorkItemType:
        """The one work item type with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug, project_id=project)
        return self._load(row, slug, project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateWorkItemType,
        *,
        fields: Sequence[WorkItemTypesCreateField] | None = None,
    ) -> LoadedWorkItemType:
        row = self._create(data, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def update(
        self,
        slug: str,
        project: str,
        type: str,
        data: UpdateWorkItemType,
        *,
        fields: Sequence[WorkItemTypesPartialUpdateField] | None = None,
    ) -> LoadedWorkItemType:
        row = self._update(data, pk=type, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def delete(self, slug: str, project: str, type: str) -> None:
        return self._delete(pk=type, slug=slug, project_id=project)

    def enable(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[WorkItemTypesEnableField] | None = None,
    ) -> LoadedWorkItemType:
        """Enable this project's epic/system work item type (idempotent).
        Collection-level, not per-row -- there is no `{pk}` in
        `.../work-item-types/enable/` -- so this goes through the kernel's
        `_custom_action` against the `extra_paths` override, not `_action`."""
        row = self._custom_action(
            "enable", model=self.model, params={"fields": fields}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def import_types(self, slug: str, project: str, type_ids: builtins.list[str]) -> None:
        """Import the given (global/system) work item type ids into this project.
        Collection-level (no `{pk}`), so this goes through the kernel's
        `_custom_request` against the `extra_paths` override rather than a
        hand-built URL; the response carries nothing to return."""
        self._custom_request(
            "import_types",
            data=WorkItemTypeImport(work_item_types=list(type_ids)),
            slug=slug,
            project_id=project,
        )
        return None

    def mark_default(
        self,
        slug: str,
        project: str,
        type: str,
        *,
        fields: Sequence[WorkItemTypesMarkDefaultField] | None = None,
    ) -> LoadedWorkItemType:
        """Make this the project's default work item type for new work items."""
        row = self._action(
            "mark-default", pk=type, params={"fields": fields}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def schema(
        self, slug: str, project: str, type: str, **filters: Unpack[WorkItemTypesSchemaFilters]
    ) -> WorkItemTypeSchema:
        """The type's writable standard fields (with options inline) plus its
        custom properties -- what a client needs to build a create/update form.
        The response is its own envelope (`WorkItemTypeSchema`), not a
        `WorkItemType` row, so it is not loaded -- there is nothing here for it to
        reach. A GET, unlike every other custom action on this class, so it goes
        through `_custom_action` rather than `_action`."""
        return self._custom_action(
            "schema",
            model=WorkItemTypeSchema,
            method="GET",
            pk=type,
            params=dict(filters),
            slug=slug,
            project_id=project,
        )


class WorkspaceWorkItemTypes(
    V2Resource[WorkItemType, CreateWorkItemType, UpdateWorkItemType],
    LoadsNavigableRows[LoadedWorkspaceWorkItemType],
):
    path = "/workspaces/{slug}/work-item-types/"
    model = WorkItemType
    loaded_model = LoadedWorkspaceWorkItemType
    loaded_names = ("slug", "type")
    operations = {
        "list": "workspace_work_item_types_list",
        "retrieve": "workspace_work_item_types_retrieve",
        "create": "workspace_work_item_types_create",
        "update": "workspace_work_item_types_partial_update",
        "delete": "workspace_work_item_types_destroy",
        "mark-default": "workspace_work_item_types_mark_default",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.properties = WorkspaceWorkItemTypeProperties(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceWorkItemTypesListField] | None = None,
        order_by: WorkspaceWorkItemTypesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkspaceWorkItemTypesListFilters],
    ) -> Page[LoadedWorkspaceWorkItemType]:
        """One page of work item types across the whole workspace."""
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
        )
        return self._load_page(page, slug, fields=fields)

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceWorkItemTypesListField] | None = None,
        order_by: WorkspaceWorkItemTypesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkspaceWorkItemTypesListFilters],
    ) -> Iterator[LoadedWorkspaceWorkItemType]:
        """Every work item type in the workspace, following pages automatically."""
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
        )
        return (self._load(row, slug, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        type: str,
        *,
        fields: Sequence[WorkspaceWorkItemTypesRetrieveField] | None = None,
    ) -> LoadedWorkspaceWorkItemType:
        row = self._retrieve(pk=type, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def find_by_name(self, slug: str, name: str) -> LoadedWorkspaceWorkItemType:
        """The one workspace-level type with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug)
        return self._load(row, slug)

    def create(
        self,
        slug: str,
        data: CreateWorkItemType,
        *,
        fields: Sequence[WorkspaceWorkItemTypesCreateField] | None = None,
    ) -> LoadedWorkspaceWorkItemType:
        row = self._create(data, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def update(
        self,
        slug: str,
        type: str,
        data: UpdateWorkItemType,
        *,
        fields: Sequence[WorkspaceWorkItemTypesPartialUpdateField] | None = None,
    ) -> LoadedWorkspaceWorkItemType:
        row = self._update(data, pk=type, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def delete(self, slug: str, type: str) -> None:
        return self._delete(pk=type, slug=slug)

    def mark_default(
        self,
        slug: str,
        type: str,
        *,
        fields: Sequence[WorkspaceWorkItemTypesMarkDefaultField] | None = None,
    ) -> LoadedWorkspaceWorkItemType:
        """Make this the workspace's default work item type."""
        row = self._action("mark-default", pk=type, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)
