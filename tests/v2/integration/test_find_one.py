"""`find_by_name` against a real server: single, zero, and multiple match.
The `?name=` filter is case-insensitive but uniqueness is case-sensitive, so
two differently-cased rows both legally exist and both match one lookup.

Reached off the loaded `project` row (`project.states.find_by_name(name)`), so the
server-side `_find_one` shape is exercised through navigation, not only flat."""

from __future__ import annotations

import pytest

from plane.api.v2 import LoadedProject, MultipleMatchesFound, NoMatchFound

from .helpers import ResourceSpec, unique_name


class TestFindByName:
    def test_single_match(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        name = unique_name(f"{spec.key}-single")
        created = ops.create(spec.make_write(name))
        try:
            found = ops.find_by_name(name)
            assert found.id == created.id
        finally:
            ops.delete(created.id)

    def test_zero_match_raises_no_match_found(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        with pytest.raises(NoMatchFound):
            ops.find_by_name(unique_name(f"{spec.key}-does-not-exist"))

    def test_multiple_match_raises_multiple_matches_found(
        self, project: LoadedProject, spec: ResourceSpec
    ) -> None:
        ops = spec.on(project)
        base = unique_name(f"{spec.key}-multi")
        lower = ops.create(spec.make_write(base.lower()))
        upper = ops.create(spec.make_write(base.upper()))
        try:
            with pytest.raises(MultipleMatchesFound):
                ops.find_by_name(base)
        finally:
            ops.delete(lower.id)
            ops.delete(upper.id)
