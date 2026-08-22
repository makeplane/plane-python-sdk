"""Scope parity against a real server: `.project(project_id)` and
`.project(project_key)` must bind to the same project and agree on every
result. Only runs against `CONVERTED_SPECS` (see `helpers.py`)."""

from __future__ import annotations

import pytest

from plane.client import PlaneClient

from .helpers import CONVERTED_SPECS, ResourceSpec, unique_name


@pytest.fixture(params=sorted(CONVERTED_SPECS), ids=sorted(CONVERTED_SPECS))
def spec(request: pytest.FixtureRequest) -> ResourceSpec:
    """Overrides the function-scoped `spec` from conftest, which parametrizes over
    every resource -- this file only makes sense for the converted ones."""
    return CONVERTED_SPECS[request.param]


class TestScopeParity:
    def test_list_agrees(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        spec: ResourceSpec,
    ) -> None:
        by_id = spec.ops(client, workspace_slug, project_id).list()
        by_key = spec.ops(client, workspace_slug, project_key).list()
        assert {row.id for row in by_id.data} == {row.id for row in by_key.data}

    def test_create_retrieve_update_delete_agree(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        spec: ResourceSpec,
    ) -> None:
        by_id = spec.ops(client, workspace_slug, project_id)
        by_key = spec.ops(client, workspace_slug, project_key)

        created_via_id = by_id.create(spec.make_write(unique_name(f"{spec.key}-scope")))
        fetched_via_key = by_key.retrieve(created_via_id.id)
        assert fetched_via_key.id == created_via_id.id
        assert getattr(fetched_via_key, spec.name_field) == getattr(
            created_via_id, spec.name_field
        )

        new_name = unique_name(f"{spec.key}-scope-renamed")
        updated_via_key = by_key.update(created_via_id.id, spec.make_patch_name(new_name))
        assert getattr(updated_via_key, spec.name_field) == new_name

        fetched_via_id = by_id.retrieve(created_via_id.id)
        assert getattr(fetched_via_id, spec.name_field) == new_name

        by_id.delete(created_via_id.id)

    def test_find_by_name_agrees(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        spec: ResourceSpec,
    ) -> None:
        by_id = spec.ops(client, workspace_slug, project_id)
        by_key = spec.ops(client, workspace_slug, project_key)
        name = unique_name(f"{spec.key}-scope-find")
        created = by_id.create(spec.make_write(name))
        try:
            found_via_id = by_id.find_by_name(name)
            found_via_key = by_key.find_by_name(name)
            assert found_via_id.id == found_via_key.id == created.id
        finally:
            by_id.delete(created.id)
