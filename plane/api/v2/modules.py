"""Project modules (api_v2). Module membership (`member_ids`) is read-only:
the golden's `ModuleWriteRequest` has no writable member field; work item
membership is the `.work_items` bridge (`add`/`remove`)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from ...models.v2.common import BulkWriteResponse
from ...models.v2.module_work_items import (
    ModuleWorkItemManageRequest,
    ModuleWorkItemManageResponse,
)
from ...models.v2.modules import CreateModule, Module, UpdateModule
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport


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

    def add(self, module_id: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Link 1..100 work items to this module; returns the ids actually added
        (already-linked ones are omitted)."""
        return self._bridge(key="add", ids=work_item_ids, module_id=module_id)

    def remove(self, module_id: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Unlink 1..100 work items from this module; returns the ids actually
        removed."""
        return self._bridge(key="remove", ids=work_item_ids, module_id=module_id)


class Modules(V2Resource[Module, CreateModule, UpdateModule]):
    path = "/workspaces/{slug}/projects/{project_id}/modules/"
    model = Module
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

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.work_items = ModuleWorkItems(transport, **self._scope)

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Module]:
        """One page of modules in this project."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Module]:
        """Every module, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        module_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Module:
        return self._retrieve(pk=module_id, params={"fields": fields, "expand": expand})

    def find_by_name(self, name: str) -> Module:
        """The one module with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateModule) -> Module:
        return self._create(data)

    def update(self, module_id: str, data: UpdateModule) -> Module:
        return self._update(data, pk=module_id)

    def delete(self, module_id: str) -> None:
        return self._delete(pk=module_id)

    def upsert(self, data: CreateModule) -> Module:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data)

    def bulk_create(
        self, items: builtins.list[CreateModule], *, all_or_none: bool = False
    ) -> BulkWriteResponse:
        return self._bulk_create(items, all_or_none=all_or_none)

    def bulk_update(
        self, items: builtins.list[Mapping[str, Any]], *, all_or_none: bool = False
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`."""
        return self._bulk_update(items, all_or_none=all_or_none)

    def bulk_delete(
        self, ids: builtins.list[str], *, all_or_none: bool = False
    ) -> BulkWriteResponse:
        return self._bulk_delete(ids, all_or_none=all_or_none)
