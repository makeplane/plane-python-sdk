"""Estimates + nested estimate points against a real server, mirroring
`test_crud.py`/`test_upsert.py`/`test_bulk.py`'s conventions rather than
`helpers.SPECS`. Not verified against a live server yet.

The whole file is loaded-row navigation, two levels of it: estimates off the loaded
`project`, points off each loaded *estimate*. The points calls used to read
`project.estimates.points.create(estimate.id, ...)`, which is not a route -- see
`tests/v2/test_owned_sub_resources.py` for what that expression used to do. The
navigation property is `estimate_points`, not `points`, because `Estimate.points` is
a real API field: the inline point data `expand=["points"]` returns, which
`test_expand_points_inlines_the_points_list` below reads."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError
from plane.models.v2.estimates import (
    CreateEstimate,
    CreateEstimatePoint,
    UpdateEstimate,
    UpdateEstimatePoint,
)

from .helpers import unique_name


@pytest.fixture
def estimate(project: LoadedProject) -> Iterator[Any]:
    """One freshly created estimate, deleted afterwards."""
    created = project.estimates.create(CreateEstimate(name=unique_name("estimate"), type="points"))
    yield created
    try:
        project.estimates.delete(created.id)
    except Exception:
        pass


class TestEstimatesCrud:
    def test_list_and_retrieve(self, project: LoadedProject, estimate: Any) -> None:
        page = project.estimates.list()
        assert any(row.id == estimate.id for row in page.data)

        fetched = project.estimates.retrieve(estimate.id)
        assert fetched.id == estimate.id
        assert fetched.type == "points"

    def test_update_only_touches_given_fields(self, project: LoadedProject, estimate: Any) -> None:
        new_name = unique_name("estimate-renamed")
        updated = project.estimates.update(estimate.id, UpdateEstimate(name=new_name))
        assert updated.name == new_name
        assert updated.type == estimate.type

    def test_delete_then_retrieve_404s(self, project: LoadedProject) -> None:
        created = project.estimates.create(CreateEstimate(name=unique_name("estimate-del")))
        project.estimates.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project.estimates.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_sparse_fields_leave_others_none(self, project: LoadedProject, estimate: Any) -> None:
        fetched = project.estimates.retrieve(estimate.id, fields=["id", "name"])
        assert fetched.id == estimate.id
        assert fetched.created_at is None


class TestEstimatesUpsert:
    def test_upsert_creates_then_reconciles(self, project: LoadedProject) -> None:
        marker = unique_name("estimate-upsert")
        first = project.estimates.upsert(
            CreateEstimate(name=marker, external_source=marker, external_id="1"),
        )
        try:
            second = project.estimates.upsert(
                CreateEstimate(name=f"{marker}-v2", external_source=marker, external_id="1"),
            )
            assert second.id == first.id
            assert second.name == f"{marker}-v2"
        finally:
            project.estimates.delete(first.id)


class TestEstimatesBulk:
    def test_bulk_create_update_delete(self, project: LoadedProject) -> None:
        # Only one item: the server allows at most one estimate per project
        # (v1 parity, `views/estimates.py`); a batch of 2+ always partially
        # conflicts, so this still exercises bulk create/update/delete safely.
        items = [CreateEstimate(name=unique_name("estimate-bulk"))]
        created = project.estimates.bulk_create(items)
        created.raise_for_failures()
        # Narrowed on `result` rather than indexed blindly: a bulk envelope mixes
        # `BulkRowSuccess` (which always carries an id) with `BulkRowFailure` (which
        # may not), and `raise_for_failures()` above only guarantees there are none.
        ids = [row.id for row in created.results if row.result != "failed"]
        try:
            updated = project.estimates.bulk_update(
                [{"id": pk, "name": unique_name("estimate-bulk-renamed")} for pk in ids],
            )
            assert updated.succeeded == 1
        finally:
            deleted = project.estimates.bulk_delete(ids)
            assert deleted.succeeded == 1


class TestEstimateExpandPoints:
    def test_expand_points_inlines_the_points_list(self, project: LoadedProject, estimate: Any) -> None:
        created_point = estimate.estimate_points.create(CreateEstimatePoint(value="1", key=0))
        try:
            fetched = project.estimates.retrieve(estimate.id, expand=["points"])
            assert fetched.points is not None
            assert any(p.id == created_point.id for p in fetched.points)
        finally:
            estimate.estimate_points.delete(created_point.id)


class TestEstimatePointsCrud:
    def test_crud(self, project: LoadedProject, estimate: Any) -> None:
        created = estimate.estimate_points.create(CreateEstimatePoint(value="XS", key=1))
        try:
            assert created.estimate_id == estimate.id

            fetched = estimate.estimate_points.retrieve(created.id)
            assert fetched.id == created.id

            page = estimate.estimate_points.list()
            assert any(p.id == created.id for p in page.data)

            updated = estimate.estimate_points.update(
                created.id, UpdateEstimatePoint(value="Small")
            )
            assert updated.value == "Small"
        finally:
            estimate.estimate_points.delete(created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            estimate.estimate_points.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_upsert_creates_then_reconciles(self, project: LoadedProject, estimate: Any) -> None:
        marker = unique_name("point-upsert")
        first = estimate.estimate_points.upsert(
            CreateEstimatePoint(value="2", external_source=marker, external_id="1")
        )
        try:
            second = estimate.estimate_points.upsert(
                CreateEstimatePoint(value="3", external_source=marker, external_id="1")
            )
            assert second.id == first.id
            assert second.value == "3"
        finally:
            estimate.estimate_points.delete(first.id)

    def test_bulk_create_update_delete(self, project: LoadedProject, estimate: Any) -> None:
        items = [CreateEstimatePoint(value=str(i), key=i) for i in range(3, 5)]
        created = estimate.estimate_points.bulk_create(items)
        created.raise_for_failures()
        ids = [row.id for row in created.results]
        try:
            updated = estimate.estimate_points.bulk_update(
                [{"id": pk, "value": "updated"} for pk in ids]
            )
            assert updated.succeeded == 2
        finally:
            deleted = estimate.estimate_points.bulk_delete(ids)
            assert deleted.succeeded == 2
