from collections.abc import Mapping
from typing import Any

from ..models.cycles import (
    CreateCycle,
    Cycle,
    PaginatedArchivedCycleResponse,
    PaginatedCycleLiteResponse,
    PaginatedCycleResponse,
    PaginatedCycleWorkItemResponse,
    TransferCycleWorkItemsRequest,
    UpdateCycle,
)
from ..models.query_params import (
    CycleListQueryParams,
    CycleLiteListQueryParams,
    WorkItemQueryParams,
)
from .base_resource import BaseResource
from .work_items.base import prepare_work_item_params


class Cycles(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, project_id: str, data: CreateCycle) -> Cycle:
        """Create a new cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Cycle data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/cycles",
            data.model_dump(exclude_none=True),
        )
        return Cycle.model_validate(response)

    def retrieve(self, workspace_slug: str, project_id: str, cycle_id: str) -> Cycle:
        """Retrieve a cycle by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}")
        return Cycle.model_validate(response)

    def update(
        self, workspace_slug: str, project_id: str, cycle_id: str, data: UpdateCycle
    ) -> Cycle:
        """Update a cycle by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
            data: Updated cycle data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}",
            data.model_dump(exclude_none=True),
        )
        return Cycle.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, cycle_id: str) -> None:
        """Delete a cycle by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        params: CycleListQueryParams | Mapping[str, Any] | None = None,
    ) -> PaginatedCycleResponse | list[Cycle]:
        """List cycles with optional filtering parameters.

        Supports cycle status filtering via :class:`CycleListQueryParams`. Pass
        ``status`` (canonical) or the deprecated ``cycle_view`` alias with one of
        ``current``, ``upcoming``, ``completed``, ``draft``, ``incomplete``; if
        both are supplied the server uses ``status``.

        .. note::
            With ``status=current`` (or ``cycle_view=current``) the server
            returns a **bare list** of :class:`Cycle` objects instead of the
            paginated :class:`PaginatedCycleResponse` envelope returned for all
            other values. This method returns whichever shape the server sends.
            The :meth:`list_lite` endpoint always paginates, even for
            ``status=current``.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters. Prefer ``CycleListQueryParams``;
                a plain mapping is also accepted for backwards compatibility.
        """
        if isinstance(params, CycleListQueryParams):
            query_params: Mapping[str, Any] | None = params.to_query_params()
        else:
            query_params = params
        response = self._get(f"{workspace_slug}/projects/{project_id}/cycles", params=query_params)
        if isinstance(response, list):
            return [Cycle.model_validate(item) for item in response]
        return PaginatedCycleResponse.model_validate(response)

    def list_lite(
        self,
        workspace_slug: str,
        project_id: str,
        params: CycleLiteListQueryParams | None = None,
    ) -> PaginatedCycleLiteResponse:
        """List cycles as a paginated "lite" response.

        Calls the read-only ``/cycles-lite/`` endpoint, which returns the full
        cycle field set minus the issue-count metric annotations (total_issues,
        completed_issues, etc.), suitable for pickers and reference lookups.
        Supports ordering, cursor pagination, and a ``status`` filter -- there
        are no field filters. ``per_page`` defaults to and caps at 1000. Unlike
        the full cycles list, the lite endpoint accepts only ``status`` (no
        ``cycle_view`` alias).

        Unlike the full ``cycles`` list endpoint (where ``status=current``
        returns a bare array), this endpoint always returns the paginated
        envelope for every ``status`` value.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional ordering + cursor pagination query parameters,
                plus the ``status`` filter
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/cycles-lite",
            params=params.to_query_params() if params else None,
        )
        return PaginatedCycleLiteResponse.model_validate(response)

    def list_archived(
        self, workspace_slug: str, project_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedArchivedCycleResponse:
        """List archived cycles with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/archived-cycles", params=params
        )
        return PaginatedArchivedCycleResponse.model_validate(response)

    def add_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        cycle_id: str,
        issue_ids: [str],
    ) -> None:
        """Add work items to a cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
            issue_ids: List of issue IDs to add to the cycle
        """
        return self._post(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues",
            {"issues": issue_ids},
        )

    def remove_work_item(
        self, workspace_slug: str, project_id: str, cycle_id: str, work_item_id: str
    ) -> None:
        """Remove a work item from a cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
            work_item_id: UUID of the work item
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{work_item_id}"
        )

    def list_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        cycle_id: str,
        params: WorkItemQueryParams | Mapping[str, Any] | None = None,
    ) -> PaginatedCycleWorkItemResponse:
        """List work items in a cycle.

        Supports the same ``filters`` and ``pql`` query parameters as
        :meth:`WorkItems.list`. ``filters`` is JSON-encoded into the query
        string for both the DTO and the mapping path, so callers can pass
        a dict either way.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
            params: Optional query parameters. Prefer ``WorkItemQueryParams``;
                a plain mapping is also accepted for backwards compatibility.
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues",
            params=prepare_work_item_params(params),
        )
        return PaginatedCycleWorkItemResponse.model_validate(response)

    def transfer_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        cycle_id: str,
        data: TransferCycleWorkItemsRequest,
    ) -> None:
        """Transfer work items from one cycle to another.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the source cycle
            data: Transfer request with target cycle
        """
        return self._post(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/transfer-issues",
            data.model_dump(exclude_none=True),
        )

    def archive(self, workspace_slug: str, project_id: str, cycle_id: str) -> bool:
        """Archive a cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
        """
        self._post(f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/archive", {})
        return True

    def unarchive(self, workspace_slug: str, project_id: str, cycle_id: str) -> bool:
        """Unarchive a cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
        """
        self._delete(f"{workspace_slug}/projects/{project_id}/archived-cycles/{cycle_id}/unarchive")
        return True
