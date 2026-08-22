from typing import Any

import pytest
from pydantic import BaseModel

from plane.api.v2._kernel.pagination import iterate, parse_page
from plane.errors import PlaneError
from plane.models.v2.common import CursorPage, OffsetPage


class Row(BaseModel):
    id: str
    name: str | None = None


def test_parses_offset_envelope() -> None:
    page = parse_page(
        {
            "data": [{"id": "1", "name": "Todo"}],
            "pagination": {"style": "offset"},
            "next": 50,
            "previous": None,
            "total_count": 123,
        },
        Row,
    )
    assert isinstance(page, OffsetPage)
    assert page.total_count == 123
    assert page.data[0].name == "Todo"


def test_parses_cursor_envelope() -> None:
    page = parse_page(
        {
            "data": [{"id": "1"}],
            "pagination": {"style": "cursor"},
            "has_more": True,
            "next_cursor": "b3A9MTcx",
        },
        Row,
    )
    assert isinstance(page, CursorPage)
    assert page.next_cursor == "b3A9MTcx"


def test_iterate_follows_offset_pages() -> None:
    pages = [
        {"data": [{"id": "1"}], "pagination": {"style": "offset"}, "next": 1},
        {"data": [{"id": "2"}], "pagination": {"style": "offset"}, "next": None},
    ]
    seen: list[dict[str, Any]] = []

    def fetch(params: dict[str, Any]) -> Any:
        seen.append(dict(params))
        return parse_page(pages[len(seen) - 1], Row)

    assert [row.id for row in iterate(fetch, {})] == ["1", "2"]
    assert seen[1]["offset"] == 1


def test_iterate_follows_cursor_pages() -> None:
    pages = [
        {
            "data": [{"id": "1"}],
            "pagination": {"style": "cursor"},
            "has_more": True,
            "next_cursor": "c1",
        },
        {
            "data": [{"id": "2"}],
            "pagination": {"style": "cursor"},
            "has_more": False,
            "next_cursor": None,
        },
    ]
    seen: list[dict[str, Any]] = []

    def fetch(params: dict[str, Any]) -> Any:
        seen.append(dict(params))
        return parse_page(pages[len(seen) - 1], Row)

    assert [row.id for row in iterate(fetch, {"paginate": "cursor"})] == ["1", "2"]
    assert seen[1]["cursor"] == "c1"


def test_iterate_raises_on_stalled_offset_page() -> None:
    """A server that keeps echoing the same `next` offset must not spin forever."""
    responses = [
        {"data": [{"id": "1"}], "pagination": {"style": "offset"}, "next": 3},
        {"data": [{"id": "2"}], "pagination": {"style": "offset"}, "next": 3},
    ]
    calls = iter(responses)

    def fetch(params: dict[str, Any]) -> Any:
        return parse_page(next(calls), Row)

    with pytest.raises(PlaneError, match="Pagination stalled"):
        list(iterate(fetch, {}))


def test_iterate_raises_on_stalled_cursor_page() -> None:
    """A server that keeps echoing the same `next_cursor` must not spin forever."""
    responses = [
        {
            "data": [{"id": "1"}],
            "pagination": {"style": "cursor"},
            "has_more": True,
            "next_cursor": "c1",
        },
        {
            "data": [{"id": "2"}],
            "pagination": {"style": "cursor"},
            "has_more": True,
            "next_cursor": "c1",
        },
    ]
    calls = iter(responses)

    def fetch(params: dict[str, Any]) -> Any:
        return parse_page(next(calls), Row)

    with pytest.raises(PlaneError, match="Pagination stalled"):
        list(iterate(fetch, {"paginate": "cursor"}))


def test_iterate_allows_next_zero_on_first_offset_page() -> None:
    """`next=0` on the very first page is legitimate, not a stall: there was no
    prior `offset` param to have echoed back."""
    pages = [
        {"data": [{"id": "1"}], "pagination": {"style": "offset"}, "next": 0},
        {"data": [{"id": "2"}], "pagination": {"style": "offset"}, "next": None},
    ]
    seen: list[dict[str, Any]] = []

    def fetch(params: dict[str, Any]) -> Any:
        seen.append(dict(params))
        return parse_page(pages[len(seen) - 1], Row)

    assert [row.id for row in iterate(fetch, {})] == ["1", "2"]
    assert seen[1]["offset"] == 0
