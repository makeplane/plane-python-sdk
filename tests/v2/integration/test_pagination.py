"""Pagination against a real server: both envelopes, and `iterate()` auto-paging
both. Rows are tagged with a per-class `external_source` marker and seeded once
per class to keep the rate-limited API key's request cost down."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, NamedTuple

import pytest

from plane.client import PlaneClient

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
def seeded(
    client: PlaneClient, workspace_slug: str, project_id: str, spec: ResourceSpec
) -> Iterator[Seeded]:
    ops = spec.ops(client, workspace_slug, project_id)
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
