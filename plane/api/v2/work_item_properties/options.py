"""Options on a project-scoped work item property (api_v2). Only meaningful for
OPTION-type properties. No `?fields=` here -- options always return in full;
`order_by` is offered, though."""

from __future__ import annotations

from collections.abc import Iterator

from typing_extensions import Unpack

from ....models.v2.work_item_properties import (
    CreateWorkItemPropertyOption,
    UpdateWorkItemPropertyOption,
    WorkItemPropertyOption,
)
from .._generated.constants import (
    WorkItemPropertyOptionsListFilters,
    WorkItemPropertyOptionsListOrderBy,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkItemPropertyOptions(
    V2Resource[WorkItemPropertyOption, CreateWorkItemPropertyOption, UpdateWorkItemPropertyOption]
):
    path = "/workspaces/{slug}/projects/{project_id}/work-item-properties/{property_id}/options/"
    model = WorkItemPropertyOption
    operations = {
        "list": "work_item_property_options_list",
        "retrieve": "work_item_property_options_retrieve",
        "create": "work_item_property_options_create",
        "update": "work_item_property_options_partial_update",
        "delete": "work_item_property_options_destroy",
    }

    def list(
        self,
        slug: str,
        project: str,
        property: str,
        *,
        order_by: WorkItemPropertyOptionsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[WorkItemPropertyOptionsListFilters],
    ) -> Page[WorkItemPropertyOption]:
        """One page of a property's options."""
        return self._list(
            params={"order_by": order_by, "per_page": per_page, "offset": offset, **filters},
            slug=slug,
            project_id=project,
            property_id=property,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        property: str,
        *,
        order_by: WorkItemPropertyOptionsListOrderBy | None = None,
        **filters: Unpack[WorkItemPropertyOptionsListFilters],
    ) -> Iterator[WorkItemPropertyOption]:
        """Every option on a property, following pages automatically."""
        return self._iter(
            params={"order_by": order_by, **filters},
            slug=slug,
            project_id=project,
            property_id=property,
        )

    def retrieve(
        self, slug: str, project: str, property: str, option: str
    ) -> WorkItemPropertyOption:
        return self._retrieve(pk=option, slug=slug, project_id=project, property_id=property)

    def find_by_name(
        self, slug: str, project: str, property: str, name: str
    ) -> WorkItemPropertyOption:
        """The one option on this property with this name; raises if none or
        several match."""
        return self._find_one(
            filters={"name": name}, slug=slug, project_id=project, property_id=property
        )

    def create(
        self, slug: str, project: str, property: str, data: CreateWorkItemPropertyOption
    ) -> WorkItemPropertyOption:
        return self._create(data, slug=slug, project_id=project, property_id=property)

    def update(
        self,
        slug: str,
        project: str,
        property: str,
        option: str,
        data: UpdateWorkItemPropertyOption,
    ) -> WorkItemPropertyOption:
        return self._update(data, pk=option, slug=slug, project_id=project, property_id=property)

    def delete(self, slug: str, project: str, property: str, option: str) -> None:
        return self._delete(pk=option, slug=slug, project_id=project, property_id=property)
