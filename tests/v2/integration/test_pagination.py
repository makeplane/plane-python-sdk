"""Pagination against a real server: both envelopes, and `iterate()` auto-paging
both. Rows are tagged with a per-class `external_source` marker and seeded once
per class to keep the rate-limited API key's request cost down.

Reached off the loaded `project` row. Until this refresh these four scenarios were
not expressible at all: `paginate="cursor"` and a `per_page` on `iterate` were
written here against an SDK that had neither -- see
`tests/v2/test_pagination_coverage.py` for the gap that hid, and how."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, NamedTuple

import pytest

from plane.api.v2 import LoadedProject

from .helpers import SPECS, ResourceSpec, unique_name

ROW_COUNT = 4
PER_PAGE = 2  # forces at least 2 pages over ROW_COUNT rows


class Seeded(NamedTuple):
    ops: Any
    ids: list[str]
    marker: str


@pytest.fixture(scope="class", params=sorted(SPECS), ids=sorted(SPECS))
def spec(request: pytest.FixtureRequest) -> ResourceSpec:
    """Overrides the function-scoped `spec` from conftest so the seed fixture
    below -- which must outlive a single test function -- can depend on it."""
    return SPECS[request.param]


@pytest.fixture(scope="class")
def seeded(project: LoadedProject, spec: ResourceSpec) -> Iterator[Seeded]:
    ops = spec.on(project)
    marker = unique_name(f"{spec.key}-pg")
    items = [
        spec.make_write(
            unique_name(f"{spec.key}-pg-row"), external_source=marker, external_id=str(i)
        )
        for i in range(ROW_COUNT)
    ]
    result = ops.bulk_create(items)
    result.raise_for_failures()
    ids = [row.id for row in result.results]
    yield Seeded(ops=ops, ids=ids, marker=marker)
    ops.bulk_delete(ids)


class TestPagination:
    """All four scenarios share one seeded batch per resource (see `seeded` above)."""

    def test_offset_list_one_page_reports_a_next_offset(self, seeded: Seeded) -> None:
        page = seeded.ops.list(external_source=seeded.marker, per_page=PER_PAGE)
        assert len(page.data) == PER_PAGE
        assert page.next is not None
        assert page.total_count == ROW_COUNT

    def test_offset_iter_follows_every_page(self, seeded: Seeded) -> None:
        rows = list(seeded.ops.iterate(external_source=seeded.marker, per_page=PER_PAGE))
        assert {row.id for row in rows} == set(seeded.ids)

    def test_cursor_list_one_page_uses_the_cursor_envelope(self, seeded: Seeded) -> None:
        # Both resources default-order on a non-unique float column, which the
        # server refuses to keyset on (`ordering_not_cursor_eligible`); cursor
        # pagination needs an explicit cursor-safe `order_by` (`created_at`/`id`).
        page = seeded.ops.list(
            external_source=seeded.marker,
            per_page=PER_PAGE,
            paginate="cursor",
            order_by="created_at",
        )
        assert len(page.data) == PER_PAGE
        assert page.has_more is True
        assert page.next_cursor is not None

    def test_cursor_iter_follows_every_page(self, seeded: Seeded) -> None:
        rows = list(
            seeded.ops.iterate(
                external_source=seeded.marker,
                per_page=PER_PAGE,
                paginate="cursor",
                order_by="created_at",
            )
        )
        assert {row.id for row in rows} == set(seeded.ids)

    def test_cursor_page_two_can_be_fetched_by_hand(self, seeded: Seeded) -> None:
        """The half `iterate` hides: a caller holding a `next_cursor` must be able to
        spend it. Before `list` took `cursor` there was no way to, so asking for the
        cursor envelope by hand was a dead end after page one."""
        first = seeded.ops.list(
            external_source=seeded.marker,
            per_page=PER_PAGE,
            paginate="cursor",
            order_by="created_at",
        )
        second = seeded.ops.list(
            external_source=seeded.marker,
            per_page=PER_PAGE,
            paginate="cursor",
            order_by="created_at",
            cursor=first.next_cursor,
        )
        assert {row.id for row in second.data}.isdisjoint({row.id for row in first.data})
        assert {row.id for row in first.data} | {row.id for row in second.data} <= set(seeded.ids)

    def test_count_false_drops_the_total_count(self, seeded: Seeded) -> None:
        """`?count=false` skips the `COUNT(*)`; the rows still come back, `total_count`
        does not. The kernel's `_find_one` has always sent this -- no caller could."""
        counted = seeded.ops.list(external_source=seeded.marker, per_page=PER_PAGE)
        uncounted = seeded.ops.list(external_source=seeded.marker, per_page=PER_PAGE, count=False)
        assert counted.total_count == ROW_COUNT
        assert uncounted.total_count is None
        assert len(uncounted.data) == PER_PAGE
