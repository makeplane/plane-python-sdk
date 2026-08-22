"""Estimate points (api_v2) -- nested under a project-scoped estimate."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from ....models.v2.common import BulkWriteResponse
from ....models.v2.estimates import CreateEstimatePoint, EstimatePoint, UpdateEstimatePoint
from .._kernel.pagination import Page
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
        estimate_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[EstimatePoint]:
        """One page of points belonging to an estimate."""
        return self._list(estimate_id=estimate_id, params={"fields": fields, **filters})

    def iterate(
        self,
        estimate_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[EstimatePoint]:
        """Every point belonging to an estimate, following pages automatically."""
        return self._iter(estimate_id=estimate_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        estimate_id: str,
        point_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> EstimatePoint:
        return self._retrieve(pk=point_id, estimate_id=estimate_id, params={"fields": fields})

    def create(self, estimate_id: str, data: CreateEstimatePoint) -> EstimatePoint:
        return self._create(data, estimate_id=estimate_id)

    def update(
        self, estimate_id: str, point_id: str, data: UpdateEstimatePoint
    ) -> EstimatePoint:
        return self._update(data, pk=point_id, estimate_id=estimate_id)

    def delete(self, estimate_id: str, point_id: str) -> None:
        return self._delete(pk=point_id, estimate_id=estimate_id)

    def upsert(self, estimate_id: str, data: CreateEstimatePoint) -> EstimatePoint:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data, estimate_id=estimate_id)

    def bulk_create(
        self,
        estimate_id: str,
        items: builtins.list[CreateEstimatePoint],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_create(items, all_or_none=all_or_none, estimate_id=estimate_id)

    def bulk_update(
        self,
        estimate_id: str,
        items: builtins.list[Mapping[str, Any]],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`."""
        return self._bulk_update(items, all_or_none=all_or_none, estimate_id=estimate_id)

    def bulk_delete(
        self,
        estimate_id: str,
        ids: builtins.list[str],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_delete(ids, all_or_none=all_or_none, estimate_id=estimate_id)
