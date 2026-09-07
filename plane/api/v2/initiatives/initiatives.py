"""Initiatives (api_v2) -- workspace-scoped, unlike states/labels/work items.
Label/project/work-item membership are the `.labels`/`.projects`/`.work_items`
bridges (`add`/`remove`), not methods on `Initiatives` itself."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.initiatives import CreateInitiative, Initiative, UpdateInitiative
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .labels import InitiativeLabels
from .projects import InitiativeProjects
from .work_items import InitiativeWorkItems

__all__ = ["InitiativeLabels", "InitiativeProjects", "InitiativeWorkItems", "Initiatives"]


class Initiatives(V2Resource[Initiative, CreateInitiative, UpdateInitiative]):
    path = "/workspaces/{slug}/initiatives/"
    model = Initiative
    operations = {
        "list": "initiatives_list",
        "retrieve": "initiatives_retrieve",
        "create": "initiatives_create",
        "update": "initiatives_partial_update",
        "delete": "initiatives_destroy",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.labels = InitiativeLabels(transport, **self._scope)
        self.projects = InitiativeProjects(transport, **self._scope)
        self.work_items = InitiativeWorkItems(transport, **self._scope)

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Initiative]:
        """One page of initiatives in a workspace.

        `**filters` covers `lead_id`, `state`/`state__in`, `search`."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Initiative]:
        """Every initiative in a workspace, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        pk: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Initiative:
        return self._retrieve(pk=pk, params={"fields": fields, "expand": expand})

    def find_by_name(self, name: str) -> Initiative:
        """The one initiative with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateInitiative) -> Initiative:
        return self._create(data)

    def update(self, pk: str, data: UpdateInitiative) -> Initiative:
        return self._update(data, pk=pk)

    def delete(self, pk: str) -> None:
        return self._delete(pk=pk)
