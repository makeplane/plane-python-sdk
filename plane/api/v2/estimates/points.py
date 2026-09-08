"""Estimate points (api_v2) -- nested under a project-scoped estimate."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence

from typing_extensions import Unpack

from ....models.v2.common import BulkWriteResponse
from ....models.v2.estimates import CreateEstimatePoint, EstimatePoint, UpdateEstimatePoint
from .._generated.constants import (
    EstimatePointsCreateField,
    EstimatePointsListField,
    EstimatePointsListFilters,
    EstimatePointsListOrderBy,
    EstimatePointsPartialUpdateField,
    EstimatePointsRetrieveField,
    EstimatePointsUpsertField,
)
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource


class EstimatePoints(V2Resource[EstimatePoint, CreateEstimatePoint, UpdateEstimatePoint]):
    path = "/workspaces/{slug}/projects/{project_id}/estimates/{estimate_id}/points/"
    model = EstimatePoint
    operations = {
        "list": "estimate_points_list",
        "retrieve": "estimate_points_retrieve",
        "create": "estimate_points_create",
        "update": "estimate_points_partial_update",
        "upsert": "estimate_points_upsert",
        "delete": "estimate_points_destroy",
        "bulk_create": "estimate_points_bulk_create",
        "bulk_update": "estimate_points_bulk_update",
        "bulk_delete": "estimate_points_bulk_delete",
    }

    def list(
        self,
        slug: str,
        project: str,
        estimate: str,
        *,
        fields: Sequence[EstimatePointsListField] | None = None,
        order_by: EstimatePointsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[EstimatePointsListFilters],
    ) -> Page[EstimatePoint]:
        """One page of points belonging to an estimate."""
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
            project_id=project,
            estimate_id=estimate,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        estimate: str,
        *,
        fields: Sequence[EstimatePointsListField] | None = None,
        order_by: EstimatePointsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[EstimatePointsListFilters],
    ) -> Iterator[EstimatePoint]:
        """Every point belonging to an estimate, following pages automatically."""
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
            project_id=project,
            estimate_id=estimate,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        estimate: str,
        point: str,
        *,
        fields: Sequence[EstimatePointsRetrieveField] | None = None,
    ) -> EstimatePoint:
        return self._retrieve(
            pk=point,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            estimate_id=estimate,
        )

    def find_by_key(self, slug: str, project: str, estimate: str, key: int) -> EstimatePoint:
        """The one point on this estimate with this key; raises if none or several
        match."""
        return self._find_one(
            filters={"key": key}, slug=slug, project_id=project, estimate_id=estimate
        )

    def create(
        self,
        slug: str,
        project: str,
        estimate: str,
        data: CreateEstimatePoint,
        *,
        fields: Sequence[EstimatePointsCreateField] | None = None,
    ) -> EstimatePoint:
        return self._create(
            data,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            estimate_id=estimate,
        )

    def update(
        self,
        slug: str,
        project: str,
        estimate: str,
        point: str,
        data: UpdateEstimatePoint,
        *,
        fields: Sequence[EstimatePointsPartialUpdateField] | None = None,
    ) -> EstimatePoint:
        return self._update(
            data,
            pk=point,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            estimate_id=estimate,
        )

    def delete(self, slug: str, project: str, estimate: str, point: str) -> None:
        return self._delete(pk=point, slug=slug, project_id=project, estimate_id=estimate)

    def upsert(
        self,
        slug: str,
        project: str,
        estimate: str,
        data: CreateEstimatePoint,
        *,
        fields: Sequence[EstimatePointsUpsertField] | None = None,
    ) -> EstimatePoint:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(
            data,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            estimate_id=estimate,
        )

    def bulk_create(
        self,
        slug: str,
        project: str,
        estimate: str,
        items: builtins.list[CreateEstimatePoint],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_create(
            items,
            all_or_none=all_or_none,
            slug=slug,
            project_id=project,
            estimate_id=estimate,
        )

    def bulk_update(
        self,
        slug: str,
        project: str,
        estimate: str,
        items: builtins.list[Mapping[str, object]],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`."""
        return self._bulk_update(
            items,
            all_or_none=all_or_none,
            slug=slug,
            project_id=project,
            estimate_id=estimate,
        )

    def bulk_delete(
        self,
        slug: str,
        project: str,
        estimate: str,
        ids: builtins.list[str],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_delete(
            ids,
            all_or_none=all_or_none,
            slug=slug,
            project_id=project,
            estimate_id=estimate,
        )
