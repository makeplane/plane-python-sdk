"""Work item types (project- and workspace-scoped) + custom-property
attachments, against a real server. A workspace runs in exactly one mode
(project- or workspace-managed); fixtures probe and skip on mode conflict."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.project import Project
from plane.api.v2.workspace import Workspace
from plane.client import PlaneClient
from plane.models.v2.work_item_types import CreateWorkItemType, UpdateWorkItemType

from .helpers import unique_name


def _skip_on_mode_conflict(exc: PlaneAPIError) -> None:
    """Common guard for both project-scoped and workspace-scoped work item type
    writes: skip on the *other* mode's 409, and on the 402 a plan/license flag
    would raise. Re-raises anything else."""
    if exc.status == 402:
        pytest.skip("work item types feature not enabled on this workspace")
    if exc.status == 409 and exc.code in (
        "work_item_types_managed_at_workspace",
        "work_item_types_managed_at_project",
    ):
        pytest.skip(
            f"this workspace's work item type mode conflicts with this surface "
            f"({exc.code}) -- see api_v2/core/feature_modes.py"
        )
    raise exc


@pytest.fixture
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Project:
    return client.v2.workspace(workspace_slug).project(project_id)


@pytest.fixture
def ws(client: PlaneClient, workspace_slug: str) -> Workspace:
    return client.v2.workspace(workspace_slug)


@pytest.fixture
def work_item_type(proj: Project) -> Iterator[Any]:
    """One freshly created, non-default work item type, deleted afterwards.
    Skips if this workspace runs in workspace-managed mode (see module
    docstring) -- project-scoped type writes are a 409 there by design."""
    try:
        created = proj.work_item_types.create(CreateWorkItemType(name=unique_name("wit")))
    except PlaneAPIError as exc:
        _skip_on_mode_conflict(exc)
        raise  # pragma: no cover -- _skip_on_mode_conflict always raises or skips
    yield created
    try:
        proj.work_item_types.delete(created.id)
    except Exception:
        pass


class TestWorkItemTypesCrud:
    def test_list_and_retrieve(self, proj: Project, work_item_type: Any) -> None:
        page = proj.work_item_types.list()
        assert any(row.id == work_item_type.id for row in page.data)

        fetched = proj.work_item_types.retrieve(work_item_type.id)
        assert fetched.id == work_item_type.id
        assert fetched.is_default is not True

    def test_update_only_touches_given_fields(self, proj: Project, work_item_type: Any) -> None:
        new_name = unique_name("wit-renamed")
        updated = proj.work_item_types.update(work_item_type.id, UpdateWorkItemType(name=new_name))
        assert updated.name == new_name

    def test_delete_then_retrieve_404s(self, proj: Project) -> None:
        try:
            created = proj.work_item_types.create(CreateWorkItemType(name=unique_name("wit-del")))
        except PlaneAPIError as exc:
            _skip_on_mode_conflict(exc)
            raise  # pragma: no cover
        proj.work_item_types.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            proj.work_item_types.retrieve(created.id)
        assert exc_info.value.status == 404


class TestWorkItemTypesActions:
    def test_mark_default_then_schema(self, proj: Project, work_item_type: Any) -> None:
        # Restore the prior default afterwards: a default type cannot be deleted (409).
        prior = next((row for row in proj.work_item_types.list().data if row.is_default), None)
        try:
            marked = proj.work_item_types.mark_default(work_item_type.id)
            assert marked.is_default is True

            schema = proj.work_item_types.schema(work_item_type.id)
            assert schema.type_id == work_item_type.id
        finally:
            if prior is not None:
                proj.work_item_types.mark_default(prior.id)

    def test_enable_epic_type_is_idempotent(self, proj: Project) -> None:
        # `enable` returns the project's DEFAULT (non-epic) type -- the epic type
        # is created as a side effect, not returned (`views/work_item_types.py`
        # `enable()` responds with `default_type`, which is always `is_epic=False`).
        try:
            first = proj.work_item_types.enable()
        except PlaneAPIError as exc:
            _skip_on_mode_conflict(exc)
            raise  # pragma: no cover
        second = proj.work_item_types.enable()
        assert first.id == second.id
        assert second.is_epic is False

        types = proj.work_item_types.list().data
        assert any(row.is_epic for row in types)

    def test_import_types_enables_a_workspace_type_on_the_project(
        self, proj: Project, ws: Workspace
    ) -> None:
        workspace_types = ws.work_item_types.list().data
        project_type_ids = {row.id for row in proj.work_item_types.list().data}
        candidates = [row for row in workspace_types if row.id not in project_type_ids]
        if not candidates:
            pytest.skip("no workspace-level work item type is available to import")
        target = candidates[0]

        proj.work_item_types.import_types([target.id])

        imported_ids = {row.id for row in proj.work_item_types.list().data}
        assert target.id in imported_ids


class TestWorkspaceWorkItemTypes:
    """Workspace-level types use a different path template than project-scoped
    ones -- covered separately rather than assumed to agree."""

    @pytest.fixture
    def workspace_work_item_type(self, ws: Workspace) -> Iterator[Any]:
        try:
            created = ws.work_item_types.create(
                CreateWorkItemType(name=unique_name("workspace-wit"))
            )
        except PlaneAPIError as exc:
            _skip_on_mode_conflict(exc)
            raise  # pragma: no cover
        yield created
        try:
            ws.work_item_types.delete(created.id)
        except Exception:
            pass

    def test_list_and_retrieve(self, ws: Workspace, workspace_work_item_type: Any) -> None:
        page = ws.work_item_types.list()
        assert any(row.id == workspace_work_item_type.id for row in page.data)

        fetched = ws.work_item_types.retrieve(workspace_work_item_type.id)
        assert fetched.id == workspace_work_item_type.id

    def test_mark_default(self, ws: Workspace, workspace_work_item_type: Any) -> None:
        # Restore the prior default afterwards: a default type cannot be deleted (409).
        prior = next((row for row in ws.work_item_types.list().data if row.is_default), None)
        try:
            marked = ws.work_item_types.mark_default(workspace_work_item_type.id)
            assert marked.is_default is True
        finally:
            if prior is not None:
                ws.work_item_types.mark_default(prior.id)


class TestWorkItemTypeProperties:
    @pytest.fixture
    def attachable_property_id(self, client: PlaneClient, workspace_slug: str) -> str:
        """An existing, unattached custom property definition to attach in tests
        below. Skips if the workspace has none -- creating one is out of this
        shard's scope (`work-item-properties.json`)."""
        try:
            payload = client.v2.transport.request(
                "GET", f"/workspaces/{workspace_slug}/work-item-properties/", params={"per_page": 5}
            )
        except PlaneAPIError as exc:
            if exc.status in (402, 404):
                pytest.skip("work item properties not available on this workspace")
            raise
        data = payload.get("data", [])
        if not data:
            pytest.skip("workspace has no work item property definitions to attach")
        return str(data[0]["id"])

    def test_list_is_empty_on_a_fresh_type(self, proj: Project, work_item_type: Any) -> None:
        page = proj.work_item_types.properties.list(work_item_type.id)
        assert page.data == []

    def test_attach_then_list_then_detach(
        self,
        proj: Project,
        work_item_type: Any,
        attachable_property_id: str,
    ) -> None:
        attached = proj.work_item_types.properties.attach(
            work_item_type.id, [attachable_property_id]
        )
        assert attachable_property_id in attached.properties
        try:
            page = proj.work_item_types.properties.list(work_item_type.id)
            assert any(p.id == attachable_property_id for p in page.data)

            fetched = proj.work_item_types.properties.retrieve(
                work_item_type.id, attachable_property_id
            )
            assert fetched.id == attachable_property_id
        finally:
            proj.work_item_types.properties.detach(work_item_type.id, attachable_property_id)

        page_after = proj.work_item_types.properties.list(work_item_type.id)
        assert all(p.id != attachable_property_id for p in page_after.data)
