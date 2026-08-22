"""Teamspaces (api_v2) -- a named grouping of members + projects. Flat CRUD
(no bulk, no upsert). `expand` accepts `lead`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.teamspaces import CreateTeamspace, Teamspace, UpdateTeamspace
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


class Teamspaces(V2Resource[Teamspace, CreateTeamspace, UpdateTeamspace]):
    path = "/workspaces/{slug}/teamspaces/"
    model = Teamspace
    operations = {
        "list": "teamspaces_list",
        "retrieve": "teamspaces_retrieve",
        "create": "teamspaces_create",
        "update": "teamspaces_partial_update",
        "delete": "teamspaces_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Teamspace]:
        """One page of teamspaces. `**filters` covers the golden's query filters
        directly, e.g. `lead_id=...`, `name="Platform"`, `search="plat"`."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Teamspace]:
        """Every teamspace, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        teamspace_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Teamspace:
        return self._retrieve(
            pk=teamspace_id,
            params={"fields": fields, "expand": expand},
        )

    def find_by_name(self, name: str) -> Teamspace:
        """The one teamspace with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateTeamspace) -> Teamspace:
        return self._create(data)

    def update(self, teamspace_id: str, data: UpdateTeamspace) -> Teamspace:
        return self._update(data, pk=teamspace_id)

    def delete(self, teamspace_id: str) -> None:
        return self._delete(pk=teamspace_id)
