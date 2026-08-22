"""Initiatives (api_v2) -- workspace-scoped, unlike states/labels/work items.
`manage_labels`/`manage_projects`/`manage_work_items` return changed ids, not an
`Initiative`, so they bypass `_action`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.initiatives import (
    CreateInitiative,
    Initiative,
    InitiativeChildManageRequest,
    InitiativeChildManageResponse,
    UpdateInitiative,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .labels import InitiativeLabels

__all__ = ["InitiativeLabels", "Initiatives"]


class Initiatives(V2Resource[Initiative, CreateInitiative, UpdateInitiative]):
    path = "/workspaces/{slug}/initiatives/"
    model = Initiative
    operations = {
        "list": "initiatives_list",
        "retrieve": "initiatives_retrieve",
        "create": "initiatives_create",
        "update": "initiatives_partial_update",
        "delete": "initiatives_destroy",
        "manage_labels": "initiatives_labels",
        "manage_projects": "initiatives_projects",
        "manage_work_items": "initiatives_work_items",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.labels = InitiativeLabels(transport, **self._scope)

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

    def _manage_child(
        self, action: str, pk: str, data: InitiativeChildManageRequest
    ) -> InitiativeChildManageResponse:
        payload = self.transport.request(
            "POST",
            f"{self._detail_url(pk)}{action}/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return InitiativeChildManageResponse.model_validate(payload)

    def manage_labels(
        self, pk: str, data: InitiativeChildManageRequest
    ) -> InitiativeChildManageResponse:
        """Attach (`data.add`) or detach (`data.remove`) initiative labels on this
        initiative, returning the ids actually changed."""
        return self._manage_child("labels", pk, data)

    def manage_projects(
        self, pk: str, data: InitiativeChildManageRequest
    ) -> InitiativeChildManageResponse:
        """Add (`data.add`) or remove (`data.remove`) projects on this initiative,
        returning the ids actually changed."""
        return self._manage_child("projects", pk, data)

    def manage_work_items(
        self, pk: str, data: InitiativeChildManageRequest
    ) -> InitiativeChildManageResponse:
        """Link (`data.add`) or unlink (`data.remove`) work items on this
        initiative, returning the ids actually changed."""
        return self._manage_child("work-items", pk, data)
