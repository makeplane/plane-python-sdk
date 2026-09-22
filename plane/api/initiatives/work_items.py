from collections.abc import Iterable, Mapping
from typing import Any

from ...models.work_items import PaginatedWorkItemResponse, WorkItem
from ..base_resource import BaseResource


class InitiativeWorkItems(BaseResource):
    """API client for managing work items associated with initiatives.

    This is the successor to :class:`~plane.api.initiatives.epics.InitiativeEpics`.
    The two surfaces share one implementation server-side and one association
    model, so they behave identically; they differ only in the URL and in the
    request field name (``work_item_ids`` here, ``epic_ids`` there). Any
    work-item type is accepted -- the ``/epics/`` spelling reflects the old
    Epic-only model and is deprecated.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, initiative_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedWorkItemResponse:
        """List the work items associated with an initiative (paginated).

        Returns one page (20 by default). Pass `per_page`/`cursor` in params and
        follow `next_cursor` to page through the rest.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
            params: Optional query parameters, e.g. `per_page`, `cursor`

        Returns:
            Paginated list of work items
        """
        response = self._get(
            f"{workspace_slug}/initiatives/{initiative_id}/work-items", params=params
        )
        return PaginatedWorkItemResponse.model_validate(response)

    def add(
        self, workspace_slug: str, initiative_id: str, work_item_ids: Iterable[str]
    ) -> Iterable[WorkItem]:
        """Associate work items with an initiative.

        Work items already associated are skipped. The response covers every id
        requested, not only the newly added ones.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
            work_item_ids: List of work item UUIDs to associate

        Returns:
            List of the work items named in the request
        """
        response = self._post(
            f"{workspace_slug}/initiatives/{initiative_id}/work-items",
            {"work_item_ids": work_item_ids},
        )
        return [WorkItem.model_validate(work_item) for work_item in response]

    def remove(self, workspace_slug: str, initiative_id: str, work_item_ids: Iterable[str]) -> None:
        """Remove work items from an initiative.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
            work_item_ids: List of work item UUIDs to remove
        """
        return self._delete(
            f"{workspace_slug}/initiatives/{initiative_id}/work-items",
            {"work_item_ids": work_item_ids},
        )
