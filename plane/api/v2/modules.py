"""Project modules (api_v2). Module membership (`member_ids`) is read-only:
the golden's `ModuleWriteRequest` has no writable member field."""

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
        "manage_work_items": "modules_work_items_manage",
    }

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

    # -- Custom actions ------------------------------------------------------

    def manage_work_items(
        self, module_id: str, data: ModuleWorkItemManageRequest
    ) -> ModuleWorkItemManageResponse:
        """Add and/or remove work items on this module, returning the ids
        actually changed. Built directly since the response isn't this resource's `model`."""
        payload = self.transport.request(
            "POST",
            f"{self._detail_url(module_id)}work-items/",
            params=self._query(None, action="manage_work_items"),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return ModuleWorkItemManageResponse.model_validate(payload)
