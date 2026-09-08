"""Project cycles (api_v2). `transfer` doesn't fit the CRUD request/response shape
`V2Resource` generates, so it goes through the kernel's custom-action helper
(`_custom_action`) instead of `_action`, which assumes the response is the resource's
own `model`; cycle membership is the `.work_items` bridge (`add`/`remove`)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence

from typing_extensions import Unpack

from ...models.v2.common import BulkWriteResponse
from ...models.v2.cycle_actions import (
    CycleTransfer,
    CycleTransferResult,
    CycleWorkItemManage,
    CycleWorkItemManageResult,
)
from ...models.v2.cycles import CreateCycle, Cycle, UpdateCycle
from ._generated.constants import (
    CyclesCreateField,
    CyclesListField,
    CyclesListFilters,
    CyclesListOrderBy,
    CyclesPartialUpdateField,
    CyclesRetrieveField,
    CyclesUpsertField,
)
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

    def add(
        self, slug: str, project: str, cycle: str, work_item_ids: Sequence[str]
    ) -> builtins.list[str]:
        """Move 1..100 work items into this cycle; returns the ids actually added
        (already-present ones are omitted)."""
        return self._bridge(
            key="add", ids=work_item_ids, slug=slug, project_id=project, cycle_id=cycle
        )

    def remove(
        self, slug: str, project: str, cycle: str, work_item_ids: Sequence[str]
    ) -> builtins.list[str]:
        """Take 1..100 work items out of this cycle; returns the ids actually removed."""
        return self._bridge(
            key="remove", ids=work_item_ids, slug=slug, project_id=project, cycle_id=cycle
        )


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

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.work_items = CycleWorkItems(transport)

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[CyclesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: CyclesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[CyclesListFilters],
    ) -> Page[Cycle]:
        """One page of cycles in this project."""
        return self._list(
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

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[CyclesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: CyclesListOrderBy | None = None,
        **filters: Unpack[CyclesListFilters],
    ) -> Iterator[Cycle]:
        """Every cycle, following pages automatically."""
        return self._iter(
            params={"fields": fields, "expand": expand, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        cycle: str,
        *,
        fields: Sequence[CyclesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Cycle:
        return self._retrieve(
            pk=cycle, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )

    def find_by_name(self, slug: str, project: str, name: str) -> Cycle:
        """The one cycle with this name; raises if none or several match."""
        return self._find_one(filters={"name": name}, slug=slug, project_id=project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateCycle,
        *,
        fields: Sequence[CyclesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Cycle:
        return self._create(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )

    def update(
        self,
        slug: str,
        project: str,
        cycle: str,
        data: UpdateCycle,
        *,
        fields: Sequence[CyclesPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Cycle:
        return self._update(
            data,
            pk=cycle,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )

    def delete(self, slug: str, project: str, cycle: str) -> None:
        return self._delete(pk=cycle, slug=slug, project_id=project)

    def upsert(
        self,
        slug: str,
        project: str,
        data: CreateCycle,
        *,
        fields: Sequence[CyclesUpsertField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Cycle:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )

    def bulk_create(
        self,
        slug: str,
        project: str,
        items: builtins.list[CreateCycle],
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

    # -- Custom actions ------------------------------------------------------

    def transfer(self, slug: str, project: str, cycle: str, new_cycle: str) -> CycleTransferResult:
        """Move `cycle`'s incomplete work items into `new_cycle`. The source cycle
        must already be completed (server-enforced); the destination must exist in
        the same project."""
        data = CycleTransfer(new_cycle_id=new_cycle)
        return self._custom_action(
            "transfer",
            model=CycleTransferResult,
            pk=cycle,
            data=data,
            slug=slug,
            project_id=project,
        )
