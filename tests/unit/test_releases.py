"""Unit tests for the Releases API resource (smoke tests with real HTTP requests)."""

from uuid import uuid4

import pytest

from plane.client import PlaneClient
from plane.errors.errors import HttpError
from plane.models.releases import (
    AddReleaseItemLabel,
    AddReleaseWorkItems,
    CreateRelease,
    CreateReleaseComment,
    CreateReleaseLabel,
    CreateReleaseLink,
    CreateReleaseTag,
    UpdateRelease,
    UpdateReleaseLabel,
    UpdateReleaseLink,
    UpdateReleaseTag,
)


def _uid() -> str:
    return uuid4().hex[:8]


class TestReleases:
    """Release CRUD."""

    @pytest.fixture
    def release(self, client: PlaneClient, workspace_slug: str):
        rel = client.releases.create(workspace_slug, CreateRelease(name=f"release-{_uid()}"))
        yield rel
        try:
            client.releases.delete(workspace_slug, rel.id)
        except Exception:
            pass

    def test_list_releases_returns_list(self, client: PlaneClient, workspace_slug: str) -> None:
        """list() returns a plain list (it used to raise on the paginated envelope)."""
        releases = client.releases.list(workspace_slug)
        assert isinstance(releases, list)

    def test_list_paginated_returns_envelope(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        response = client.releases.list_paginated(workspace_slug)
        assert hasattr(response, "results")
        assert isinstance(response.results, list)
        assert isinstance(response.total_count, int)

    def test_create_release(self, release) -> None:
        assert release.id is not None
        assert release.name is not None

    def test_retrieve_release(self, client: PlaneClient, workspace_slug: str, release) -> None:
        retrieved = client.releases.retrieve(workspace_slug, release.id)
        assert retrieved.id == release.id

    def test_update_release(self, client: PlaneClient, workspace_slug: str, release) -> None:
        new_name = f"release-{_uid()}"
        updated = client.releases.update(workspace_slug, release.id, UpdateRelease(name=new_name))
        assert updated.id == release.id
        assert updated.name == new_name

    def test_create_with_description_html(self, client: PlaneClient, workspace_slug: str) -> None:
        """The body is written via description_html, and read back as a nested object."""
        rel = client.releases.create(
            workspace_slug,
            CreateRelease(name=f"release-{_uid()}", description_html="<p>notes</p>"),
        )
        try:
            assert rel.id is not None
        finally:
            try:
                client.releases.delete(workspace_slug, rel.id)
            except Exception:
                pass

    def test_delete_release(self, client: PlaneClient, workspace_slug: str) -> None:
        rel = client.releases.create(workspace_slug, CreateRelease(name=f"release-{_uid()}"))
        client.releases.delete(workspace_slug, rel.id)
        with pytest.raises(HttpError):
            client.releases.retrieve(workspace_slug, rel.id)


class TestReleaseTags:
    """Release tags are version markers."""

    @pytest.fixture
    def tag(self, client: PlaneClient, workspace_slug: str):
        t = client.releases.tags.create(
            workspace_slug, CreateReleaseTag(version=f"v{_uid()}", commit_hash="abc123")
        )
        yield t
        try:
            client.releases.tags.delete(workspace_slug, t.id)
        except Exception:
            pass

    def test_list_tags(self, client: PlaneClient, workspace_slug: str) -> None:
        assert isinstance(client.releases.tags.list(workspace_slug), list)

    def test_create_tag_carries_version(self, tag) -> None:
        assert tag.id is not None
        assert tag.version is not None

    def test_retrieve_tag(self, client: PlaneClient, workspace_slug: str, tag) -> None:
        assert client.releases.tags.retrieve(workspace_slug, tag.id).id == tag.id

    def test_update_tag(self, client: PlaneClient, workspace_slug: str, tag) -> None:
        updated = client.releases.tags.update(
            workspace_slug, tag.id, UpdateReleaseTag(description="updated")
        )
        assert updated.id == tag.id

    def test_delete_tag(self, client: PlaneClient, workspace_slug: str) -> None:
        t = client.releases.tags.create(workspace_slug, CreateReleaseTag(version=f"v{_uid()}"))
        client.releases.tags.delete(workspace_slug, t.id)
        with pytest.raises(HttpError):
            client.releases.tags.retrieve(workspace_slug, t.id)

    def test_create_model_keeps_deprecated_fields(self) -> None:
        """name/color stay on the create model for backward compatibility."""
        fields = set(CreateReleaseTag.model_fields)
        assert {"version", "commit_hash", "git_tag"} <= fields
        assert {"name", "color"} <= fields


class TestReleaseLabels:
    """Workspace-level release labels."""

    @pytest.fixture
    def label(self, client: PlaneClient, workspace_slug: str):
        lbl = client.releases.labels.create(
            workspace_slug, CreateReleaseLabel(name=f"label-{_uid()}", color="#112233")
        )
        yield lbl
        try:
            client.releases.labels.delete(workspace_slug, lbl.id)
        except Exception:
            pass

    def test_list_labels(self, client: PlaneClient, workspace_slug: str) -> None:
        assert isinstance(client.releases.labels.list(workspace_slug), list)

    def test_create_label(self, label) -> None:
        assert label.id is not None
        assert label.name is not None

    def test_retrieve_label(self, client: PlaneClient, workspace_slug: str, label) -> None:
        assert client.releases.labels.retrieve(workspace_slug, label.id).id == label.id

    def test_update_label(self, client: PlaneClient, workspace_slug: str, label) -> None:
        updated = client.releases.labels.update(
            workspace_slug, label.id, UpdateReleaseLabel(name=f"label-{_uid()}")
        )
        assert updated.id == label.id

    def test_delete_label(self, client: PlaneClient, workspace_slug: str) -> None:
        lbl = client.releases.labels.create(
            workspace_slug, CreateReleaseLabel(name=f"label-{_uid()}")
        )
        client.releases.labels.delete(workspace_slug, lbl.id)
        with pytest.raises(HttpError):
            client.releases.labels.retrieve(workspace_slug, lbl.id)


class TestReleaseItemLabels:
    """Labels attached to a specific release."""

    @pytest.fixture
    def release(self, client: PlaneClient, workspace_slug: str):
        rel = client.releases.create(workspace_slug, CreateRelease(name=f"release-{_uid()}"))
        yield rel
        try:
            client.releases.delete(workspace_slug, rel.id)
        except Exception:
            pass

    def test_list_item_labels(self, client: PlaneClient, workspace_slug: str, release) -> None:
        assert isinstance(client.releases.item_labels.list(workspace_slug, release.id), list)

    def test_attach_and_detach_label(
        self, client: PlaneClient, workspace_slug: str, release
    ) -> None:
        label = client.releases.labels.create(
            workspace_slug, CreateReleaseLabel(name=f"label-{_uid()}")
        )
        try:
            attached = client.releases.item_labels.create(
                workspace_slug, release.id, AddReleaseItemLabel(label_ids=[label.id])
            )
            assert isinstance(attached, list)
            assert label.id in [
                x.id for x in client.releases.item_labels.list(workspace_slug, release.id)
            ]

            client.releases.item_labels.delete(workspace_slug, release.id, label.id)
            assert label.id not in [
                x.id for x in client.releases.item_labels.list(workspace_slug, release.id)
            ]
        finally:
            try:
                client.releases.labels.delete(workspace_slug, label.id)
            except Exception:
                pass


class TestReleaseWorkItems:
    """Work items linked to a release."""

    @pytest.fixture
    def release(self, client: PlaneClient, workspace_slug: str):
        rel = client.releases.create(workspace_slug, CreateRelease(name=f"release-{_uid()}"))
        yield rel
        try:
            client.releases.delete(workspace_slug, rel.id)
        except Exception:
            pass

    def test_list_work_items(self, client: PlaneClient, workspace_slug: str, release) -> None:
        assert isinstance(client.releases.work_items.list(workspace_slug, release.id), list)

    def test_add_and_remove_work_item(
        self, client: PlaneClient, workspace_slug: str, release, project
    ) -> None:
        from plane.models.work_items import CreateWorkItem

        wi = client.work_items.create(
            workspace_slug, project.id, CreateWorkItem(name=f"wi-{_uid()}")
        )
        try:
            client.releases.work_items.add(
                workspace_slug, release.id, AddReleaseWorkItems(work_item_ids=[wi.id])
            )
            assert wi.id in [
                w.id for w in client.releases.work_items.list(workspace_slug, release.id)
            ]

            client.releases.work_items.remove(workspace_slug, release.id, [wi.id])
            assert wi.id not in [
                w.id for w in client.releases.work_items.list(workspace_slug, release.id)
            ]
        finally:
            try:
                client.work_items.delete(workspace_slug, project.id, wi.id)
            except Exception:
                pass


class TestReleaseComments:
    """Comments on a release."""

    @pytest.fixture
    def release(self, client: PlaneClient, workspace_slug: str):
        rel = client.releases.create(workspace_slug, CreateRelease(name=f"release-{_uid()}"))
        yield rel
        try:
            client.releases.delete(workspace_slug, rel.id)
        except Exception:
            pass

    def test_comment_lifecycle(self, client: PlaneClient, workspace_slug: str, release) -> None:
        comment = client.releases.comments.create(
            workspace_slug, release.id, CreateReleaseComment(comment_html="<p>ship it</p>")
        )
        assert comment.id is not None

        assert comment.id in [
            c.id for c in client.releases.comments.list(workspace_slug, release.id)
        ]
        assert (
            client.releases.comments.retrieve(workspace_slug, release.id, comment.id).id
            == comment.id
        )
        client.releases.comments.delete(workspace_slug, release.id, comment.id)


class TestReleaseLinks:
    """Links on a release."""

    @pytest.fixture
    def release(self, client: PlaneClient, workspace_slug: str):
        rel = client.releases.create(workspace_slug, CreateRelease(name=f"release-{_uid()}"))
        yield rel
        try:
            client.releases.delete(workspace_slug, rel.id)
        except Exception:
            pass

    def test_link_lifecycle(self, client: PlaneClient, workspace_slug: str, release) -> None:
        link = client.releases.links.create(
            workspace_slug,
            release.id,
            CreateReleaseLink(url=f"https://example.com/{_uid()}", title="Docs"),
        )
        assert link.id is not None

        assert link.id in [x.id for x in client.releases.links.list(workspace_slug, release.id)]
        updated = client.releases.links.update(
            workspace_slug, release.id, link.id, UpdateReleaseLink(title="Updated")
        )
        assert updated.id == link.id
        client.releases.links.delete(workspace_slug, release.id, link.id)
