"""Estimates + nested estimate points against a real server, mirroring
`test_crud.py`/`test_upsert.py`/`test_bulk.py`'s conventions rather than
`helpers.SPECS`. Not verified against a live server yet."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.project import Project
from plane.client import PlaneClient
from plane.models.v2.estimates import (
    CreateEstimate,
    CreateEstimatePoint,
    UpdateEstimate,
    UpdateEstimatePoint,
)

from .helpers import unique_name


@pytest.fixture
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Project:
    return client.v2.workspace(workspace_slug).project(project_id)


@pytest.fixture
def estimate(proj: Project) -> Iterator[Any]:
    """One freshly created estimate, deleted afterwards."""
    created = proj.estimates.create(CreateEstimate(name=unique_name("estimate"), type="points"))
    yield created
    try:
        proj.estimates.delete(created.id)
    except Exception:
        pass


class TestEstimatesCrud:
    def test_list_and_retrieve(self, proj: Project, estimate: Any) -> None:
        page = proj.estimates.list()
        assert any(row.id == estimate.id for row in page.data)

        fetched = proj.estimates.retrieve(estimate.id)
        assert fetched.id == estimate.id
        assert fetched.type == "points"

    def test_update_only_touches_given_fields(self, proj: Project, estimate: Any) -> None:
        new_name = unique_name("estimate-renamed")
        updated = proj.estimates.update(estimate.id, UpdateEstimate(name=new_name))
        assert updated.name == new_name
        assert updated.type == estimate.type

    def test_delete_then_retrieve_404s(self, proj: Project) -> None:
        created = proj.estimates.create(CreateEstimate(name=unique_name("estimate-del")))
        proj.estimates.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            proj.estimates.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_sparse_fields_leave_others_none(self, proj: Project, estimate: Any) -> None:
        fetched = proj.estimates.retrieve(estimate.id, fields=["id", "name"])
        assert fetched.id == estimate.id
        assert fetched.created_at is None


class TestEstimatesUpsert:
    def test_upsert_creates_then_reconciles(self, proj: Project) -> None:
        marker = unique_name("estimate-upsert")
        first = proj.estimates.upsert(
            CreateEstimate(name=marker, external_source=marker, external_id="1"),
        )
        try:
            second = proj.estimates.upsert(
                CreateEstimate(name=f"{marker}-v2", external_source=marker, external_id="1"),
            )
            assert second.id == first.id
            assert second.name == f"{marker}-v2"
        finally:
            proj.estimates.delete(first.id)


class TestEstimatesBulk:
    def test_bulk_create_update_delete(self, proj: Project) -> None:
        # Only one item: the server allows at most one estimate per project
        # (v1 parity, `views/estimates.py`); a batch of 2+ always partially
        # conflicts, so this still exercises bulk create/update/delete safely.
        items = [CreateEstimate(name=unique_name("estimate-bulk"))]
        created = proj.estimates.bulk_create(items)
        created.raise_for_failures()
        ids = [row.id for row in created.results]
        try:
            updated = proj.estimates.bulk_update(
                [{"id": pk, "name": unique_name("estimate-bulk-renamed")} for pk in ids],
            )
            assert updated.succeeded == 1
        finally:
            deleted = proj.estimates.bulk_delete(ids)
            assert deleted.succeeded == 1


class TestEstimateExpandPoints:
    def test_expand_points_inlines_the_points_list(self, proj: Project, estimate: Any) -> None:
        created_point = proj.estimates.points.create(
            estimate.id, CreateEstimatePoint(value="1", key=0)
        )
        try:
            fetched = proj.estimates.retrieve(estimate.id, expand=["points"])
            assert fetched.points is not None
            assert any(p.id == created_point.id for p in fetched.points)
        finally:
            proj.estimates.points.delete(estimate.id, created_point.id)


class TestEstimatePointsCrud:
    def test_crud(self, proj: Project, estimate: Any) -> None:
        created = proj.estimates.points.create(estimate.id, CreateEstimatePoint(value="XS", key=1))
        try:
            assert created.estimate_id == estimate.id

            fetched = proj.estimates.points.retrieve(estimate.id, created.id)
            assert fetched.id == created.id

            page = proj.estimates.points.list(estimate.id)
            assert any(p.id == created.id for p in page.data)

            updated = proj.estimates.points.update(
                estimate.id, created.id, UpdateEstimatePoint(value="Small")
            )
            assert updated.value == "Small"
        finally:
            proj.estimates.points.delete(estimate.id, created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            proj.estimates.points.retrieve(estimate.id, created.id)
        assert exc_info.value.status == 404

    def test_upsert_creates_then_reconciles(self, proj: Project, estimate: Any) -> None:
        marker = unique_name("point-upsert")
        first = proj.estimates.points.upsert(
            estimate.id,
            CreateEstimatePoint(value="2", external_source=marker, external_id="1"),
        )
        try:
            second = proj.estimates.points.upsert(
                estimate.id,
                CreateEstimatePoint(value="3", external_source=marker, external_id="1"),
            )
            assert second.id == first.id
            assert second.value == "3"
        finally:
            proj.estimates.points.delete(estimate.id, first.id)

    def test_bulk_create_update_delete(self, proj: Project, estimate: Any) -> None:
        items = [CreateEstimatePoint(value=str(i), key=i) for i in range(3, 5)]
        created = proj.estimates.points.bulk_create(estimate.id, items)
        created.raise_for_failures()
        ids = [row.id for row in created.results]
        try:
            updated = proj.estimates.points.bulk_update(
                estimate.id, [{"id": pk, "value": "updated"} for pk in ids],
            )
            assert updated.succeeded == 2
        finally:
            deleted = proj.estimates.points.bulk_delete(estimate.id, ids)
            assert deleted.succeeded == 2
