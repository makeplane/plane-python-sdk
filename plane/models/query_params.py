"""Query parameter DTOs for list/retrieve endpoints."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BaseQueryParams(BaseModel):
    """Base query parameters for API requests."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    expand: str | None = Field(
        None,
        description="Comma-separated list of related fields to expand in response",
    )
    fields: str | None = Field(
        None,
        description="Comma-separated list of fields to include in response",
    )
    external_id: str | None = Field(
        None,
        description="External system identifier for filtering or lookup",
    )
    external_source: str | None = Field(
        None,
        description="External system source name for filtering or lookup",
    )
    order_by: str | None = Field(
        None,
        description="Field to order results by. Prefix with '-' for descending order",
    )


class PaginatedQueryParams(BaseQueryParams):
    """Query parameters for paginated list endpoints."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    cursor: str | None = Field(
        None,
        description="Pagination cursor for getting next set of results",
    )
    per_page: int | None = Field(
        None,
        description="Number of results per page",
        ge=1,
        le=100,
    )


class WorkItemQueryParams(PaginatedQueryParams):
    """Query parameters for work item list endpoints.

    Inherits all documented query parameters from PaginatedQueryParams:
    - cursor: Pagination cursor
    - expand: Comma-separated fields to expand
    - external_id: External system identifier
    - external_source: External system source name
    - fields: Comma-separated fields to include
    - order_by: Field to order by (prefix with '-' for descending)
    - per_page: Number of results per page (1-100)
    - pql: Plane Query Language expression for structured filtering
    - filters: JSON-serializable filter expression for structured filtering
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    pql: str | None = Field(
        None,
        description=(
            "Plane Query Language expression. Human-readable alternative to "
            '`filters`. Example: `priority = "urgent" AND assignee = currentUser()`.'
        ),
    )
    filters: dict[str, Any] | None = Field(
        None,
        description=(
            "Structured filter expression. Supports nested `and`/`or`/`not` groups "
            "and field comparisons with operators like `__in`, `__gte`, `__range`, "
            "`__isnull`, `__icontains`, etc. JSON-encoded into the `filters=` "
            "query param by the client."
        ),
    )


#: Valid field names accepted by ``group_by`` and ``sub_group_by``.
GROUP_BY_FIELDS = (
    "state_id",
    "priority",
    "assignees__id",
    "labels__id",
    "cycle_id",
    "issue_module__module_id",
    "type_id",
    "project_id",
    "state__group",
    "release_work_items__release_id",
    "milestone_id",
    "target_date",
    "start_date",
    "created_by",
)


class WorkspaceWorkItemQueryParams(WorkItemQueryParams):
    """Query parameters for the workspace-scoped work item list endpoint.

    Extends :class:`WorkItemQueryParams` with grouping and sub-issue controls
    that are specific to ``GET /workspaces/{slug}/work-items``.

    Grouping fields (``group_by``, ``sub_group_by``) change the shape of the
    ``results`` envelope:

    - Neither set → ``results`` is ``list[WorkItem]``
    - ``group_by`` only → ``results`` is ``dict[str, WorkItemGroupBucket]``
    - Both set → ``results`` is ``dict[str, dict[str, WorkItemGroupBucket]]``

    ``group_by`` and ``sub_group_by`` must differ; the server returns HTTP 400
    if they are the same.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    group_by: str | None = Field(
        None,
        description=(
            "Field to group results by. When set the paginator returns a dict of "
            "group buckets instead of a flat list. Valid values: "
            + ", ".join(f"``{f}``" for f in GROUP_BY_FIELDS)
        ),
    )
    sub_group_by: str | None = Field(
        None,
        description=(
            "Field to nest a second grouping within each top-level group. "
            "Requires ``group_by`` to be set and must differ from it. "
            "Same valid values as ``group_by``."
        ),
    )
    sub_issue: bool | None = Field(
        None,
        description=(
            "When ``False``, only top-level items and direct children of epics "
            "are returned (sub-issues are excluded). Omit or pass ``True`` to "
            "include all items regardless of parent."
        ),
    )


class RetrieveQueryParams(BaseQueryParams):
    """Query parameters for retrieve endpoints."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


__all__ = [
    "BaseQueryParams",
    "PaginatedQueryParams",
    "RetrieveQueryParams",
    "WorkItemQueryParams",
    "WorkspaceWorkItemQueryParams",
]
