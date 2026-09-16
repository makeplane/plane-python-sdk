"""`project.work_items` against a real server: CRUD, `?fields=`/`?expand=`, archive,
upsert, bulk ops, pagination, errors. Workspace-wide listing and
`retrieve_by_identifier` live in their own file.

Loaded-row navigation off the session `project`, except the uuid-vs-key parity check,
which has to put two spellings in the same path slot and so takes the flat path."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import FieldNotRequested, LoadedProject, PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.common import OffsetPage
from plane.models.v2.work_items import CreateWorkItem, UpdateWorkItem

from ._guard import skip_absent_capability
from .helpers import unique_name

MISSING_ID = "00000000-0000-0000-0000-000000000000"


@pytest.fixture
def work_item(project: LoadedProject) -> Iterator[Any]:
    """One freshly created work item, deleted afterwards."""
    created = project.work_items.create(CreateWorkItem(name=unique_name("wi")))
    yield created
    try:
        project.work_items.delete(created.id)
    except Exception:
        pass


class TestCRUD:
    def test_create_returns_the_written_fields(self, project: LoadedProject) -> None:
        name = unique_name("wi-create")
        created = project.work_items.create(CreateWorkItem(name=name))
        try:
            assert created.name == name
            assert created.id
            assert created.identifier  # the server-assigned human key, e.g. "ENG-12"
        finally:
            project.work_items.delete(created.id)

    def test_retrieve_returns_the_created_row(self, project: LoadedProject, work_item: Any) -> None:
        fetched = project.work_items.retrieve(work_item.id)
        assert fetched.id == work_item.id
        assert fetched.name == work_item.name

    def test_list_by_project_uuid_and_key_agree(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        work_item: Any,
    ) -> None:
        work_items = client.v2.workspaces.projects.work_items
        by_id = {row.id for row in work_items.list(workspace_slug, project_id).data}
        by_key = {row.id for row in work_items.list(workspace_slug, project_key).data}
        assert work_item.id in by_id
        assert by_id == by_key

    def test_patch_updates_only_the_given_fields(
        self, project: LoadedProject, work_item: Any
    ) -> None:
        new_name = unique_name("wi-renamed")
        updated = project.work_items.update(work_item.id, UpdateWorkItem(name=new_name))
        assert updated.id == work_item.id
        assert updated.name == new_name

    def test_delete_then_retrieve_404s(self, project: LoadedProject) -> None:
        created = project.work_items.create(CreateWorkItem(name=unique_name("wi-del")))
        project.work_items.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project.work_items.retrieve(created.id)
        assert exc_info.value.status == 404


class TestFieldsAndExpand:
    def test_fields_returns_a_sparse_row(self, project: LoadedProject, work_item: Any) -> None:
        """Only `id` and `name` come back. `priority` has a real server-side default,
        so reading it as `None` would look like data -- the loaded row raises instead
        and names what the server returned."""
        fetched = project.work_items.retrieve(work_item.id, fields=["id", "name"])
        assert fetched.id == work_item.id
        assert fetched.name == work_item.name
        with pytest.raises(FieldNotRequested) as exc_info:
            _ = fetched.priority
        assert "LoadedWorkItem.priority" in str(exc_info.value)
        assert "['id', 'name']" in str(exc_info.value)

    def test_expand_state_adds_the_embedded_object(
        self, project: LoadedProject, work_item: Any
    ) -> None:
        plain = project.work_items.retrieve(work_item.id)
        expanded = project.work_items.retrieve(work_item.id, expand=["state"])
        # `state` is not a declared field on `WorkItem` -- it only shows up (via
        # `extra="allow"`) when `?expand=state` actually asked the server for it.
        assert plain.model_extra is not None and expanded.model_extra is not None
        assert "state" not in plain.model_extra
        assert "state" in expanded.model_extra

    def test_invalid_expand_is_rejected_client_side(self, project: LoadedProject) -> None:
        with pytest.raises(ValueError, match="bogus"):
            project.work_items.list(expand=["bogus"])


class TestArchive:
    def test_archive_then_unarchive_round_trips(self, project: LoadedProject) -> None:
        # Only work items in a completed/cancelled state can be archived
        # (server-enforced) -- find a real one rather than assuming a name.
        states = project.states.list(per_page=100).data
        eligible = next((s for s in states if s.group in ("completed", "cancelled")), None)
        if eligible is None:
            skip_absent_capability("project has no completed/cancelled-group state to archive into")

        created = project.work_items.create(
            CreateWorkItem(name=unique_name("wi-archive"), state_id=eligible.id),
        )
        try:
            archived = project.work_items.archive(created.id)
            assert archived.archived_at is not None

            unarchived = project.work_items.unarchive(created.id)
            assert unarchived.archived_at is None
        finally:
            project.work_items.delete(created.id)


class TestUpsert:
    def test_upsert_creates_then_reconciles(self, project: LoadedProject) -> None:
        marker = unique_name("wi-upsert")
        first = project.work_items.upsert(
            CreateWorkItem(name=marker, external_source=marker, external_id="1"),
        )
        try:
            renamed = f"{marker}-renamed"
            second = project.work_items.upsert(
                CreateWorkItem(name=renamed, external_source=marker, external_id="1"),
            )
            assert second.id == first.id, "same (external_source, external_id) must reconcile"
            assert second.name == renamed

            page = project.work_items.list(external_source=marker, external_id="1")
            assert len(page.data) == 1, "reconcile must not leave a duplicate row behind"
        finally:
            project.work_items.delete(first.id)


class TestBulk:
    def test_bulk_create_update_delete_round_trip(self, project: LoadedProject) -> None:
        items = [CreateWorkItem(name=unique_name("wi-bulk")) for _ in range(2)]
        created = project.work_items.bulk_create(items)
        created.raise_for_failures()
        ids = [row.id for row in created.results if row.result != "failed"]
        try:
            updated = project.work_items.bulk_update(
                [{"id": pk, "name": unique_name("wi-bulk-renamed")} for pk in ids],
            )
            assert updated.succeeded == 2
            assert updated.failed == 0
        finally:
            deleted = project.work_items.bulk_delete(ids)
            assert deleted.succeeded == 2


class TestErrors:
    def test_retrieve_missing_id_surfaces_404(self, project: LoadedProject) -> None:
        with pytest.raises(PlaneAPIError) as exc_info:
            project.work_items.retrieve(MISSING_ID)
        error = exc_info.value
        assert error.status == 404
        assert error.code == "not_found"

    def test_missing_required_name_surfaces_a_field_error(self, project: LoadedProject) -> None:
        """`model_construct()` builds the DTO without validating it, so the empty body
        the server has to reject actually reaches it -- through `create`, not a
        hand-rolled `transport.request`, so the resource's own request path is what is
        under test. `CreateWorkItem(name=...)` cannot express this case: pydantic
        rejects it first, and the point is the *server's* field-error contract."""
        with pytest.raises(PlaneAPIError) as exc_info:
            project.work_items.create(CreateWorkItem.model_construct())
        error = exc_info.value
        assert error.status == 400
        assert error.errors is not None
        assert any(field_error.field == "name" for field_error in error.errors)


class TestPagination:
    def test_iter_follows_every_page(self, project: LoadedProject) -> None:
        marker = unique_name("wi-pg")
        items = [
            CreateWorkItem(
                name=unique_name("wi-pg-row"), external_source=marker, external_id=str(i)
            )
            for i in range(4)
        ]
        created = project.work_items.bulk_create(items)
        created.raise_for_failures()
        ids = [row.id for row in created.results if row.result != "failed"]
        try:
            page = project.work_items.list(external_source=marker, per_page=2)
            assert isinstance(page, OffsetPage), "no `paginate=`, so this is the offset envelope"
            assert len(page.data) == 2
            assert page.next is not None

            rows = list(project.work_items.iterate(external_source=marker, per_page=2))
            assert {row.id for row in rows} == set(ids)
        finally:
            project.work_items.bulk_delete(ids)
