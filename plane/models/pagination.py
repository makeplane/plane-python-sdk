from pydantic import BaseModel, ConfigDict


class PaginatedResponse(BaseModel):
    """Base class for all paginated responses with common pagination properties."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    grouped_by: str | None = None
    sub_grouped_by: str | None = None
    total_count: int
    next_cursor: str
    prev_cursor: str
    next_page_results: bool
    prev_page_results: bool
    count: int
    total_pages: int
    total_results: int
    extra_stats: str | None = None
