"""Project states (api_v2)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence

from typing_extensions import Unpack

from ...models.v2.common import BulkWriteResponse
from ...models.v2.states import CreateState, State, UpdateState
from ._generated.constants import (
    StatesCreateField,
    StatesListField,
    StatesListFilters,
    StatesListOrderBy,
    StatesPartialUpdateField,
    StatesRetrieveField,
    StatesUpsertField,
)
from ._kernel.pagination import Page, PaginateStyle
from ._kernel.resource import V2Resource


class States(V2Resource[State, CreateState, UpdateState]):
    path = "/workspaces/{slug}/projects/{project_id}/states/"
    model = State
    operations = {
        "list": "states_list",
        "retrieve": "states_retrieve",
        "create": "states_create",
        "update": "states_partial_update",
        "delete": "states_destroy",
        "upsert": "states_upsert",
        "bulk_create": "states_bulk_create",
        "bulk_update": "states_bulk_update",
        "bulk_delete": "states_bulk_delete",
    }

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[StatesListField] | None = None,
        order_by: StatesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[StatesListFilters],
    ) -> Page[State]:
        """One page of states in this project."""
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
        )

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[StatesListField] | None = None,
        order_by: StatesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[StatesListFilters],
    ) -> Iterator[State]:
        """Every state, following pages automatically."""
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
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        state: str,
        *,
        fields: Sequence[StatesRetrieveField] | None = None,
    ) -> State:
        return self._retrieve(pk=state, params={"fields": fields}, slug=slug, project_id=project)

    def find_by_name(self, slug: str, project: str, name: str) -> State:
        """The one state with this name; raises if none or several match."""
        return self._find_one(filters={"name": name}, slug=slug, project_id=project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateState,
        *,
        fields: Sequence[StatesCreateField] | None = None,
    ) -> State:
        return self._create(data, params={"fields": fields}, slug=slug, project_id=project)

    def update(
        self,
        slug: str,
        project: str,
        state: str,
        data: UpdateState,
        *,
        fields: Sequence[StatesPartialUpdateField] | None = None,
    ) -> State:
        return self._update(
            data, pk=state, params={"fields": fields}, slug=slug, project_id=project
        )

    def delete(self, slug: str, project: str, state: str) -> None:
        return self._delete(pk=state, slug=slug, project_id=project)

    def upsert(
        self,
        slug: str,
        project: str,
        data: CreateState,
        *,
        fields: Sequence[StatesUpsertField] | None = None,
    ) -> State:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data, params={"fields": fields}, slug=slug, project_id=project)

    def bulk_create(
        self,
        slug: str,
        project: str,
        items: builtins.list[CreateState],
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
