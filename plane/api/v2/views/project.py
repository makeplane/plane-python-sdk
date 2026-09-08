"""Project-scoped saved views (api_v2)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.views import CreateView, UpdateView, View
from .._generated.constants import (
    ProjectViewsCreateField,
    ProjectViewsListField,
    ProjectViewsListFilters,
    ProjectViewsListOrderBy,
    ProjectViewsPartialUpdateField,
    ProjectViewsRetrieveField,
)
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
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectViewsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ProjectViewsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[ProjectViewsListFilters],
    ) -> Page[View]:
        """One page of views in this project. `**filters` covers `access`,
        `is_locked`, `name`, `owned_by_id`."""
        return self._list(
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

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectViewsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ProjectViewsListOrderBy | None = None,
        **filters: Unpack[ProjectViewsListFilters],
    ) -> Iterator[View]:
        """Every view in this project, following pages automatically."""
        return self._iter(
            params={"fields": fields, "expand": expand, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        view: str,
        *,
        fields: Sequence[ProjectViewsRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> View:
        return self._retrieve(
            pk=view,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )

    def create(
        self,
        slug: str,
        project: str,
        data: CreateView,
        *,
        fields: Sequence[ProjectViewsCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> View:
        return self._create(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )

    def update(
        self,
        slug: str,
        project: str,
        view: str,
        data: UpdateView,
        *,
        fields: Sequence[ProjectViewsPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> View:
        return self._update(
            data,
            pk=view,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )

    def delete(self, slug: str, project: str, view: str) -> None:
        return self._delete(pk=view, slug=slug, project_id=project)
