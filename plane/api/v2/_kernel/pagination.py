"""Envelope discrimination and auto-paging."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, TypeVar

from pydantic import BaseModel

from ....errors import PlaneError
from ....models.v2.common import CursorPage, OffsetPage

T = TypeVar("T", bound=BaseModel)

Page = OffsetPage[T] | CursorPage[T]


def parse_page(payload: Any, model: type[T]) -> Page[T]:
    """Discriminate on `pagination.style` — the API's own marker."""
    style = (payload or {}).get("pagination", {}).get("style")
    if style == "cursor":
        return CursorPage[model].model_validate(payload)  # type: ignore[valid-type]
    return OffsetPage[model].model_validate(payload)  # type: ignore[valid-type]


def iterate(fetch: Callable[[dict[str, Any]], Page[T]], params: dict[str, Any]) -> Iterator[T]:
    """Yield every row across pages, following whichever envelope came back.

    Raises `PlaneError` if the server echoes back the same offset/cursor (stalled-pager guard)."""
    current = dict(params)
    while True:
        page = fetch(current)
        yield from page.data
        if isinstance(page, CursorPage):
            if not page.has_more or not page.next_cursor:
                return
            if page.next_cursor == current.get("cursor"):
                raise PlaneError(
                    f"Pagination stalled: server returned next_cursor={page.next_cursor!r} "
                    "for the same cursor. Refusing to loop."
                )
            current["cursor"] = page.next_cursor
        else:
            if page.next is None:
                return
            if "offset" in current and page.next == current["offset"]:
                raise PlaneError(
                    f"Pagination stalled: server returned next={page.next} "
                    "for the same offset. Refusing to loop."
                )
            current["offset"] = page.next
