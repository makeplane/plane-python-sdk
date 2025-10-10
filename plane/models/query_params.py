"""Query parameter DTOs for list/retrieve endpoints."""

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
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class RetrieveQueryParams(BaseQueryParams):
    """Query parameters for retrieve endpoints."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


__all__ = [
    "BaseQueryParams",
    "PaginatedQueryParams",
    "RetrieveQueryParams",
    "WorkItemQueryParams",
]
