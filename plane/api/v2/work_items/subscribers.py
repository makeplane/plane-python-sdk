"""Work item subscribers (api_v2). One list per work item with no pk of its own, so it
goes through the kernel's `_retrieve_singleton`/`_update_singleton` pair. Named
`WorkItemSubscribersResource` to avoid clashing with the `WorkItemSubscribers` model.

The `*_by_identifier` pair reaches the same list by human-readable key (e.g.
`"ENG-12"`) with no project id, via `extra_paths`."""

from __future__ import annotations

from ....models.v2.work_items import UpdateWorkItemSubscribers, WorkItemSubscribers
from .._kernel.resource import V2Resource

__all__ = ["WorkItemSubscribersResource"]

_BY_IDENTIFIER = "/workspaces/{slug}/work-items/{identifier}/subscribers/"


class WorkItemSubscribersResource(
    V2Resource[WorkItemSubscribers, UpdateWorkItemSubscribers, UpdateWorkItemSubscribers]
):
    path = "/workspaces/{slug}/projects/{project_id}/work-items/{work_item_id}/subscribers/"
    extra_paths = {
        "retrieve_by_identifier": _BY_IDENTIFIER,
        "update_by_identifier": _BY_IDENTIFIER,
    }
    model = WorkItemSubscribers
    operations = {
        "retrieve": "work_items_subscribers_retrieve",
        "update": "work_items_subscribers_partial_update",
        "retrieve_by_identifier": "work_items_subscribers_retrieve_by_identifier",
        "update_by_identifier": "work_items_subscribers_partial_update_by_identifier",
    }

    def retrieve(self, slug: str, project: str, work_item: str) -> WorkItemSubscribers:
        return self._retrieve_singleton(slug=slug, project_id=project, work_item_id=work_item)

    def update(
        self, slug: str, project: str, work_item: str, data: UpdateWorkItemSubscribers
    ) -> WorkItemSubscribers:
        """Apply `add`/`remove` and return the resulting list."""
        return self._update_singleton(data, slug=slug, project_id=project, work_item_id=work_item)

    def retrieve_by_identifier(self, slug: str, identifier: str) -> WorkItemSubscribers:
        return self._retrieve_singleton(
            action="retrieve_by_identifier", slug=slug, identifier=identifier
        )

    def update_by_identifier(
        self, slug: str, identifier: str, data: UpdateWorkItemSubscribers
    ) -> WorkItemSubscribers:
        return self._update_singleton(
            data, action="update_by_identifier", slug=slug, identifier=identifier
        )
