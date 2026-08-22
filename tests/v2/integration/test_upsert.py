"""`upsert` against a real server: the create path and the reconcile path,
keyed on `(external_source, external_id)` -- posting the same pair twice
must update the existing row in place, not create a second one."""

from __future__ import annotations

from plane.client import PlaneClient

from .helpers import ResourceSpec, unique_name


class TestUpsert:
    def test_upsert_creates_when_no_row_matches(
        self, client: PlaneClient, workspace_slug: str, project_id: str, spec: ResourceSpec
    ) -> None:
        ops = spec.ops(client, workspace_slug, project_id)
        marker = unique_name(f"{spec.key}-upsert-create")
        created = ops.upsert(spec.make_write(marker, external_source=marker, external_id="1"))
        try:
            assert getattr(created, spec.name_field) == marker
            assert created.external_id == "1"
        finally:
            ops.delete(created.id)

    def test_upsert_reconciles_on_second_call(
        self, client: PlaneClient, workspace_slug: str, project_id: str, spec: ResourceSpec
    ) -> None:
        ops = spec.ops(client, workspace_slug, project_id)
        marker = unique_name(f"{spec.key}-upsert-reconcile")
        first = ops.upsert(spec.make_write(marker, external_source=marker, external_id="1"))
        renamed = f"{marker}-renamed"
        try:
            second = ops.upsert(spec.make_write(renamed, external_source=marker, external_id="1"))
            assert second.id == first.id, "same (external_source, external_id) must reconcile"
            assert getattr(second, spec.name_field) == renamed

            page = ops.list(external_source=marker, external_id="1")
            assert len(page.data) == 1, "reconcile must not leave a duplicate row behind"
            assert page.data[0].id == first.id
        finally:
            ops.delete(first.id)
