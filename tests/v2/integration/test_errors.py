"""Error contract against a real server: a 404 and a field-validation 400;
`PlaneAPIError` carries `.status`/`.code`/`.detail` always, and `.errors`
(a list of field entries) for per-field validation failures.

Reached off the loaded `project` row: an error raised through navigation must be
the same `PlaneAPIError`, not something `Owned` wrapped or swallowed."""

from __future__ import annotations

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError

from .helpers import ResourceSpec, unique_name

MISSING_ID = "00000000-0000-0000-0000-000000000000"


class TestNotFound:
    def test_retrieve_missing_id_surfaces_404(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        with pytest.raises(PlaneAPIError) as exc_info:
            ops.retrieve(MISSING_ID)
        error = exc_info.value
        assert error.status == 404
        assert error.code == "not_found"
        assert error.detail


class TestValidationFailure:
    def test_over_length_name_surfaces_field_errors(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        too_long = unique_name(spec.key) + ("x" * 300)
        with pytest.raises(PlaneAPIError) as exc_info:
            ops.create(spec.make_write(too_long))
        error = exc_info.value
        assert error.status == 400
        assert error.errors is not None
        assert any(field_error.field == spec.name_field for field_error in error.errors)
