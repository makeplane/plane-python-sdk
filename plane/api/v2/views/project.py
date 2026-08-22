"""Project-scoped saved views (api_v2)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.views import CreateView, UpdateView, View
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class ProjectViews(V2Resource[View, CreateView, UpdateView]):
    path = "/workspaces/{slug}/projects/{project_id}/views/"
    model = View
    operations = {
        "list": "project_views_list",
        "retrieve": "project_views_retrieve",
        "create": "project_views_create",
        "update": "project_views_partial_update",
        "delete": "project_views_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[View]:
        """One page of views in this project. `**filters` covers `access`,
        `is_locked`, `name`, `owned_by_id`."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[View]:
        """Every view in this project, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        view_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> View:
        return self._retrieve(pk=view_id, params={"fields": fields, "expand": expand})

    def create(self, data: CreateView) -> View:
        return self._create(data)

    def update(self, view_id: str, data: UpdateView) -> View:
        return self._update(data, pk=view_id)

    def delete(self, view_id: str) -> None:
        return self._delete(pk=view_id)
