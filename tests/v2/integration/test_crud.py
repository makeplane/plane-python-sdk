"""list/retrieve/create/update/delete against a real server, parametrized over
every resource in `SPECS` via the `spec` fixture; assertions read the row's
name through `spec.name_field` and gate `color` checks on `spec.has_color`.

This is the **flat-path** half of the generic harness (`spec.flat(client)`): every
call carries `(slug, project, ...)` itself, which is what lets the same scenario run
once with a project uuid in that slot and once with the project's identifier. The
loaded-row half is `test_find_one`/`test_upsert`/`test_bulk`/`test_errors`/
`test_pagination`, which reach the same resources off a fetched `LoadedProject`.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.client import PlaneClient

from .helpers import ResourceSpec, unique_name


@pytest.fixture
def row(
    client: PlaneClient, workspace_slug: str, project_id: str, spec: ResourceSpec
) -> Iterator[Any]:
    """One freshly created row of the parametrized resource, deleted afterwards."""
    ops = spec.flat(client)
    created = ops.create(workspace_slug, project_id, spec.make_write(unique_name(spec.key)))
    yield created
    try:
        ops.delete(workspace_slug, project_id, created.id)
    except Exception:
        pass


class TestList:
    def test_list_by_project_uuid(
        self, client: PlaneClient, workspace_slug: str, project_id: str, spec: ResourceSpec
    ) -> None:
        page = spec.flat(client).list(workspace_slug, project_id)
        assert isinstance(page.data, list)

    def test_list_by_project_key(
        self, client: PlaneClient, workspace_slug: str, project_key: str, spec: ResourceSpec
    ) -> None:
        page = spec.flat(client).list(workspace_slug, project_key)
        assert isinstance(page.data, list)

    def test_list_by_uuid_and_by_key_agree(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        spec: ResourceSpec,
    ) -> None:
        ops = spec.flat(client)
        by_id = {row.id for row in ops.list(workspace_slug, project_id).data}
        by_key = {row.id for row in ops.list(workspace_slug, project_key).data}
        assert by_id == by_key

    def test_list_without_fields_returns_full_row(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        spec: ResourceSpec,
        row: Any,
    ) -> None:
        page = spec.flat(client).list(workspace_slug, project_id)
        found = next(item for item in page.data if item.id == row.id)
        assert getattr(found, spec.name_field) == getattr(row, spec.name_field)
        if spec.has_color:
            assert found.color is not None

    def test_list_with_fields_is_sparse(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        spec: ResourceSpec,
        row: Any,
    ) -> None:
        """A field not requested comes back None, not an error or a KeyError."""
        page = spec.flat(client).list(
            workspace_slug, project_id, fields=["id", spec.name_field]
        )
        found = next(item for item in page.data if item.id == row.id)
        assert getattr(found, spec.name_field) is not None
        assert found.created_at is None
        assert found.external_id is None
        if spec.has_color:
            assert found.color is None


class TestRetrieve:
    def test_retrieve_returns_the_created_row(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        spec: ResourceSpec,
        row: Any,
    ) -> None:
        fetched = spec.flat(client).retrieve(workspace_slug, project_id, row.id)
        assert fetched.id == row.id
        assert getattr(fetched, spec.name_field) == getattr(row, spec.name_field)
        if spec.has_color:
            assert fetched.color is not None

    def test_retrieve_with_fields_is_sparse(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        spec: ResourceSpec,
        row: Any,
    ) -> None:
        fetched = spec.flat(client).retrieve(
            workspace_slug, project_id, row.id, fields=["id", spec.name_field]
        )
        assert fetched.id == row.id
        assert fetched.external_id is None
        if spec.has_color:
            assert fetched.color is None


class TestCreate:
    def test_create_returns_the_written_fields(
        self, client: PlaneClient, workspace_slug: str, project_id: str, spec: ResourceSpec
    ) -> None:
        ops = spec.flat(client)
        name = unique_name(spec.key)
        overrides = {"color": "#abcdef"} if spec.has_color else {}
        created = ops.create(workspace_slug, project_id, spec.make_write(name, **overrides))
        try:
            assert getattr(created, spec.name_field) == name
            if spec.has_color:
                assert created.color == "#abcdef"
            assert created.id
        finally:
            ops.delete(workspace_slug, project_id, created.id)


class TestUpdate:
    def test_patch_updates_only_the_given_fields(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        spec: ResourceSpec,
        row: Any,
    ) -> None:
        new_name = unique_name(f"{spec.key}-renamed")
        updated = spec.flat(client).update(
            workspace_slug, project_id, row.id, spec.make_patch_name(new_name)
        )
        assert updated.id == row.id
        assert getattr(updated, spec.name_field) == new_name
        if spec.has_color:
            assert updated.color == row.color  # untouched field survives the PATCH


class TestDelete:
    def test_delete_then_retrieve_404s(
        self, client: PlaneClient, workspace_slug: str, project_id: str, spec: ResourceSpec
    ) -> None:
        ops = spec.flat(client)
        created = ops.create(workspace_slug, project_id, spec.make_write(unique_name(spec.key)))
        ops.delete(workspace_slug, project_id, created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            ops.retrieve(workspace_slug, project_id, created.id)
        assert exc_info.value.status == 404
