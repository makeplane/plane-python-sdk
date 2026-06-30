"""Query parameter DTOs for list/retrieve endpoints."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .enums import CycleStatusEnum


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


class RetrieveQueryParams(BaseQueryParams):
    """Query parameters for retrieve endpoints."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class MemberQueryParams(BaseQueryParams):
    """Query parameters for workspace/project member list endpoints.

    Inherits the documented query parameters from BaseQueryParams (expand,
    fields, external_id, external_source, order_by) and adds member-specific
    filters. Text filters match case-insensitively on a substring; ``role_slug``
    matches exactly. Boolean filters narrow by membership/account flags.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    # text filters
    first_name: str | None = Field(
        None, description="Filter by member first name (case-insensitive contains)"
    )
    last_name: str | None = Field(
        None, description="Filter by member last name (case-insensitive contains)"
    )
    email: str | None = Field(
        None, description="Filter by member email (case-insensitive contains)"
    )
    display_name: str | None = Field(
        None, description="Filter by member display name (case-insensitive contains)"
    )
    role_slug: str | None = Field(None, description="Filter by role slug (exact match)")

    # boolean filters
    is_active: bool | None = Field(None, description="Filter by active membership status")
    is_bot: bool | None = Field(None, description="Filter by bot accounts")

    def to_query_params(self) -> dict[str, Any]:
        """Serialize to a query-param dict the member endpoints accept.

        Booleans are rendered as lowercase ``"true"``/``"false"`` strings so the
        backend's typed filter backend parses them (a Python ``True`` would be
        encoded as ``"True"`` and rejected with HTTP 400). Unset fields are
        dropped so they never reach the query string.
        """
        raw = self.model_dump(exclude_none=True)
        return {k: (str(v).lower() if isinstance(v, bool) else v) for k, v in raw.items()}


class MemberListQueryParams(MemberQueryParams):
    """Query parameters for the paginated member-lite list endpoints.

    Adds cursor pagination to the :class:`MemberQueryParams` filters. The lite
    endpoints default to and cap ``per_page`` at 1000.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    cursor: str | None = Field(
        None,
        description='Pagination cursor of the form "{per_page}:{page}:{offset}", '
        "e.g. 100:0:0. Use the response's next_cursor to fetch the next page.",
    )
    per_page: int | None = Field(
        None,
        description="Number of results per page (default and max 1000)",
        ge=1,
        le=1000,
    )


class LiteListQueryParams(BaseModel):
    """Query parameters for the read-only "lite" list endpoints.

    The lite list routes (``projects-lite``, ``cycles-lite``, ``modules-lite``)
    support only ordering and cursor pagination -- they expose no field filters.
    ``per_page`` defaults to and caps at 1000 on the server.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    cursor: str | None = Field(
        None,
        description='Pagination cursor of the form "{per_page}:{page}:{offset}", '
        "e.g. 1000:0:0. Use the response's next_cursor to fetch the next page.",
    )
    per_page: int | None = Field(
        None,
        description="Number of results per page (default and max 1000)",
        ge=1,
        le=1000,
    )
    order_by: str | None = Field(
        None,
        description="Field to order results by. Prefix with '-' for descending order",
    )

    def to_query_params(self) -> dict[str, Any]:
        """Serialize to a query-param dict the lite endpoints accept.

        Booleans are rendered as lowercase ``"true"``/``"false"`` strings so the
        backend parses them (a Python ``True`` would be encoded as ``"True"`` and
        rejected). Unset fields are dropped so they never reach the query string.
        """
        raw = self.model_dump(exclude_none=True)
        return {k: (str(v).lower() if isinstance(v, bool) else v) for k, v in raw.items()}


class ProjectLiteListQueryParams(LiteListQueryParams):
    """Query parameters for the projects-lite list endpoint.

    Adds the ``include_archived`` toggle to the shared lite ordering + cursor
    pagination params.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    include_archived: bool | None = Field(
        None,
        description=(
            "Include archived projects in the results. Defaults to False on the "
            "server, which excludes archived projects. Set True to restore the "
            "previous behavior of listing archived projects too."
        ),
    )


_CYCLE_STATUS_DESCRIPTION = (
    "Filter cycles by status: 'current' (started, not yet ended), 'upcoming' "
    "(starts in the future), 'completed' (ended), 'draft' (no start/end dates), "
    "or 'incomplete' (not yet finished or open-ended). Omit to return all cycles."
)


class CycleLiteListQueryParams(LiteListQueryParams):
    """Query parameters for the cycles-lite list endpoint.

    Adds the ``status`` filter to the shared lite ordering + cursor pagination
    params. Unlike the full cycles list, the lite endpoint accepts only
    ``status`` (no ``cycle_view`` alias) and always returns a paginated envelope.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    status: CycleStatusEnum | None = Field(None, description=_CYCLE_STATUS_DESCRIPTION)


class CycleListQueryParams(PaginatedQueryParams):
    """Query parameters for the full cycles list endpoint.

    Adds cycle status filtering on top of the standard pagination params.
    ``status`` is the canonical filter; ``cycle_view`` is a deprecated alias kept
    for backward compatibility. If both are sent, the server uses ``status`` and
    ignores ``cycle_view``.

    Note: with ``status=current`` (or ``cycle_view=current``) the server returns
    a bare array of cycles rather than the paginated envelope returned for all
    other values. :meth:`~plane.api.cycles.Cycles.list` handles both shapes.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    status: CycleStatusEnum | None = Field(None, description=_CYCLE_STATUS_DESCRIPTION)
    cycle_view: CycleStatusEnum | None = Field(
        None,
        description=(
            "Deprecated alias for ``status``, kept for backward compatibility. "
            "Prefer ``status``; if both are supplied the server uses ``status``."
        ),
    )

    def to_query_params(self) -> dict[str, Any]:
        """Serialize to a query-param dict, dropping unset fields."""
        return self.model_dump(exclude_none=True)


WorkItemCountGroupBy = Literal[
    "state_id",
    "state__group",
    "priority",
    "project_id",
    "type_id",
    "labels__id",
    "assignees__id",
    "issue_module__module_id",
    "release_work_items__release_id",
    "cycle_id",
    "milestone_id",
    "created_by",
    "target_date",
    "start_date",
]


class WorkItemCountQueryParams(BaseModel):
    """Query parameters for the workspace work item count endpoint.

    Accepts the same ``filters`` and ``pql`` as :class:`WorkItemQueryParams`
    plus an optional ``group_by`` field.

    Always returns a grouped envelope matching :class:`~plane.models.work_items.WorkItemGroupedCountResponse`.
    When ``group_by`` is omitted, ``grouped_counts`` is empty and ``total_count`` holds the overall count.
    When ``group_by`` is provided, ``grouped_counts`` contains per-group counts, optionally nested when ``sub_group_by`` is also provided.
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
            "Structured filter expression. JSON-encoded into the `filters=` "
            "query param by the client."
        ),
    )
    group_by: WorkItemCountGroupBy | None = Field(
        None,
        description=(
            "ORM field to group counts by. When supplied the response shape "
            "changes from a flat ``{count}`` to a grouped "
            "``{grouped_by, total_count, results}`` envelope."
        ),
    )

    sub_group_by: WorkItemCountGroupBy | None = Field(
        None,
        description=(
            "Optional second field to group by, for nested grouping. Only valid if "
            "`group_by` is also supplied. The response shape changes to include an "
            "additional nesting level in the `results` envelope."
        ),
    )


__all__ = [
    "BaseQueryParams",
    "CycleLiteListQueryParams",
    "CycleListQueryParams",
    "LiteListQueryParams",
    "MemberListQueryParams",
    "MemberQueryParams",
    "ProjectLiteListQueryParams",
    "PaginatedQueryParams",
    "RetrieveQueryParams",
    "WorkItemCountGroupBy",
    "WorkItemCountQueryParams",
    "WorkItemQueryParams",
]
