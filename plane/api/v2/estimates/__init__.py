"""Estimates (api_v2) -- project-scoped, with nested estimate points.
Mirrors `states`/`labels` (CRUD + upsert + bulk), plus `expand=["points"]`.

A fetched row (`retrieve`/`create`, and every row in a `list` page) comes back as a
`LoadedEstimate`: it carries the row's data and can reach `.estimate_points.list()`
etc. without the caller repeating `slug`/`project`/`estimate` -- named
`estimate_points`, not `points`, because `points` is itself a real field (inline
data returned when the caller passes `expand=["points"]`)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence

from typing_extensions import Unpack

from ....models.v2.common import BulkWriteResponse
from ....models.v2.estimates import CreateEstimate, Estimate, UpdateEstimate
from .._generated.constants import (
    EstimatesCreateField,
    EstimatesListField,
    EstimatesListFilters,
    EstimatesListOrderBy,
    EstimatesPartialUpdateField,
    EstimatesRetrieveField,
    EstimatesUpsertField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.estimate import LoadedEstimate
from .points import EstimatePoints

__all__ = ["EstimatePoints", "Estimates"]


class Estimates(
    V2Resource[Estimate, CreateEstimate, UpdateEstimate], LoadsNavigableRows[LoadedEstimate]
):
    path = "/workspaces/{slug}/projects/{project_id}/estimates/"
    model = Estimate
    loaded_model = LoadedEstimate
    loaded_names = ("slug", "project", "estimate")
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

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.points = EstimatePoints(transport)

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[EstimatesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: EstimatesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[EstimatesListFilters],
    ) -> Page[LoadedEstimate]:
        """One page of estimates in this project. Pass `expand=["points"]` to
        inline each estimate's points."""
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
        fields: Sequence[EstimatesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: EstimatesListOrderBy | None = None,
        **filters: Unpack[EstimatesListFilters],
    ) -> Iterator[LoadedEstimate]:
        """Every estimate in this project, following pages automatically."""
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
        estimate: str,
        *,
        fields: Sequence[EstimatesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedEstimate:
        row = self._retrieve(
            pk=estimate,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )
        return self._load(row, slug, project, fields=fields)

    def find_by_name(self, slug: str, project: str, name: str) -> LoadedEstimate:
        """The one estimate with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug, project_id=project)
        return self._load(row, slug, project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateEstimate,
        *,
        fields: Sequence[EstimatesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedEstimate:
        row = self._create(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def update(
        self,
        slug: str,
        project: str,
        estimate: str,
        data: UpdateEstimate,
        *,
        fields: Sequence[EstimatesPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedEstimate:
        row = self._update(
            data,
            pk=estimate,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )
        return self._load(row, slug, project, fields=fields)

    def delete(self, slug: str, project: str, estimate: str) -> None:
        return self._delete(pk=estimate, slug=slug, project_id=project)

    def upsert(
        self,
        slug: str,
        project: str,
        data: CreateEstimate,
        *,
        fields: Sequence[EstimatesUpsertField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedEstimate:
        """Reconciles on (external_source, external_id) when both are set."""
        row = self._upsert(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def bulk_create(
        self,
        slug: str,
        project: str,
        items: builtins.list[CreateEstimate],
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
