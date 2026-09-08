"""Scope parity against a real server: a project's uuid and its identifier must
address the same project, and agree on every result.

This is a flat-path file by necessity, not by preference. The `project` path slot
takes either form, so the same `spec.flat(client)` resource can be called both ways
and the two answers compared. A loaded row cannot express it: `Projects._row_id` is
`identifier`, so a project fetched *by uuid* still binds its children with the
identifier -- correct behaviour, and it means navigation has only one of the two
spellings to offer.

It now runs over every resource in `SPECS`. It used to run over `CONVERTED_SPECS`, a
subset that existed because cycles/modules/milestones had not been migrated off the
retired locator; with the migration complete that distinction is gone and the subset
with it, so cycles, modules and milestones are covered here for the first time.
"""

from __future__ import annotations

from plane.client import PlaneClient

from .helpers import ResourceSpec, unique_name


class TestScopeParity:
    def test_list_agrees(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        spec: ResourceSpec,
    ) -> None:
        ops = spec.flat(client)
        by_id = ops.list(workspace_slug, project_id)
        by_key = ops.list(workspace_slug, project_key)
        assert {row.id for row in by_id.data} == {row.id for row in by_key.data}

    def test_create_retrieve_update_delete_agree(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        spec: ResourceSpec,
    ) -> None:
        ops = spec.flat(client)

        created_via_id = ops.create(
            workspace_slug, project_id, spec.make_write(unique_name(f"{spec.key}-scope"))
        )
        fetched_via_key = ops.retrieve(workspace_slug, project_key, created_via_id.id)
        assert fetched_via_key.id == created_via_id.id
        assert getattr(fetched_via_key, spec.name_field) == getattr(created_via_id, spec.name_field)

        new_name = unique_name(f"{spec.key}-scope-renamed")
        updated_via_key = ops.update(
            workspace_slug, project_key, created_via_id.id, spec.make_patch_name(new_name)
        )
        assert getattr(updated_via_key, spec.name_field) == new_name

        fetched_via_id = ops.retrieve(workspace_slug, project_id, created_via_id.id)
        assert getattr(fetched_via_id, spec.name_field) == new_name

        ops.delete(workspace_slug, project_id, created_via_id.id)

    def test_find_by_name_agrees(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        spec: ResourceSpec,
    ) -> None:
        ops = spec.flat(client)
        name = unique_name(f"{spec.key}-scope-find")
        created = ops.create(workspace_slug, project_id, spec.make_write(name))
        try:
            found_via_id = ops.find_by_name(workspace_slug, project_id, name)
            found_via_key = ops.find_by_name(workspace_slug, project_key, name)
            assert found_via_id.id == found_via_key.id == created.id
        finally:
            ops.delete(workspace_slug, project_id, created.id)
