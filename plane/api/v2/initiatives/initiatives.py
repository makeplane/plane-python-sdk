"""Initiatives (api_v2) -- workspace-scoped, unlike states/labels/work items.
Label/project/work-item membership are the `.labels`/`.projects`/`.work_items`
bridges (`add`/`remove`), not methods on `Initiatives` itself.

A fetched row (`retrieve`/`create`, and every row in a `list` page) comes back as a
`LoadedInitiative`: it carries the row's data and can reach `.projects.add(...)` and
friends without the caller repeating `slug`/`initiative`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.initiatives import CreateInitiative, Initiative, UpdateInitiative
from .._generated.constants import (
    InitiativesCreateField,
    InitiativesListField,
    InitiativesListFilters,
    InitiativesListOrderBy,
    InitiativesPartialUpdateField,
    InitiativesRetrieveField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.initiative import LoadedInitiative
from .labels import InitiativeLabels
from .projects import InitiativeProjects
from .work_items import InitiativeWorkItems

__all__ = ["InitiativeLabels", "InitiativeProjects", "InitiativeWorkItems", "Initiatives"]


class Initiatives(
    V2Resource[Initiative, CreateInitiative, UpdateInitiative], LoadsNavigableRows[LoadedInitiative]
):
    path = "/workspaces/{slug}/initiatives/"
    model = Initiative
    loaded_model = LoadedInitiative
    loaded_names = ("slug", "initiative")
    operations = {
        "list": "initiatives_list",
        "retrieve": "initiatives_retrieve",
        "create": "initiatives_create",
        "update": "initiatives_partial_update",
        "delete": "initiatives_destroy",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.labels = InitiativeLabels(transport)
        self.projects = InitiativeProjects(transport)
        self.work_items = InitiativeWorkItems(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[InitiativesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: InitiativesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[InitiativesListFilters],
    ) -> Page[LoadedInitiative]:
        """One page of initiatives in the workspace."""
        page = self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
        )
        return self._load_page(page, slug, fields=fields)

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[InitiativesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: InitiativesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[InitiativesListFilters],
    ) -> Iterator[LoadedInitiative]:
        """Every initiative in the workspace, following pages automatically."""
        rows = self._iter(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )
        return (self._load(row, slug, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        initiative: str,
        *,
        fields: Sequence[InitiativesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedInitiative:
        row = self._retrieve(pk=initiative, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def find_by_name(self, slug: str, name: str) -> LoadedInitiative:
        """The one initiative with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug)
        return self._load(row, slug)

    def create(
        self,
        slug: str,
        data: CreateInitiative,
        *,
        fields: Sequence[InitiativesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedInitiative:
        row = self._create(data, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def update(
        self,
        slug: str,
        initiative: str,
        data: UpdateInitiative,
        *,
        fields: Sequence[InitiativesPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedInitiative:
        row = self._update(
            data, pk=initiative, params={"fields": fields, "expand": expand}, slug=slug
        )
        return self._load(row, slug, fields=fields)

    def delete(self, slug: str, initiative: str) -> None:
        return self._delete(pk=initiative, slug=slug)
