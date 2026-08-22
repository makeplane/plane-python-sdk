"""Estimates (api_v2) -- project-scoped, with nested estimate points.
Mirrors `states`/`labels` (CRUD + upsert + bulk), plus `expand=["points"]`."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from ....models.v2.common import BulkWriteResponse
from ....models.v2.estimates import CreateEstimate, Estimate, UpdateEstimate
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .points import EstimatePoints

__all__ = ["EstimatePoints", "Estimates"]


class Estimates(V2Resource[Estimate, CreateEstimate, UpdateEstimate]):
    path = "/workspaces/{slug}/projects/{project_id}/estimates/"
    model = Estimate
    operations = {
        "list": "estimates_list",
        "retrieve": "estimates_retrieve",
        "create": "estimates_create",
        "update": "estimates_partial_update",
        "upsert": "estimates_upsert",
        "delete": "estimates_destroy",
        "bulk_create": "estimates_bulk_create",
        "bulk_update": "estimates_bulk_update",
        "bulk_delete": "estimates_bulk_delete",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.points = EstimatePoints(transport, **self._scope)

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Estimate]:
        """One page of estimates in this project. Pass `expand=["points"]` to
        inline each estimate's points."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Estimate]:
        """Every estimate in this project, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        estimate_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Estimate:
        return self._retrieve(pk=estimate_id, params={"fields": fields, "expand": expand})

    def find_by_name(self, name: str) -> Estimate:
        """The one estimate with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateEstimate) -> Estimate:
        return self._create(data)

    def update(self, estimate_id: str, data: UpdateEstimate) -> Estimate:
        return self._update(data, pk=estimate_id)

    def delete(self, estimate_id: str) -> None:
        return self._delete(pk=estimate_id)

    def upsert(self, data: CreateEstimate) -> Estimate:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data)

    def bulk_create(
        self, items: builtins.list[CreateEstimate], *, all_or_none: bool = False
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
