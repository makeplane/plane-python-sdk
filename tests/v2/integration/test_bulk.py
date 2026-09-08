"""bulk_create/bulk_update/bulk_delete against a real server: all-success,
partial failure (200 with per-row detail), and `all_or_none=True` turning
that into a 409, using a real name conflict rather than a pydantic reject.

Reached off the loaded `project` row -- bulk writes are the widest set of methods
a navigation property has to forward, so they are worth driving that way."""

from __future__ import annotations

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError

from .helpers import ResourceSpec, unique_name


class TestBulkCreate:
    def test_all_rows_succeed(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        items = [spec.make_write(unique_name(f"{spec.key}-bc")) for _ in range(3)]
        result = ops.bulk_create(items)
        try:
            assert result.succeeded == 3
            assert result.failed == 0
            assert result.failures == []
        finally:
            ops.bulk_delete([row.id for row in result.results])

    def test_partial_failure_reports_the_failing_row(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        taken_name = unique_name(f"{spec.key}-taken")
        existing = ops.create(spec.make_write(taken_name))
        good_name = unique_name(f"{spec.key}-ok")
        try:
            result = ops.bulk_create([spec.make_write(good_name), spec.make_write(taken_name)])
            assert result.succeeded == 1
            assert result.failed == 1
            assert len(result.failures) == 1
            failure = result.failures[0]
            assert failure.index == 1
            assert failure.code  # a real code, e.g. "conflict"
            assert failure.detail

            with pytest.raises(PlaneAPIError, match="1 of 2 rows failed"):
                result.raise_for_failures()

            good_row = next(r for r in result.results if r.result != "failed")
            ops.delete(good_row.id)
        finally:
            ops.delete(existing.id)

    def test_all_or_none_turns_a_failing_row_into_409(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        taken_name = unique_name(f"{spec.key}-taken-aon")
        existing = ops.create(spec.make_write(taken_name))
        good_name = unique_name(f"{spec.key}-ok-aon")
        try:
            with pytest.raises(PlaneAPIError) as exc_info:
                ops.bulk_create(
                    [spec.make_write(good_name), spec.make_write(taken_name)],
                    all_or_none=True,
                )
            assert exc_info.value.status == 409
            assert exc_info.value.code == "batch_failed"

            # Nothing was applied: the good row must not exist.
            page = ops.list(name=good_name)
            assert page.data == []
        finally:
            ops.delete(existing.id)


class TestBulkUpdate:
    def test_all_rows_succeed(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        created = ops.bulk_create(
            [spec.make_write(unique_name(f"{spec.key}-bu")) for _ in range(2)]
        )
        ids = [row.id for row in created.results]
        try:
            result = ops.bulk_update(
                [{"id": pk, spec.name_field: unique_name(f"{spec.key}-bu-renamed")} for pk in ids]
            )
            assert result.succeeded == 2
            assert result.failed == 0
        finally:
            ops.bulk_delete(ids)

    def test_partial_failure_on_unknown_id(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        created = ops.create(spec.make_write(unique_name(f"{spec.key}-bu-ok")))
        missing_id = "00000000-0000-0000-0000-000000000000"
        try:
            result = ops.bulk_update(
                [
                    {"id": created.id, spec.name_field: unique_name(f"{spec.key}-bu-renamed")},
                    {"id": missing_id, spec.name_field: "irrelevant"},
                ]
            )
            assert result.succeeded == 1
            assert result.failed == 1
            assert result.failures[0].index == 1
            assert result.failures[0].code

            with pytest.raises(PlaneAPIError):
                result.raise_for_failures()
        finally:
            ops.delete(created.id)


class TestBulkDelete:
    def test_all_rows_succeed(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        created = ops.bulk_create(
            [spec.make_write(unique_name(f"{spec.key}-bd")) for _ in range(2)]
        )
        ids = [row.id for row in created.results]
        result = ops.bulk_delete(ids)
        assert result.succeeded == 2
        assert result.failed == 0

    def test_partial_failure_on_unknown_id(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        created = ops.create(spec.make_write(unique_name(f"{spec.key}-bd-ok")))
        missing_id = "00000000-0000-0000-0000-000000000000"
        result = ops.bulk_delete([created.id, missing_id])
        assert result.succeeded == 1
        assert result.failed == 1
        assert result.failures[0].code


class TestBulkEmptyBatchRejectedClientSide:
    """The known bug fix, proven live: the client must reject `[]` itself rather
    than round-trip a request the server always 400s on `minItems: 1`."""

    def test_bulk_create_empty_batch_never_hits_the_network(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        with pytest.raises(ValueError, match="non-empty"):
            ops.bulk_create([])

    def test_bulk_delete_empty_batch_never_hits_the_network(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        with pytest.raises(ValueError, match="non-empty"):
            ops.bulk_delete([])
