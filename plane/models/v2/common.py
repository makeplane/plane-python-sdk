"""Envelopes and shared payloads for api_v2 responses."""

from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from ...api.v2._kernel.errors import FieldError, PlaneAPIError

T = TypeVar("T", bound=BaseModel)


class OffsetStyle(BaseModel):
    style: Literal["offset"]


class CursorStyle(BaseModel):
    style: Literal["cursor"]


class OffsetPage(BaseModel, Generic[T]):
    """Default list envelope. `total_count` is absent when the caller sent ?count=false."""

    model_config = ConfigDict(extra="allow")

    data: list[T]
    pagination: OffsetStyle
    next: int | None = None
    previous: int | None = None
    total_count: int | None = None


class CursorPage(BaseModel, Generic[T]):
    """Keyset envelope, returned when the caller sent ?paginate=cursor."""

    model_config = ConfigDict(extra="allow")

    data: list[T]
    pagination: CursorStyle
    has_more: bool = False
    next_cursor: str | None = None


class BulkRowSuccess(BaseModel):
    """A row that landed. `result` says which write happened."""

    model_config = ConfigDict(extra="allow")

    index: int
    result: Literal["created", "updated", "deleted"]
    id: str


class BulkRowFailure(BaseModel):
    """A row that did not land, carrying its own problem detail."""

    model_config = ConfigDict(extra="allow")

    index: int
    result: Literal["failed"]
    type: str = "invalid_request"
    code: str = "invalid_request"
    detail: str = ""
    errors: list["FieldError"] | None = None
    id: str | None = None


class BulkWriteResponse(BaseModel):
    """Always HTTP 200 -- read `results` for what happened; `all_or_none=True` raises
    `PlaneAPIError` (409) instead."""

    model_config = ConfigDict(extra="allow")

    results: list[BulkRowSuccess | BulkRowFailure] = Field(default_factory=list)
    succeeded: int = 0
    failed: int = 0

    @property
    def failures(self) -> list[BulkRowFailure]:
        return [row for row in self.results if isinstance(row, BulkRowFailure)]

    def raise_for_failures(self) -> None:
        """Raise if any row failed. Opt-in, because partial success is the default."""
        failures = self.failures
        if not failures:
            return
        first = failures[0]
        raise PlaneAPIError(
            status=200,
            type=first.type,
            code=first.code,
            detail=f"{len(failures)} of {len(self.results)} rows failed: {first.detail}",
            errors=first.errors,
            response=self.model_dump(),
        )


BulkRowFailure.model_rebuild()
