"""Envelope discrimination and auto-paging."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, Literal, TypeVar

from pydantic import BaseModel

from ....errors import PlaneError
from ....models.v2.common import CursorPage, OffsetPage

T = TypeVar("T", bound=BaseModel)

Page = OffsetPage[T] | CursorPage[T]

PaginateStyle = Literal["cursor"]
"""Value of the `?paginate=` query param.

The API answers two envelopes and says which it sent in `pagination.style`, but
*choosing* the COUNT-free keyset one is the caller's, via `?paginate=cursor`. The
golden declares it on 67 of the 68 list operations, and one resource
(`AuditLogs`, `AuditLogViewSet.count_styles_enabled = False`) refuses the offset
envelope outright, so without this parameter that resource cannot be listed at all
and no other can be traversed deeply without paying for a `COUNT(*)` per page.

`?cursor=` is the page token that comes back as `CursorPage.next_cursor`. The golden
does not document it -- `iterate` below has always sent it -- but a caller holding a
`next_cursor` it cannot spend has been handed a dead end, so `list` accepts it too."""


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
