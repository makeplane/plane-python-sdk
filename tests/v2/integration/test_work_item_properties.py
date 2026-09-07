"""`proj.work_item_properties`/`ws.work_item_properties` (and their
`.options`/`.contexts` sub-resources) against a real server; not parametrized
through `helpers.SPECS` since this shard nests two independent scopes."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.work_item_properties import (
    CreateWorkItemProperty,
    CreateWorkItemPropertyContext,
    CreateWorkItemPropertyOption,
    UpdateWorkItemProperty,
    UpdateWorkItemPropertyContext,
    UpdateWorkItemPropertyOption,
)

from .helpers import unique_name


@pytest.fixture
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Any:
    return client.v2.workspace(workspace_slug).project(project_id)


@pytest.fixture
def ws(client: PlaneClient, workspace_slug: str) -> Any:
    return client.v2.workspace(workspace_slug)


def _create_project_property_or_skip(proj: Any, data: CreateWorkItemProperty) -> Any:
    try:
        return proj.work_item_properties.create(data)
    except PlaneAPIError as exc:
        if exc.status == 409 and exc.code == "work_item_types_managed_at_workspace":
            pytest.skip(
                "this workspace runs in workspace-managed work item type mode -- "
                "project-scoped property writes are a 409 by design"
            )
        raise


@pytest.fixture(scope="module")
def project_property(client: PlaneClient, workspace_slug: str, project_id: str) -> Iterator[Any]:
    """One project-scoped OPTION property, shared by every test in this module --
    sub-resources (options) hang off it and clean up their own rows."""
    proj = client.v2.workspace(workspace_slug).project(project_id)
    created = _create_project_property_or_skip(
        proj,
        CreateWorkItemProperty(display_name=unique_name("wip-project"), property_type="OPTION"),
    )
    yield created
    try:
        proj.work_item_properties.delete(created.id)
    except Exception:
        pass


def _create_workspace_property_or_skip(ws: Any, data: CreateWorkItemProperty) -> Any:
    """Any-scoped property writes require workspace-managed mode
    symmetrically to `_create_project_property_or_skip` above
    (`views/workspace_work_item_properties.py`)."""
    try:
        return ws.work_item_properties.create(data)
    except PlaneAPIError as exc:
        if exc.status == 409 and exc.code == "work_item_types_managed_at_project":
            pytest.skip(
                "this workspace runs in project-managed work item type mode -- "
                "workspace-scoped property writes are a 409 by design"
            )
        raise


@pytest.fixture(scope="module")
def workspace_property(client: PlaneClient, workspace_slug: str) -> Iterator[Any]:
    """One workspace-scoped OPTION property, shared by every test in this module --
    sub-resources (contexts, options) hang off it and clean up their own rows."""
    ws = client.v2.workspace(workspace_slug)
    created = _create_workspace_property_or_skip(
        ws,
        CreateWorkItemProperty(display_name=unique_name("wip-workspace"), property_type="OPTION"),
    )
    yield created
    try:
        ws.work_item_properties.delete(created.id)
    except Exception:
        pass


class TestProjectScopedProperties:
    def test_create_returns_the_written_fields(self, proj: Any) -> None:
        name = unique_name("wip-create")
        created = _create_project_property_or_skip(
            proj, CreateWorkItemProperty(display_name=name, property_type="TEXT")
        )
        try:
            assert created.display_name == name
            assert created.property_type == "TEXT"
            assert created.id
        finally:
            proj.work_item_properties.delete(created.id)

    def test_retrieve_returns_the_created_row(self, proj: Any, project_property: Any) -> None:
        fetched = proj.work_item_properties.retrieve(project_property.id)
        assert fetched.id == project_property.id

    def test_list_by_project_uuid_and_key_agree(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        project_property: Any,
    ) -> None:
        ws = client.v2.workspace(workspace_slug)
        by_id = {row.id for row in ws.project(project_id).work_item_properties.list().data}
        by_key = {row.id for row in ws.project(project_key).work_item_properties.list().data}
        assert project_property.id in by_id
        assert by_id == by_key

    def test_patch_updates_only_the_given_fields(self, proj: Any) -> None:
        created = _create_project_property_or_skip(
            proj,
            CreateWorkItemProperty(display_name=unique_name("wip-patch"), property_type="TEXT"),
        )
        try:
            new_name = unique_name("wip-patched")
            updated = proj.work_item_properties.update(
                created.id, UpdateWorkItemProperty(display_name=new_name)
            )
            assert updated.id == created.id
            assert updated.display_name == new_name
            assert updated.property_type == "TEXT"
        finally:
            proj.work_item_properties.delete(created.id)

    def test_delete_then_retrieve_404s(self, proj: Any) -> None:
        created = _create_project_property_or_skip(
            proj, CreateWorkItemProperty(display_name=unique_name("wip-del"), property_type="TEXT")
        )
        proj.work_item_properties.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            proj.work_item_properties.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_fields_returns_a_sparse_row(self, proj: Any, project_property: Any) -> None:
        fetched = proj.work_item_properties.retrieve(project_property.id, fields=["id"])
        assert fetched.id == project_property.id
        assert fetched.display_name is None

    def test_invalid_fields_is_rejected_client_side(self, proj: Any) -> None:
        with pytest.raises(ValueError, match="bogus"):
            proj.work_item_properties.list(fields=["bogus"])


class TestProjectScopedOptions:
    def test_crud(self, proj: Any, project_property: Any) -> None:
        created = proj.work_item_properties.options.create(
            project_property.id, CreateWorkItemPropertyOption(name=unique_name("wip-opt"))
        )
        try:
            assert created.id

            fetched = proj.work_item_properties.options.retrieve(project_property.id, created.id)
            assert fetched.id == created.id

            page = proj.work_item_properties.options.list(project_property.id)
            assert any(o.id == created.id for o in page.data)

            new_name = unique_name("wip-opt-renamed")
            updated = proj.work_item_properties.options.update(
                project_property.id, created.id, UpdateWorkItemPropertyOption(name=new_name)
            )
            assert updated.name == new_name
        finally:
            proj.work_item_properties.options.delete(project_property.id, created.id)

    def test_delete_then_retrieve_404s(self, proj: Any, project_property: Any) -> None:
        created = proj.work_item_properties.options.create(
            project_property.id, CreateWorkItemPropertyOption(name=unique_name("wip-opt-del"))
        )
        proj.work_item_properties.options.delete(project_property.id, created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            proj.work_item_properties.options.retrieve(project_property.id, created.id)
        assert exc_info.value.status == 404


class TestWorkspaceScopedProperties:
    def test_create_returns_the_written_fields(self, ws: Any) -> None:
        name = unique_name("wswip-create")
        created = _create_workspace_property_or_skip(
            ws, CreateWorkItemProperty(display_name=name, property_type="TEXT")
        )
        try:
            assert created.display_name == name
            assert created.id
        finally:
            ws.work_item_properties.delete(created.id)

    def test_retrieve_returns_the_created_row(self, ws: Any, workspace_property: Any) -> None:
        fetched = ws.work_item_properties.retrieve(workspace_property.id)
        assert fetched.id == workspace_property.id

    def test_patch_updates_only_the_given_fields(self, ws: Any) -> None:
        created = _create_workspace_property_or_skip(
            ws,
            CreateWorkItemProperty(display_name=unique_name("wswip-patch"), property_type="TEXT"),
        )
        try:
            new_name = unique_name("wswip-patched")
            updated = ws.work_item_properties.update(
                created.id, UpdateWorkItemProperty(display_name=new_name)
            )
            assert updated.display_name == new_name
        finally:
            ws.work_item_properties.delete(created.id)

    def test_delete_then_retrieve_404s(self, ws: Any) -> None:
        created = _create_workspace_property_or_skip(
            ws, CreateWorkItemProperty(display_name=unique_name("wswip-del"), property_type="TEXT")
        )
        ws.work_item_properties.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            ws.work_item_properties.retrieve(created.id)
        assert exc_info.value.status == 404


class TestWorkspaceScopedOptions:
    def test_crud(self, ws: Any, workspace_property: Any) -> None:
        created = ws.work_item_properties.options.create(
            workspace_property.id, CreateWorkItemPropertyOption(name=unique_name("wswip-opt"))
        )
        try:
            assert created.id

            fetched = ws.work_item_properties.options.retrieve(workspace_property.id, created.id)
            assert fetched.id == created.id

            page = ws.work_item_properties.options.list(workspace_property.id)
            assert any(o.id == created.id for o in page.data)

            new_name = unique_name("wswip-opt-renamed")
            updated = ws.work_item_properties.options.update(
                workspace_property.id, created.id, UpdateWorkItemPropertyOption(name=new_name)
            )
            assert updated.name == new_name
        finally:
            ws.work_item_properties.options.delete(workspace_property.id, created.id)


class TestContexts:
    def test_crud(self, ws: Any, project_id: str, workspace_property: Any) -> None:
        created = ws.work_item_properties.contexts.create(
            workspace_property.id,
            # `issue_type_ids` is required unless `applies_to_all_work_item_types`;
            # an unnamed create clashes with the auto-provisioned "Default" context
            # and surfaces as a raw 500 (unhandled `UniqueViolation`, confirmed live).
            CreateWorkItemPropertyContext(
                name=unique_name("wip-ctx"),
                project_ids=[project_id],
                applies_to_all_work_item_types=True,
                is_required=True,
            ),
        )
        try:
            assert created.id
            assert created.is_required is True

            fetched = ws.work_item_properties.contexts.retrieve(workspace_property.id, created.id)
            assert fetched.id == created.id

            page = ws.work_item_properties.contexts.list(workspace_property.id)
            assert any(c.id == created.id for c in page.data)

            updated = ws.work_item_properties.contexts.update(
                workspace_property.id, created.id, UpdateWorkItemPropertyContext(is_required=False)
            )
            assert updated.is_required is False
        finally:
            ws.work_item_properties.contexts.delete(workspace_property.id, created.id)

    def test_delete_then_retrieve_404s(
        self, ws: Any, project_id: str, workspace_property: Any
    ) -> None:
        created = ws.work_item_properties.contexts.create(
            workspace_property.id,
            CreateWorkItemPropertyContext(
                name=unique_name("wip-ctx-del"),
                project_ids=[project_id],
                applies_to_all_work_item_types=True,
            ),
        )
        ws.work_item_properties.contexts.delete(workspace_property.id, created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            ws.work_item_properties.contexts.retrieve(workspace_property.id, created.id)
        assert exc_info.value.status == 404
