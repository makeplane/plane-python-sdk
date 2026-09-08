"""Project modules (api_v2). Module membership (`member_ids`) is read-only:
the golden's `ModuleWriteRequest` has no writable member field; work item
membership is the `.work_items` bridge (`add`/`remove`).

A fetched row (`retrieve`/`create`, and every row in a `list` page) comes back as a
`LoadedModule`: it carries the row's data and can reach `.work_items.add(...)`
without the caller repeating `slug`/`project`/`module`."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence

from typing_extensions import Unpack

from ...models.v2.common import BulkWriteResponse
from ...models.v2.module_work_items import (
    ModuleWorkItemManageRequest,
    ModuleWorkItemManageResponse,
)
from ...models.v2.modules import CreateModule, Module, UpdateModule
from ._generated.constants import (
    ModulesCreateField,
    ModulesListField,
    ModulesListFilters,
    ModulesListOrderBy,
    ModulesPartialUpdateField,
    ModulesRetrieveField,
    ModulesUpsertField,
)
from ._kernel.loaded import LoadsNavigableRows
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport
from ._loaded.module import LoadedModule


class ModuleWorkItems(
    V2Resource[
        ModuleWorkItemManageResponse, ModuleWorkItemManageRequest, ModuleWorkItemManageRequest
    ]
):
    """Membership bridge between a module and work items: `add` links work items
    to the module, `remove` unlinks them. Both POST to
    `.../modules/{module_id}/work-items/` and return the ids actually changed."""

    path = "/workspaces/{slug}/projects/{project_id}/modules/{module_id}/work-items/"
    model = ModuleWorkItemManageResponse
    operations = {
        "bridge": "modules_work_items_manage",
    }

    def add(
        self, slug: str, project: str, module: str, work_item_ids: Sequence[str]
    ) -> builtins.list[str]:
        """Link 1..100 work items to this module; returns the ids actually added
        (already-linked ones are omitted)."""
        return self._bridge(
            key="add", ids=work_item_ids, slug=slug, project_id=project, module_id=module
        )

    def remove(
        self, slug: str, project: str, module: str, work_item_ids: Sequence[str]
    ) -> builtins.list[str]:
        """Unlink 1..100 work items from this module; returns the ids actually
        removed."""
        return self._bridge(
            key="remove", ids=work_item_ids, slug=slug, project_id=project, module_id=module
        )


class Modules(V2Resource[Module, CreateModule, UpdateModule], LoadsNavigableRows[LoadedModule]):
    path = "/workspaces/{slug}/projects/{project_id}/modules/"
    model = Module
    loaded_model = LoadedModule
    loaded_names = ("slug", "project", "module")
    operations = {
        "list": "modules_list",
        "retrieve": "modules_retrieve",
        "create": "modules_create",
        "update": "modules_partial_update",
        "upsert": "modules_upsert",
        "delete": "modules_destroy",
        "bulk_create": "modules_bulk_create",
        "bulk_update": "modules_bulk_update",
        "bulk_delete": "modules_bulk_delete",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.work_items = ModuleWorkItems(transport)

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[ModulesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ModulesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[ModulesListFilters],
    ) -> Page[LoadedModule]:
        """One page of modules in this project."""
        page = self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
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
        fields: Sequence[ModulesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ModulesListOrderBy | None = None,
        **filters: Unpack[ModulesListFilters],
    ) -> Iterator[LoadedModule]:
        """Every module, following pages automatically."""
        rows = self._iter(
            params={"fields": fields, "expand": expand, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
        )
        return (self._load(row, slug, project, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        project: str,
        module: str,
        *,
        fields: Sequence[ModulesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedModule:
        row = self._retrieve(
            pk=module, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def find_by_name(self, slug: str, project: str, name: str) -> LoadedModule:
        """The one module with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug, project_id=project)
        return self._load(row, slug, project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateModule,
        *,
        fields: Sequence[ModulesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedModule:
        row = self._create(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def update(
        self,
        slug: str,
        project: str,
        module: str,
        data: UpdateModule,
        *,
        fields: Sequence[ModulesPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedModule:
        row = self._update(
            data,
            pk=module,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )
        return self._load(row, slug, project, fields=fields)

    def delete(self, slug: str, project: str, module: str) -> None:
        return self._delete(pk=module, slug=slug, project_id=project)

    def upsert(
        self,
        slug: str,
        project: str,
        data: CreateModule,
        *,
        fields: Sequence[ModulesUpsertField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedModule:
        """Reconciles on (external_source, external_id) when both are set."""
        row = self._upsert(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def bulk_create(
        self,
        slug: str,
        project: str,
        items: builtins.list[CreateModule],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_create(items, all_or_none=all_or_none, slug=slug, project_id=project)

    def bulk_update(
        self,
        slug: str,
        project: str,
        items: builtins.list[Mapping[str, object]],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`."""
        return self._bulk_update(items, all_or_none=all_or_none, slug=slug, project_id=project)

    def bulk_delete(
        self,
        slug: str,
        project: str,
        ids: builtins.list[str],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_delete(ids, all_or_none=all_or_none, slug=slug, project_id=project)
