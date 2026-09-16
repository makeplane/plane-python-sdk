"""Project milestones (api_v2). Golden calls the identifying field `title`, but
the list filter is still `?name=` (aliased server-side); `find_by_name` keeps
the same `name` parameter every other resource uses. Milestone membership is
the `.work_items` bridge (`add`/`remove`).

A fetched row (`retrieve`/`create`, and every row in a `list` page) comes back as a
`LoadedMilestone`: it carries the row's data and can reach `.work_items.add(...)`
without the caller repeating `slug`/`project`/`milestone`."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence

from typing_extensions import Unpack

from ...models.v2.common import BulkWriteResponse
from ...models.v2.milestone_work_items import (
    MilestoneWorkItemManageRequest,
    MilestoneWorkItemManageResponse,
)
from ...models.v2.milestones import CreateMilestone, Milestone, UpdateMilestone
from ._generated.constants import (
    MilestonesCreateField,
    MilestonesListField,
    MilestonesListFilters,
    MilestonesListOrderBy,
    MilestonesPartialUpdateField,
    MilestonesRetrieveField,
    MilestonesUpsertField,
)
from ._kernel.loaded import LoadsNavigableRows
from ._kernel.pagination import Page, PaginateStyle
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport
from ._loaded.milestone import LoadedMilestone


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

    def add(
        self, slug: str, project: str, milestone: str, work_item_ids: Sequence[str]
    ) -> builtins.list[str]:
        """Link 1..100 work items to this milestone; returns the ids actually
        added (already-linked ones are omitted)."""
        return self._bridge(
            key="add", ids=work_item_ids, slug=slug, project_id=project, milestone_id=milestone
        )

    def remove(
        self, slug: str, project: str, milestone: str, work_item_ids: Sequence[str]
    ) -> builtins.list[str]:
        """Unlink 1..100 work items from this milestone; returns the ids
        actually removed."""
        return self._bridge(
            key="remove", ids=work_item_ids, slug=slug, project_id=project, milestone_id=milestone
        )


class Milestones(
    V2Resource[Milestone, CreateMilestone, UpdateMilestone],
    LoadsNavigableRows[LoadedMilestone],
):
    path = "/workspaces/{slug}/projects/{project_id}/milestones/"
    model = Milestone
    loaded_model = LoadedMilestone
    loaded_names = ("slug", "project", "milestone")
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

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.work_items = MilestoneWorkItems(transport)

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[MilestonesListField] | None = None,
        order_by: MilestonesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[MilestonesListFilters],
    ) -> Page[LoadedMilestone]:
        """One page of milestones in this project."""
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
        fields: Sequence[MilestonesListField] | None = None,
        order_by: MilestonesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[MilestonesListFilters],
    ) -> Iterator[LoadedMilestone]:
        """Every milestone, following pages automatically."""
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
        milestone: str,
        *,
        fields: Sequence[MilestonesRetrieveField] | None = None,
    ) -> LoadedMilestone:
        row = self._retrieve(pk=milestone, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def find_by_name(self, slug: str, project: str, name: str) -> LoadedMilestone:
        """The one milestone whose title matches this name; raises if none or
        several match."""
        row = self._find_one(filters={"name": name}, slug=slug, project_id=project)
        return self._load(row, slug, project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateMilestone,
        *,
        fields: Sequence[MilestonesCreateField] | None = None,
    ) -> LoadedMilestone:
        row = self._create(data, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def update(
        self,
        slug: str,
        project: str,
        milestone: str,
        data: UpdateMilestone,
        *,
        fields: Sequence[MilestonesPartialUpdateField] | None = None,
    ) -> LoadedMilestone:
        row = self._update(
            data, pk=milestone, params={"fields": fields}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def delete(self, slug: str, project: str, milestone: str) -> None:
        return self._delete(pk=milestone, slug=slug, project_id=project)

    def upsert(
        self,
        slug: str,
        project: str,
        data: CreateMilestone,
        *,
        fields: Sequence[MilestonesUpsertField] | None = None,
    ) -> LoadedMilestone:
        """Reconciles on (external_source, external_id) when both are set."""
        row = self._upsert(data, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def bulk_create(
        self,
        slug: str,
        project: str,
        items: builtins.list[CreateMilestone],
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
