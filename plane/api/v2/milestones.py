"""Project milestones (api_v2). Golden calls the identifying field `title`, but
the list filter is still `?name=` (aliased server-side); `find_by_name` keeps
the same `name` parameter every other resource uses. Milestone membership is
the `.work_items` bridge (`add`/`remove`)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from ...models.v2.common import BulkWriteResponse
from ...models.v2.milestone_work_items import (
    MilestoneWorkItemManageRequest,
    MilestoneWorkItemManageResponse,
)
from ...models.v2.milestones import CreateMilestone, Milestone, UpdateMilestone
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport


class MilestoneWorkItems(
    V2Resource[
        MilestoneWorkItemManageResponse,
        MilestoneWorkItemManageRequest,
        MilestoneWorkItemManageRequest,
    ]
):
    """Membership bridge between a milestone and work items: `add` links work
    items to the milestone, `remove` unlinks them. Both POST to
    `.../milestones/{milestone_id}/work-items/` and return the ids actually
    changed."""

    path = "/workspaces/{slug}/projects/{project_id}/milestones/{milestone_id}/work-items/"
    model = MilestoneWorkItemManageResponse
    operations = {
        "bridge": "milestones_work_items",
    }

    def add(self, milestone_id: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Link 1..100 work items to this milestone; returns the ids actually
        added (already-linked ones are omitted)."""
        return self._bridge(key="add", ids=work_item_ids, milestone_id=milestone_id)

    def remove(self, milestone_id: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Unlink 1..100 work items from this milestone; returns the ids
        actually removed."""
        return self._bridge(key="remove", ids=work_item_ids, milestone_id=milestone_id)


class Milestones(V2Resource[Milestone, CreateMilestone, UpdateMilestone]):
    path = "/workspaces/{slug}/projects/{project_id}/milestones/"
    model = Milestone
    operations = {
        "list": "milestones_list",
        "retrieve": "milestones_retrieve",
        "create": "milestones_create",
        "update": "milestones_partial_update",
        "upsert": "milestones_upsert",
        "delete": "milestones_destroy",
        "bulk_create": "milestones_bulk_create",
        "bulk_update": "milestones_bulk_update",
        "bulk_delete": "milestones_bulk_delete",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.work_items = MilestoneWorkItems(transport, **self._scope)

    def list(self, *, fields: Sequence[str] | None = None, **filters: Any) -> Page[Milestone]:
        """One page of milestones in this project."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[Milestone]:
        """Every milestone, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, milestone_id: str, *, fields: Sequence[str] | None = None) -> Milestone:
        return self._retrieve(pk=milestone_id, params={"fields": fields})

    def find_by_name(self, name: str) -> Milestone:
        """The one milestone whose title matches this name; raises if none or
        several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateMilestone) -> Milestone:
        return self._create(data)

    def update(self, milestone_id: str, data: UpdateMilestone) -> Milestone:
        return self._update(data, pk=milestone_id)

    def delete(self, milestone_id: str) -> None:
        return self._delete(pk=milestone_id)

    def upsert(self, data: CreateMilestone) -> Milestone:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data)

    def bulk_create(
        self, items: builtins.list[CreateMilestone], *, all_or_none: bool = False
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
