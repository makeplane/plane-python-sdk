"""Work item links (api_v2)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_items import CreateWorkItemLink, UpdateWorkItemLink, WorkItemLink
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
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItemLink]:
        """One page of links on a work item."""
        return self._list(work_item_id=work_item_id, params={"fields": fields, **filters})

    def iterate(
        self,
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkItemLink]:
        """Every link on a work item, following pages automatically."""
        return self._iter(work_item_id=work_item_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        work_item_id: str,
        link_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WorkItemLink:
        return self._retrieve(pk=link_id, work_item_id=work_item_id, params={"fields": fields})

    def create(self, work_item_id: str, data: CreateWorkItemLink) -> WorkItemLink:
        return self._create(data, work_item_id=work_item_id)

    def update(self, work_item_id: str, link_id: str, data: UpdateWorkItemLink) -> WorkItemLink:
        return self._update(data, pk=link_id, work_item_id=work_item_id)

    def delete(self, work_item_id: str, link_id: str) -> None:
        return self._delete(pk=link_id, work_item_id=work_item_id)
