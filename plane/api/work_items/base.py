from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from ...models.query_params import (
    RetrieveQueryParams,
    WorkItemCountQueryParams,
    WorkItemQueryParams,
)
from ...models.work_items import (
    AdvancedSearchResult,
    AdvancedSearchWorkItem,
    CreateWorkItem,
    PaginatedWorkItemResponse,
    UpdateWorkItem,
    WorkItem,
    WorkItemCountResponse,
    WorkItemDetail,
    WorkItemGroupedCountResponse,
    WorkItemSearch,
)
from ..base_resource import BaseResource
from .activities import WorkItemActivities
from .attachments import WorkItemAttachments
from .comments import WorkItemComments
from .links import WorkItemLinks
from .pages import WorkItemPages
from .relations import WorkItemRelations
from .work_logs import WorkLogs


def prepare_work_item_params(
    params: WorkItemQueryParams | Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    """Serialize work-item query params for use as HTTP query params.

    Accepts either a :class:`WorkItemQueryParams` DTO or a plain mapping,
    and normalises the ``filters`` field: the API expects it as a JSON
    string in a single ``filters=`` query parameter, but callers are free
    to pass it as a dict for ergonomics. Everything else is passed through
    as-is by ``requests``' query-string encoder.
    """
    if params is None:
        return None
    if isinstance(params, WorkItemQueryParams):
        payload: dict[str, Any] = params.model_dump(exclude_none=True)
    else:
        payload = {k: v for k, v in params.items() if v is not None}
    if "filters" in payload and isinstance(payload["filters"], dict):
        payload["filters"] = json.dumps(payload["filters"], separators=(",", ":"))
    return payload


def prepare_work_item_count_params(
    params: WorkItemCountQueryParams | None,
) -> dict[str, Any] | None:
    """Serialize work-item count query params for use as HTTP query params.

    Same ``filters`` JSON-encoding logic as :func:`prepare_work_item_params`.
    """
    if params is None:
        return None
    if params.sub_group_by is not None and params.group_by is None:
        raise ValueError("sub_group_by can only be used when group_by is also provided")
    payload: dict[str, Any] = params.model_dump(exclude_none=True)
    if "filters" in payload and isinstance(payload["filters"], dict):
        payload["filters"] = json.dumps(payload["filters"], separators=(",", ":"))
    return payload


class WorkItems(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.relations = WorkItemRelations(config)
        self.links = WorkItemLinks(config)
        self.attachments = WorkItemAttachments(config)
        self.comments = WorkItemComments(config)
        self.activities = WorkItemActivities(config)
        self.work_logs = WorkLogs(config)
        self.pages = WorkItemPages(config)

    def create(self, workspace_slug: str, project_id: str, data: CreateWorkItem) -> WorkItem:
        """Create a new work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Work item data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items",
            data.model_dump(exclude_none=True),
        )
        return WorkItem.model_validate(response)

    def retrieve(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: RetrieveQueryParams | None = None,
    ) -> WorkItemDetail:
        """Retrieve a work item by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            params: Optional query parameters for expand, fields, etc.

        Example:
            # Get work item with expanded relationships
            from plane.models.schemas import RetrieveQueryParams

            work_item = client.work_items.retrieve(
                "my-workspace",
                "project-id",
                "work-item-id",
                params=RetrieveQueryParams(expand="assignees,labels,state")
            )

            # Get specific fields only
            work_item = client.work_items.retrieve(
                "my-workspace",
                "project-id",
                "work-item-id",
                params=RetrieveQueryParams(fields="id,name,priority,state")
            )
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}",
            params=query_params,
        )
        return WorkItemDetail.model_validate(response)

    def retrieve_by_identifier(
        self,
        workspace_slug: str,
        project_identifier: str,
        issue_identifier: int,
        params: RetrieveQueryParams | None = None,
    ) -> WorkItemDetail:
        """Retrieve a work item by project and issue identifiers.

        Args:
            workspace_slug: The workspace slug identifier
            project_identifier: Project identifier string
            issue_identifier: Issue sequence number
            params: Optional query parameters for expand, fields, etc.
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/work-items/{project_identifier}-{issue_identifier}",
            params=query_params,
        )
        return WorkItemDetail.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: UpdateWorkItem,
    ) -> WorkItem:
        """Update a work item by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: Updated work item data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItem.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, work_item_id: str) -> None:
        """Delete a work item by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        params: WorkItemQueryParams | None = None,
    ) -> PaginatedWorkItemResponse:
        """List work items with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters for filtering, ordering, and pagination

        Example::

            from plane.models.query_params import WorkItemQueryParams

            # PQL filter (human-readable)
            work_items = client.work_items.list(
                "my-workspace",
                "project-id",
                params=WorkItemQueryParams(pql='priority = "urgent"'),
            )

            # Structured `filters` (JSON-encoded into the query string)
            work_items = client.work_items.list(
                "my-workspace",
                "project-id",
                params=WorkItemQueryParams(
                    filters={"and": [
                        {"priority": "urgent"},
                        {"state_group__in": ["unstarted", "started"]},
                    ]},
                ),
            )
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items",
            params=prepare_work_item_params(params),
        )
        return PaginatedWorkItemResponse.model_validate(response)

    def list_workspace(
        self,
        workspace_slug: str,
        params: WorkItemQueryParams | None = None,
    ) -> PaginatedWorkItemResponse:
        """List work items across an entire workspace.

        Returns a paginated envelope of work items the caller can view,
        spanning every project in the workspace (per-project authorization
        and conditional grants are honored server-side).

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters — supports ``filters``, ``pql``,
                ``order_by``, ``cursor``, ``per_page``, ``fields``, ``expand``.

        Example::

            from plane.models.query_params import WorkItemQueryParams

            results = client.work_items.list_workspace(
                "my-workspace",
                params=WorkItemQueryParams(
                    filters={"priority": "urgent"},
                    order_by="-created_at",
                    per_page=50,
                ),
            )
        """
        response = self._get(
            f"{workspace_slug}/work-items",
            params=prepare_work_item_params(params),
        )
        return PaginatedWorkItemResponse.model_validate(response)

    def count_workspace(
        self,
        workspace_slug: str,
        params: WorkItemCountQueryParams | None = None,
    ) -> WorkItemCountResponse:
        """Return the count of work items across an entire workspace.

        Always returns :class:`WorkItemGroupedCountResponse` with fields
        ``grouped_by``, ``sub_grouped_by``, ``total_count``, and
        ``grouped_counts``.

        ``grouped_counts`` keys are raw ORM field values: UUID strings for
        FK/M2M dimensions, plain strings for ``priority`` / ``state__group``,
        ISO-date strings for ``target_date`` / ``start_date``.  ``"None"`` is
        used for work items with no value in that dimension.

        When only ``group_by`` is supplied each ``grouped_counts`` entry has
        shape ``{"count": N}``.  When ``sub_group_by`` is also supplied the
        shape becomes ``{"total_count": N, "sub_grouped_counts": {sub_key: {"count": N}}}``.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters — supports ``filters``, ``pql``,
                ``group_by``, and ``sub_group_by``.

        Example::

            from plane.models.query_params import WorkItemCountQueryParams

            # Total count (no grouping)
            result = client.work_items.count_workspace(
                "my-workspace",
                params=WorkItemCountQueryParams(
                    filters={"priority__in": ["urgent", "high"]},
                ),
            )
            print(result.total_count)  # e.g. 12

            # Grouped by priority
            result = client.work_items.count_workspace(
                "my-workspace",
                params=WorkItemCountQueryParams(group_by="priority"),
            )
            for group, entry in result.grouped_counts.items():
                print(f"{group}: {entry.count}")

            # Sub-grouped by state inside each priority
            result = client.work_items.count_workspace(
                "my-workspace",
                params=WorkItemCountQueryParams(
                    group_by="priority",
                    sub_group_by="state_id",
                ),
            )
            for group, entry in result.grouped_counts.items():
                print(f"{group}: {entry.total_count} total")
                for sub_group, sub_entry in (entry.sub_grouped_counts or {}).items():
                    print(f"  {sub_group}: {sub_entry.count}")

            # Grouped by state, filtered by PQL
            result = client.work_items.count_workspace(
                "my-workspace",
                params=WorkItemCountQueryParams(
                    pql='assignee = currentUser()',
                    group_by="state_id",
                ),
            )
        """
        response = self._get(
            f"{workspace_slug}/work-items/count",
            params=prepare_work_item_count_params(params),
        )
        return WorkItemGroupedCountResponse.model_validate(response)

    def search(
        self,
        workspace_slug: str,
        query: str,
        params: RetrieveQueryParams | None = None,
    ) -> WorkItemSearch:
        """Search work items.

        Args:
            workspace_slug: The workspace slug identifier
            query: Search query string
            params: Optional query parameters for expand, fields, etc.
        """
        search_params = {"q": query}
        if params:
            search_params.update(params.model_dump(exclude_none=True))
        response = self._get(f"{workspace_slug}/work-items/search", params=search_params)
        return WorkItemSearch.model_validate(response)

    def advanced_search(
        self,
        workspace_slug: str,
        data: AdvancedSearchWorkItem,
    ) -> list[AdvancedSearchResult]:
        """Perform advanced search on work items with filters.

        Supports text-based search via ``query`` and/or structured filters
        using recursive AND/OR groups.

        Args:
            workspace_slug: The workspace slug identifier
            data: Advanced search request with query, filters, and limit

        Example::

            from plane.models.work_items import AdvancedSearchWorkItem

            results = client.work_items.advanced_search(
                "my-workspace",
                AdvancedSearchWorkItem(
                    query="new",
                    project_id="project-uuid",
                    workspace_search=True,
                    filters={
                        "and": [
                            {"state_id": "state-uuid"},
                            {"or": [
                                {"priority": "high"},
                                {"state_id": "other-state-uuid"},
                            ]},
                        ]
                    },
                    limit=100,
                ),
            )
        """
        response = self._post(
            f"{workspace_slug}/work-items/advanced-search",
            data.model_dump(exclude_none=True),
        )
        return [AdvancedSearchResult.model_validate(item) for item in response]

    def list_archived(
        self,
        workspace_slug: str,
        project_id: str,
        params: WorkItemQueryParams | None = None,
    ) -> PaginatedWorkItemResponse:
        """List archived work items in a project.

        Supports the same ``filters`` and ``pql`` query parameters as
        :meth:`list`.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters for filtering, ordering, and pagination
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/archived-work-items",
            params=prepare_work_item_params(params),
        )
        return PaginatedWorkItemResponse.model_validate(response)

    def archive(self, workspace_slug: str, project_id: str, work_item_id: str) -> None:
        """Archive a work item.

        Only work items in a completed or cancelled state can be archived.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
        """
        self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/archive",
            {},
        )

    def unarchive(self, workspace_slug: str, project_id: str, work_item_id: str) -> None:
        """Unarchive a work item.

        Restore an archived work item to active status.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item

        Returns:
            None (HTTP 204 No Content)
        """
        self._delete(f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/unarchive")
