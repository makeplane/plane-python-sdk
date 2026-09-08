"""Work item types (project- and workspace-scoped) + custom-property attachments,
against a real server. A workspace runs in exactly one mode (project- or
workspace-managed); fixtures probe and declare a server-capability skip on conflict.

Loaded rows throughout: types off the loaded project or workspace, and each type's
attached properties off the loaded *type* (`work_item_type.properties.link([...])`),
which is where the type id comes from in the first place."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedProject, LoadedWorkspace, PlaneAPIError
from plane.models.v2.work_item_types import CreateWorkItemType, UpdateWorkItemType

from ._guard import skip_absent_capability
from .helpers import unique_name


def _skip_on_mode_conflict(exc: PlaneAPIError) -> None:
    """Common guard for both project-scoped and workspace-scoped work item type
    writes: skip on the *other* mode's 409, and on the 402 a plan/license flag
    would raise. Re-raises anything else."""
    if exc.status == 402:
        skip_absent_capability("work item types are not enabled on this workspace")
    if exc.status == 409 and exc.code in (
        "work_item_types_managed_at_workspace",
        "work_item_types_managed_at_project",
    ):
        skip_absent_capability(
            f"this workspace's work item type mode conflicts with this surface "
            f"({exc.code}) -- see api_v2/core/feature_modes.py"
        )
    raise exc


@pytest.fixture
def work_item_type(project: LoadedProject) -> Iterator[Any]:
    """One freshly created, non-default work item type, deleted afterwards.
    Skips if this workspace runs in workspace-managed mode (see module
    docstring) -- project-scoped type writes are a 409 there by design."""
    try:
        created = project.work_item_types.create(CreateWorkItemType(name=unique_name("wit")))
    except PlaneAPIError as exc:
        _skip_on_mode_conflict(exc)
        raise  # pragma: no cover -- _skip_on_mode_conflict always raises or skips
    yield created
    try:
        project.work_item_types.delete(created.id)
    except Exception:
        pass


class TestWorkItemTypesCrud:
    def test_list_and_retrieve(self, project: LoadedProject, work_item_type: Any) -> None:
        page = project.work_item_types.list()
        assert any(row.id == work_item_type.id for row in page.data)

        fetched = project.work_item_types.retrieve(work_item_type.id)
        assert fetched.id == work_item_type.id
        assert fetched.is_default is not True

    def test_update_only_touches_given_fields(
        self, project: LoadedProject, work_item_type: Any
    ) -> None:
        new_name = unique_name("wit-renamed")
        updated = project.work_item_types.update(
            work_item_type.id, UpdateWorkItemType(name=new_name)
        )
        assert updated.name == new_name

    def test_delete_then_retrieve_404s(self, project: LoadedProject) -> None:
        try:
            created = project.work_item_types.create(
                CreateWorkItemType(name=unique_name("wit-del"))
            )
        except PlaneAPIError as exc:
            _skip_on_mode_conflict(exc)
            raise  # pragma: no cover
        project.work_item_types.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project.work_item_types.retrieve(created.id)
        assert exc_info.value.status == 404


class TestWorkItemTypesActions:
    def test_mark_default_then_schema(self, project: LoadedProject, work_item_type: Any) -> None:
        # Restore the prior default afterwards: a default type cannot be deleted (409).
        prior = next((row for row in project.work_item_types.list().data if row.is_default), None)
        try:
            marked = project.work_item_types.mark_default(work_item_type.id)
            assert marked.is_default is True

            schema = project.work_item_types.schema(work_item_type.id)
            assert schema.type_id == work_item_type.id
        finally:
            if prior is not None:
                project.work_item_types.mark_default(prior.id)

    def test_enable_epic_type_is_idempotent(self, project: LoadedProject) -> None:
        # `enable` returns the project's DEFAULT (non-epic) type -- the epic type
        # is created as a side effect, not returned (`views/work_item_types.py`
        # `enable()` responds with `default_type`, which is always `is_epic=False`).
        try:
            first = project.work_item_types.enable()
        except PlaneAPIError as exc:
            _skip_on_mode_conflict(exc)
            raise  # pragma: no cover
        second = project.work_item_types.enable()
        assert first.id == second.id
        assert second.is_epic is False

        types = project.work_item_types.list().data
        assert any(row.is_epic for row in types)

    def test_import_types_enables_a_workspace_type_on_the_project(
        self, project: LoadedProject, workspace: LoadedWorkspace
    ) -> None:
        workspace_types = workspace.work_item_types.list().data
        project_type_ids = {row.id for row in project.work_item_types.list().data}
        candidates = [row for row in workspace_types if row.id not in project_type_ids]
        if not candidates:
            skip_absent_capability("no workspace-level work item type is available to import")
        target = candidates[0]

        project.work_item_types.import_types([target.id])

        imported_ids = {row.id for row in project.work_item_types.list().data}
        assert target.id in imported_ids


class TestWorkspaceWorkItemTypes:
    """Any-level types use a different path template than project-scoped
    ones -- covered separately rather than assumed to agree."""

    @pytest.fixture
    def workspace_work_item_type(self, workspace: LoadedWorkspace) -> Iterator[Any]:
        try:
            created = workspace.work_item_types.create(
                CreateWorkItemType(name=unique_name("workspace-wit"))
            )
        except PlaneAPIError as exc:
            _skip_on_mode_conflict(exc)
            raise  # pragma: no cover
        yield created
        try:
            workspace.work_item_types.delete(created.id)
        except Exception:
            pass

    def test_list_and_retrieve(
        self, workspace: LoadedWorkspace, workspace_work_item_type: Any
    ) -> None:
        page = workspace.work_item_types.list()
        assert any(row.id == workspace_work_item_type.id for row in page.data)

        fetched = workspace.work_item_types.retrieve(workspace_work_item_type.id)
        assert fetched.id == workspace_work_item_type.id

    def test_mark_default(self, workspace: LoadedWorkspace, workspace_work_item_type: Any) -> None:
        # Restore the prior default afterwards: a default type cannot be deleted (409).
        prior = next((row for row in workspace.work_item_types.list().data if row.is_default), None)
        try:
            marked = workspace.work_item_types.mark_default(workspace_work_item_type.id)
            assert marked.is_default is True
        finally:
            if prior is not None:
                workspace.work_item_types.mark_default(prior.id)


class TestWorkItemTypeProperties:
    @pytest.fixture
    def attachable_property_id(self, workspace: LoadedWorkspace) -> str:
        """An existing, unattached custom property definition to attach in tests
        below. Skips if the workspace has none -- creating one is out of this
        shard's scope (`work-item-properties.json`)."""
        try:
            # Through the resource, not `transport.request`: the hand-rolled version
            # skipped `_query`'s validation and hand-parsed the envelope.
            rows = workspace.work_item_properties.list(per_page=5).data
        except PlaneAPIError as exc:
            if exc.status in (402, 404):
                skip_absent_capability("work item properties are not available on this workspace")
            raise
        if not rows:
            skip_absent_capability("workspace has no work item property definitions to attach")
        return str(rows[0].id)

    def test_list_is_empty_on_a_fresh_type(
        self, project: LoadedProject, work_item_type: Any
    ) -> None:
        page = work_item_type.properties.list()
        assert page.data == []

    def test_attach_then_list_then_detach(
        self,
        project: LoadedProject,
        work_item_type: Any,
        attachable_property_id: str,
    ) -> None:
        attached = work_item_type.properties.link([attachable_property_id])
        assert attachable_property_id in attached.properties
        try:
            page = work_item_type.properties.list()
            assert any(p.id == attachable_property_id for p in page.data)

            fetched = work_item_type.properties.retrieve(attachable_property_id)
            assert fetched.id == attachable_property_id
        finally:
            work_item_type.properties.unlink(attachable_property_id)

        page_after = work_item_type.properties.list()
        assert all(p.id != attachable_property_id for p in page_after.data)
