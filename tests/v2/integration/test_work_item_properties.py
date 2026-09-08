"""`project.work_item_properties`/`workspace.work_item_properties` (and their
`.property_options`/`.contexts` sub-resources) against a real server; not
parametrized through `helpers.SPECS` since this shard nests two independent scopes.

Loaded rows throughout, two levels deep: properties off the loaded project or
workspace, and each property's options/contexts off the loaded *property*. The
navigation property is `property_options`, not `options`, because
`WorkItemProperty.options` is a real API field -- the inlined choices an OPTION-type
property carries.

The one flat-path test is the uuid-vs-key parity check, which needs to put two
different spellings in the same path slot; a loaded project normalises them to one.

Both "wrong scope" 409s are declared server-capability skips: a workspace runs work
item types in either project-managed or workspace-managed mode, and writes to the
other scope are refused by design."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedProject, LoadedWorkspace, PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.work_item_properties import (
    CreateWorkItemProperty,
    CreateWorkItemPropertyContext,
    CreateWorkItemPropertyOption,
    UpdateWorkItemProperty,
    UpdateWorkItemPropertyContext,
    UpdateWorkItemPropertyOption,
)

from ._guard import skip_absent_capability
from .helpers import unique_name


def _create_project_property_or_skip(project: LoadedProject, data: CreateWorkItemProperty) -> Any:
    try:
        return project.work_item_properties.create(data)
    except PlaneAPIError as exc:
        if exc.status == 409 and exc.code == "work_item_types_managed_at_workspace":
            skip_absent_capability(
                "this workspace runs in workspace-managed work item type mode, so "
                "project-scoped property writes are a 409 by design"
            )
        raise


@pytest.fixture(scope="module")
def project_property(project: LoadedProject) -> Iterator[Any]:
    """One project-scoped OPTION property, shared by every test in this module --
    its options hang off the loaded row and clean up after themselves."""
    created = _create_project_property_or_skip(
        project,
        CreateWorkItemProperty(display_name=unique_name("wip-project"), property_type="OPTION"),
    )
    yield created
    try:
        project.work_item_properties.delete(created.id)
    except Exception:
        pass


def _create_workspace_property_or_skip(workspace: LoadedWorkspace, data: CreateWorkItemProperty) -> Any:
    """Any-scoped property writes require workspace-managed mode
    symmetrically to `_create_project_property_or_skip` above
    (`views/workspace_work_item_properties.py`)."""
    try:
        return workspace.work_item_properties.create(data)
    except PlaneAPIError as exc:
        if exc.status == 409 and exc.code == "work_item_types_managed_at_project":
            skip_absent_capability(
                "this workspace runs in project-managed work item type mode, so "
                "workspace-scoped property writes are a 409 by design"
            )
        raise


@pytest.fixture(scope="module")
def workspace_property(workspace: LoadedWorkspace) -> Iterator[Any]:
    """One workspace-scoped OPTION property, shared by every test in this module --
    its contexts and options hang off the loaded row and clean up after themselves."""
    created = _create_workspace_property_or_skip(
        workspace,
        CreateWorkItemProperty(display_name=unique_name("wip-workspace"), property_type="OPTION"),
    )
    yield created
    try:
        workspace.work_item_properties.delete(created.id)
    except Exception:
        pass


class TestProjectScopedProperties:
    def test_create_returns_the_written_fields(self, project: LoadedProject) -> None:
        name = unique_name("wip-create")
        created = _create_project_property_or_skip(
            project, CreateWorkItemProperty(display_name=name, property_type="TEXT")
        )
        try:
            assert created.display_name == name
            assert created.property_type == "TEXT"
            assert created.id
        finally:
            project.work_item_properties.delete(created.id)

    def test_retrieve_returns_the_created_row(self, project: LoadedProject, project_property: Any) -> None:
        fetched = project.work_item_properties.retrieve(project_property.id)
        assert fetched.id == project_property.id

    def test_list_by_project_uuid_and_key_agree(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        project_property: Any,
    ) -> None:
        properties = client.v2.workspaces.projects.work_item_properties
        by_id = {row.id for row in properties.list(workspace_slug, project_id).data}
        by_key = {row.id for row in properties.list(workspace_slug, project_key).data}
        assert project_property.id in by_id
        assert by_id == by_key

    def test_patch_updates_only_the_given_fields(self, project: LoadedProject) -> None:
        created = _create_project_property_or_skip(
            project,
            CreateWorkItemProperty(display_name=unique_name("wip-patch"), property_type="TEXT"),
        )
        try:
            new_name = unique_name("wip-patched")
            updated = project.work_item_properties.update(
                created.id, UpdateWorkItemProperty(display_name=new_name)
            )
            assert updated.id == created.id
            assert updated.display_name == new_name
            assert updated.property_type == "TEXT"
        finally:
            project.work_item_properties.delete(created.id)

    def test_delete_then_retrieve_404s(self, project: LoadedProject) -> None:
        created = _create_project_property_or_skip(
            project, CreateWorkItemProperty(display_name=unique_name("wip-del"), property_type="TEXT")
        )
        project.work_item_properties.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project.work_item_properties.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_fields_returns_a_sparse_row(self, project: LoadedProject, project_property: Any) -> None:
        fetched = project.work_item_properties.retrieve(project_property.id, fields=["id"])
        assert fetched.id == project_property.id
        assert fetched.display_name is None

    def test_invalid_fields_is_rejected_client_side(self, project: LoadedProject) -> None:
        with pytest.raises(ValueError, match="bogus"):
            # Deliberately invalid: the point is that the *kernel* rejects it against
            # the golden before any request. A type checker rejects it too, which is
            # the guard working, so the ignore is the assertion's cost of existing.
            project.work_item_properties.list(fields=["bogus"])  # type: ignore[list-item]


class TestProjectScopedOptions:
    def test_crud(self, project: LoadedProject, project_property: Any) -> None:
        created = project_property.property_options.create(
            CreateWorkItemPropertyOption(name=unique_name("wip-opt"))
        )
        try:
            assert created.id

            fetched = project_property.property_options.retrieve(created.id)
            assert fetched.id == created.id

            page = project_property.property_options.list()
            assert any(o.id == created.id for o in page.data)

            new_name = unique_name("wip-opt-renamed")
            updated = project_property.property_options.update(
                created.id, UpdateWorkItemPropertyOption(name=new_name)
            )
            assert updated.name == new_name
        finally:
            project_property.property_options.delete(created.id)

    def test_delete_then_retrieve_404s(self, project: LoadedProject, project_property: Any) -> None:
        created = project_property.property_options.create(
            CreateWorkItemPropertyOption(name=unique_name("wip-opt-del"))
        )
        project_property.property_options.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project_property.property_options.retrieve(created.id)
        assert exc_info.value.status == 404


class TestWorkspaceScopedProperties:
    def test_create_returns_the_written_fields(self, workspace: LoadedWorkspace) -> None:
        name = unique_name("wswip-create")
        created = _create_workspace_property_or_skip(
            workspace, CreateWorkItemProperty(display_name=name, property_type="TEXT")
        )
        try:
            assert created.display_name == name
            assert created.id
        finally:
            workspace.work_item_properties.delete(created.id)

    def test_retrieve_returns_the_created_row(self, workspace: LoadedWorkspace, workspace_property: Any) -> None:
        fetched = workspace.work_item_properties.retrieve(workspace_property.id)
        assert fetched.id == workspace_property.id

    def test_patch_updates_only_the_given_fields(self, workspace: LoadedWorkspace) -> None:
        created = _create_workspace_property_or_skip(
            workspace,
            CreateWorkItemProperty(display_name=unique_name("wswip-patch"), property_type="TEXT"),
        )
        try:
            new_name = unique_name("wswip-patched")
            updated = workspace.work_item_properties.update(
                created.id, UpdateWorkItemProperty(display_name=new_name)
            )
            assert updated.display_name == new_name
        finally:
            workspace.work_item_properties.delete(created.id)

    def test_delete_then_retrieve_404s(self, workspace: LoadedWorkspace) -> None:
        created = _create_workspace_property_or_skip(
            workspace, CreateWorkItemProperty(display_name=unique_name("wswip-del"), property_type="TEXT")
        )
        workspace.work_item_properties.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            workspace.work_item_properties.retrieve(created.id)
        assert exc_info.value.status == 404


class TestWorkspaceScopedOptions:
    def test_crud(self, workspace: LoadedWorkspace, workspace_property: Any) -> None:
        created = workspace_property.property_options.create(
            CreateWorkItemPropertyOption(name=unique_name("wswip-opt"))
        )
        try:
            assert created.id

            fetched = workspace_property.property_options.retrieve(created.id)
            assert fetched.id == created.id

            page = workspace_property.property_options.list()
            assert any(o.id == created.id for o in page.data)

            new_name = unique_name("wswip-opt-renamed")
            updated = workspace_property.property_options.update(
                created.id, UpdateWorkItemPropertyOption(name=new_name)
            )
            assert updated.name == new_name
        finally:
            workspace_property.property_options.delete(created.id)


class TestContexts:
    def test_crud(self, workspace: LoadedWorkspace, project_id: str, workspace_property: Any) -> None:
        created = workspace_property.contexts.create(
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

            fetched = workspace_property.contexts.retrieve(created.id)
            assert fetched.id == created.id

            page = workspace_property.contexts.list()
            assert any(c.id == created.id for c in page.data)

            updated = workspace_property.contexts.update(
                created.id, UpdateWorkItemPropertyContext(is_required=False)
            )
            assert updated.is_required is False
        finally:
            workspace_property.contexts.delete(created.id)

    def test_delete_then_retrieve_404s(
        self, workspace: LoadedWorkspace, project_id: str, workspace_property: Any
    ) -> None:
        created = workspace_property.contexts.create(
            CreateWorkItemPropertyContext(
                name=unique_name("wip-ctx-del"),
                project_ids=[project_id],
                applies_to_all_work_item_types=True,
            ),
        )
        workspace_property.contexts.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            workspace_property.contexts.retrieve(created.id)
        assert exc_info.value.status == 404
