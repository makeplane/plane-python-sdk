"""Project cycles (api_v2). `transfer` doesn't fit the CRUD request/response shape
`V2Resource` generates, so it builds its request directly but stays a plain method on
`Cycles`; cycle membership is the `.work_items` bridge (`add`/`remove`)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from ...models.v2.common import BulkWriteResponse
from ...models.v2.cycle_actions import (
    CycleTransfer,
    CycleTransferResult,
    CycleWorkItemManage,
    CycleWorkItemManageResult,
)
from ...models.v2.cycles import CreateCycle, Cycle, UpdateCycle
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport


class CycleWorkItems(
    V2Resource[CycleWorkItemManageResult, CycleWorkItemManage, CycleWorkItemManage]
):
    """Membership bridge between a cycle and work items: `add` moves work items into the
    cycle (re-homing them from any other cycle), `remove` takes them out. Both POST to
    `.../cycles/{cycle_id}/work-items/` and return the ids actually changed."""

    path = "/workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/work-items/"
    model = CycleWorkItemManageResult
    operations = {
        "bridge": "cycles_work_items_manage",
    }

    def add(self, cycle_id: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Move 1..100 work items into this cycle; returns the ids actually added
        (already-present ones are omitted)."""
        return self._bridge(key="add", ids=work_item_ids, cycle_id=cycle_id)

    def remove(self, cycle_id: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Take 1..100 work items out of this cycle; returns the ids actually removed."""
        return self._bridge(key="remove", ids=work_item_ids, cycle_id=cycle_id)


class Cycles(V2Resource[Cycle, CreateCycle, UpdateCycle]):
    path = "/workspaces/{slug}/projects/{project_id}/cycles/"
    model = Cycle
    operations = {
        "list": "cycles_list",
        "retrieve": "cycles_retrieve",
        "create": "cycles_create",
        "update": "cycles_partial_update",
        "upsert": "cycles_upsert",
        "delete": "cycles_destroy",
        "bulk_create": "cycles_bulk_create",
        "bulk_update": "cycles_bulk_update",
        "bulk_delete": "cycles_bulk_delete",
        "transfer": "cycles_transfer",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.work_items = CycleWorkItems(transport, **self._scope)

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Cycle]:
        """One page of cycles in this project."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Cycle]:
        """Every cycle, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        cycle_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Cycle:
        return self._retrieve(pk=cycle_id, params={"fields": fields, "expand": expand})

    def find_by_name(self, name: str) -> Cycle:
        """The one cycle with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateCycle) -> Cycle:
        return self._create(data)

    def update(self, cycle_id: str, data: UpdateCycle) -> Cycle:
        return self._update(data, pk=cycle_id)

    def delete(self, cycle_id: str) -> None:
        return self._delete(pk=cycle_id)

    def upsert(self, data: CreateCycle) -> Cycle:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data)

    def bulk_create(
        self, items: builtins.list[CreateCycle], *, all_or_none: bool = False
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

    def transfer(self, cycle_id: str, new_cycle_id: str) -> CycleTransferResult:
        """Move `cycle_id`'s incomplete work items into `new_cycle_id`. The source
        cycle must already be completed (server-enforced); the destination must
        exist in the same project."""
        data = CycleTransfer(new_cycle_id=new_cycle_id)
        payload = self.transport.request(
            "POST",
            f"{self._detail_url(cycle_id)}transfer/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return CycleTransferResult.model_validate(payload)
