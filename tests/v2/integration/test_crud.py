"""list/retrieve/create/update/delete against a real server, parametrized over
every resource in `SPECS` via the `spec` fixture; assertions read the row's
name through `spec.name_field` and gate `color` checks on `spec.has_color`."""

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
    ops = spec.ops(client, workspace_slug, project_id)
    created = ops.create(spec.make_write(unique_name(spec.key)))
    yield created
    try:
        ops.delete(created.id)
    except Exception:
        pass


class TestList:
    def test_list_by_project_uuid(
        self, client: PlaneClient, workspace_slug: str, project_id: str, spec: ResourceSpec
    ) -> None:
        page = spec.ops(client, workspace_slug, project_id).list()
        assert isinstance(page.data, list)

    def test_list_by_project_key(
        self, client: PlaneClient, workspace_slug: str, project_key: str, spec: ResourceSpec
    ) -> None:
        page = spec.ops(client, workspace_slug, project_key).list()
        assert isinstance(page.data, list)

    def test_list_by_uuid_and_by_key_agree(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        spec: ResourceSpec,
    ) -> None:
        by_id = {row.id for row in spec.ops(client, workspace_slug, project_id).list().data}
        by_key = {row.id for row in spec.ops(client, workspace_slug, project_key).list().data}
        assert by_id == by_key

    def test_list_without_fields_returns_full_row(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        spec: ResourceSpec,
        row: Any,
    ) -> None:
        ops = spec.ops(client, workspace_slug, project_id)
        page = ops.list()
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
        ops = spec.ops(client, workspace_slug, project_id)
        page = ops.list(fields=["id", spec.name_field])
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
        ops = spec.ops(client, workspace_slug, project_id)
        fetched = ops.retrieve(row.id)
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
        ops = spec.ops(client, workspace_slug, project_id)
        fetched = ops.retrieve(row.id, fields=["id", spec.name_field])
        assert fetched.id == row.id
        assert fetched.external_id is None
        if spec.has_color:
            assert fetched.color is None


class TestCreate:
    def test_create_returns_the_written_fields(
        self, client: PlaneClient, workspace_slug: str, project_id: str, spec: ResourceSpec
    ) -> None:
        ops = spec.ops(client, workspace_slug, project_id)
        name = unique_name(spec.key)
        overrides = {"color": "#abcdef"} if spec.has_color else {}
        created = ops.create(spec.make_write(name, **overrides))
        try:
            assert getattr(created, spec.name_field) == name
            if spec.has_color:
                assert created.color == "#abcdef"
            assert created.id
        finally:
            ops.delete(created.id)


class TestUpdate:
    def test_patch_updates_only_the_given_fields(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        spec: ResourceSpec,
        row: Any,
    ) -> None:
        ops = spec.ops(client, workspace_slug, project_id)
        new_name = unique_name(f"{spec.key}-renamed")
        updated = ops.update(row.id, spec.make_patch_name(new_name))
        assert updated.id == row.id
        assert getattr(updated, spec.name_field) == new_name
        if spec.has_color:
            assert updated.color == row.color  # untouched field survives the PATCH


class TestDelete:
    def test_delete_then_retrieve_404s(
        self, client: PlaneClient, workspace_slug: str, project_id: str, spec: ResourceSpec
    ) -> None:
        ops = spec.ops(client, workspace_slug, project_id)
        created = ops.create(spec.make_write(unique_name(spec.key)))
        ops.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            ops.retrieve(created.id)
        assert exc_info.value.status == 404
