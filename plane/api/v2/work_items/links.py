"""Work item links (api_v2)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.work_items import CreateWorkItemLink, UpdateWorkItemLink, WorkItemLink
from .._generated.constants import (
    LinksCreateField,
    LinksListField,
    LinksListFilters,
    LinksListOrderBy,
    LinksPartialUpdateField,
    LinksRetrieveField,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkItemLinks(V2Resource[WorkItemLink, CreateWorkItemLink, UpdateWorkItemLink]):
    path = "/workspaces/{slug}/projects/{project_id}/work-items/{work_item_id}/links/"
    model = WorkItemLink
    operations = {
        "list": "links_list",
        "retrieve": "links_retrieve",
        "create": "links_create",
        "update": "links_partial_update",
        "delete": "links_destroy",
    }

    def list(
        self,
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[LinksListField] | None = None,
        order_by: LinksListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[LinksListFilters],
    ) -> Page[WorkItemLink]:
        """One page of links on a work item."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[LinksListField] | None = None,
        order_by: LinksListOrderBy | None = None,
        **filters: Unpack[LinksListFilters],
    ) -> Iterator[WorkItemLink]:
        """Every link on a work item, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        work_item: str,
        link: str,
        *,
        fields: Sequence[LinksRetrieveField] | None = None,
    ) -> WorkItemLink:
        return self._retrieve(
            pk=link,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def create(
        self,
        slug: str,
        project: str,
        work_item: str,
        data: CreateWorkItemLink,
        *,
        fields: Sequence[LinksCreateField] | None = None,
    ) -> WorkItemLink:
        return self._create(
            data,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def update(
        self,
        slug: str,
        project: str,
        work_item: str,
        link: str,
        data: UpdateWorkItemLink,
        *,
        fields: Sequence[LinksPartialUpdateField] | None = None,
    ) -> WorkItemLink:
        return self._update(
            data,
            pk=link,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def delete(self, slug: str, project: str, work_item: str, link: str) -> None:
        return self._delete(pk=link, slug=slug, project_id=project, work_item_id=work_item)
