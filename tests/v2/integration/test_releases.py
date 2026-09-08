"""`client.v2.workspace(slug).releases` and its sub-resources against a real
server; gated by the `RELEASES` flag plus `is_release_enabled`, so fixtures
skip (never fail) the module when that gate is closed. No upsert/bulk-* here."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedWorkspace, PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.releases import (
    CreateRelease,
    CreateReleaseComment,
    CreateReleaseLabel,
    CreateReleaseLink,
    CreateReleaseTag,
    UpdateRelease,
    UpdateReleaseChangelog,
    UpdateReleaseComment,
    UpdateReleaseLabel,
    UpdateReleaseLink,
    UpdateReleaseTag,
)

from .helpers import unique_name


def _create_release_or_skip(workspace: LoadedWorkspace, name: str) -> Any:
    try:
        return workspace.releases.create(CreateRelease(name=name))
    except PlaneAPIError as exc:
        if exc.status == 402:
            pytest.skip("RELEASES not enabled on this workspace")
        raise


@pytest.fixture
def release(workspace: LoadedWorkspace) -> Iterator[Any]:
    """One freshly created release, deleted afterwards."""
    created = _create_release_or_skip(releases, unique_name("release"))
    yield created
    try:
        workspace.releases.delete(created.id)
    except Exception:
        pass


class TestCRUD:
    def test_create_returns_the_written_fields(self, workspace: LoadedWorkspace) -> None:
        name = unique_name("release")
        created = _create_release_or_skip(releases, name)
        try:
            assert created.name == name
            assert created.id
            assert created.status is not None
        finally:
            workspace.releases.delete(created.id)

    def test_retrieve_returns_the_created_row(self, workspace: LoadedWorkspace, release: Any) -> None:
        fetched = workspace.releases.retrieve(release.id)
        assert fetched.id == release.id
        assert fetched.name == release.name

    def test_retrieve_with_fields_is_sparse(self, workspace: LoadedWorkspace, release: Any) -> None:
        fetched = workspace.releases.retrieve(release.id, fields=["id", "name"])
        assert fetched.id == release.id
        assert fetched.status is None

    def test_retrieve_with_expand(self, workspace: LoadedWorkspace, release: Any) -> None:
        # No lead/tag set on this row, so the expand keys are simply absent/None --
        # this only proves the server accepted the enum, not that it populated it.
        fetched = workspace.releases.retrieve(release.id, expand=["lead", "tag"])
        assert fetched.id == release.id

    def test_list_finds_the_created_row(self, workspace: LoadedWorkspace, release: Any) -> None:
        page = workspace.releases.list(name=release.name)
        assert any(row.id == release.id for row in page.data)

    def test_find_by_name(self, workspace: LoadedWorkspace, release: Any) -> None:
        found = workspace.releases.find_by_name(release.name)
        assert found.id == release.id

    def test_patch_updates_only_the_given_fields(self, workspace: LoadedWorkspace, release: Any) -> None:
        new_name = unique_name("release-renamed")
        updated = workspace.releases.update(release.id, UpdateRelease(name=new_name))
        assert updated.id == release.id
        assert updated.name == new_name

    def test_delete_then_retrieve_404s(self, workspace: LoadedWorkspace) -> None:
        created = _create_release_or_skip(releases, unique_name("release"))
        workspace.releases.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            workspace.releases.retrieve(created.id)
        assert exc_info.value.status == 404


class TestErrors:
    MISSING_ID = "00000000-0000-0000-0000-000000000000"

    def test_retrieve_missing_id_surfaces_404(self, workspace: LoadedWorkspace) -> None:
        with pytest.raises(PlaneAPIError) as exc_info:
            workspace.releases.retrieve(self.MISSING_ID)
        error = exc_info.value
        assert error.status == 404
        assert error.code == "not_found"

    def test_over_length_name_surfaces_field_errors(self, workspace: LoadedWorkspace) -> None:
        too_long = unique_name("release") + ("x" * 300)
        with pytest.raises(PlaneAPIError) as exc_info:
            workspace.releases.create(CreateRelease(name=too_long))
        error = exc_info.value
        if error.status == 402:
            pytest.skip("RELEASES not enabled on this workspace")
        assert error.status == 400
        assert error.errors is not None
        assert any(field_error.field == "name" for field_error in error.errors)


class TestPagination:
    ROW_COUNT = 4
    PER_PAGE = 2

    @pytest.fixture
    def seeded(self, workspace: LoadedWorkspace) -> Iterator[tuple[str, list[str]]]:
        # `releases_list` has no `external_source`/`external_id` filter (unlike
        # states/labels) -- `search` is the only free-text filter it exposes, so
        # the marker is embedded in the name and matched via `?search=`.
        marker = unique_name("release-pg")
        ids = []
        for _ in range(self.ROW_COUNT):
            row = _create_release_or_skip(releases, f"{marker}-{unique_name('row')}")
            ids.append(row.id)
        yield marker, ids
        for pk in ids:
            try:
                workspace.releases.delete(pk)
            except Exception:
                pass

    def test_offset_list_reports_a_next_offset(
        self, workspace: LoadedWorkspace, seeded: tuple[str, list[str]]
    ) -> None:
        marker, _ids = seeded
        page = workspace.releases.list(search=marker, per_page=self.PER_PAGE)
        assert len(page.data) == self.PER_PAGE
        assert page.next is not None
        assert page.total_count == self.ROW_COUNT

    def test_offset_iterate_follows_every_page(
        self, workspace: LoadedWorkspace, seeded: tuple[str, list[str]]
    ) -> None:
        marker, ids = seeded
        rows = list(workspace.releases.iterate(search=marker, per_page=self.PER_PAGE))
        assert {row.id for row in rows} == set(ids)

    def test_cursor_list_uses_the_cursor_envelope(
        self, workspace: LoadedWorkspace, seeded: tuple[str, list[str]]
    ) -> None:
        marker, _ids = seeded
        page = workspace.releases.list(
            search=marker,
            per_page=self.PER_PAGE,
            paginate="cursor",
            order_by="created_at",
        )
        assert len(page.data) == self.PER_PAGE
        assert page.has_more is True
        assert page.next_cursor is not None


class TestLabelsAndWorkItemsBridges:
    def test_labels_add_then_remove(self, workspace: LoadedWorkspace, release: Any) -> None:
        label = workspace.releases.labels.create(CreateReleaseLabel(name=unique_name("rel-label")))
        try:
            added = workspace.releases.labels.add(release.id, [label.id])
            assert label.id in added

            fetched = workspace.releases.retrieve(release.id)
            assert fetched.label_ids is not None
            assert label.id in fetched.label_ids

            removed = workspace.releases.labels.remove(release.id, [label.id])
            assert label.id in removed
        finally:
            workspace.releases.labels.delete(label.id)

    def test_work_items_add_then_remove(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        workspace: LoadedWorkspace,
        release: Any,
    ) -> None:
        from plane.models.v2.work_items import CreateWorkItem

        work_items = client.v2.workspace(workspace_slug).project(project_id).work_items
        work_item = work_items.create(CreateWorkItem(name=unique_name("release-wi")))
        try:
            added = workspace.releases.work_items.add(release.id, [work_item.id])
            assert work_item.id in added

            removed = workspace.releases.work_items.remove(release.id, [work_item.id])
            assert work_item.id in removed
        finally:
            work_items.delete(work_item.id)


class TestChangelog:
    def test_get_then_update(self, workspace: LoadedWorkspace, release: Any) -> None:
        changelog = workspace.releases.changelog.retrieve(release.id)
        assert changelog.release_id == release.id

        updated = workspace.releases.changelog.update(
            release.id, UpdateReleaseChangelog(description_html="<p>notes</p>")
        )
        assert updated.description_html == "<p>notes</p>"


class TestComments:
    def test_crud(self, workspace: LoadedWorkspace, release: Any) -> None:
        created = workspace.releases.comments.create(
            release.id, CreateReleaseComment(comment_html="<p>hi</p>")
        )
        try:
            assert created.release_id == release.id

            fetched = workspace.releases.comments.retrieve(release.id, created.id)
            assert fetched.id == created.id

            page = workspace.releases.comments.list(release.id)
            assert any(c.id == created.id for c in page.data)

            updated = workspace.releases.comments.update(
                release.id, created.id, UpdateReleaseComment(comment_html="<p>bye</p>")
            )
            assert updated.comment_html == "<p>bye</p>"
        finally:
            workspace.releases.comments.delete(release.id, created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            workspace.releases.comments.retrieve(release.id, created.id)
        assert exc_info.value.status == 404


class TestLinks:
    def test_crud(self, workspace: LoadedWorkspace, release: Any) -> None:
        created = workspace.releases.links.create(
            release.id, CreateReleaseLink(title="Docs", url="https://example.com/a")
        )
        try:
            assert created.url == "https://example.com/a"

            updated = workspace.releases.links.update(
                release.id, created.id, UpdateReleaseLink(url="https://example.com/b")
            )
            assert updated.url == "https://example.com/b"

            page = workspace.releases.links.list(release.id)
            assert any(link.id == created.id for link in page.data)
        finally:
            workspace.releases.links.delete(release.id, created.id)


class TestLabelsCatalog:
    def test_crud_and_find_by_name(self, workspace: LoadedWorkspace) -> None:
        name = unique_name("rel-label")
        created = workspace.releases.labels.create(CreateReleaseLabel(name=name))
        try:
            assert created.name == name

            fetched = workspace.releases.labels.retrieve(created.id)
            assert fetched.id == created.id

            found = workspace.releases.labels.find_by_name(name)
            assert found.id == created.id

            new_name = unique_name("rel-label-renamed")
            updated = workspace.releases.labels.update(created.id, UpdateReleaseLabel(name=new_name))
            assert updated.name == new_name
        finally:
            workspace.releases.labels.delete(created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            workspace.releases.labels.retrieve(created.id)
        assert exc_info.value.status == 404


class TestTagsCatalog:
    def test_crud_find_by_version_and_prefixed_lookup(self, workspace: LoadedWorkspace) -> None:
        version = f"0.0.0-{unique_name('rel-tag')}"
        created = workspace.releases.tags.create(CreateReleaseTag(version=version))
        try:
            assert created.version == version

            by_uuid = workspace.releases.tags.retrieve(created.id)
            assert by_uuid.id == created.id

            # NOT `retrieve(f"version:{version}")`: the golden implies a
            # `version:`-prefixed lookup but it 404s live (no custom `get_object`);
            # `find_by_version` is the real way to resolve a version to an id.
            found = workspace.releases.tags.find_by_version(version)
            assert found.id == created.id

            updated = workspace.releases.tags.update(
                created.id, UpdateReleaseTag(description="release notes")
            )
            assert updated.description == "release notes"
        finally:
            workspace.releases.tags.delete(created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            workspace.releases.tags.retrieve(created.id)
        assert exc_info.value.status == 404
