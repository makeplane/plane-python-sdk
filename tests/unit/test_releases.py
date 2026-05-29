"""Unit tests for Releases API resource (smoke tests with real HTTP requests)."""

from uuid import uuid4

import pytest

from plane.client import PlaneClient
from plane.models.releases import (
    AddReleaseItemLabel,
    CreateRelease,
    CreateReleaseLabel,
    CreateReleaseTag,
    UpdateRelease,
)


class TestReleases:
    """Test Releases API resource."""

    def test_list_releases(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing releases."""
        releases = client.releases.list(workspace_slug)
        assert isinstance(releases, list)

    def test_create_update_release(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test creating and updating a release."""
        name = f"test-release-{uuid4().hex[:8]}"
        data = CreateRelease(name=name, description="Test release", status="unreleased")
        created = client.releases.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name

        updated = client.releases.update(
            workspace_slug,
            created.id,
            UpdateRelease(description="Updated release description"),
        )
        assert updated.id == created.id
        assert updated.description == "Updated release description"


class TestReleaseTags:
    """Test Releases.tags sub-resource."""

    def test_list_release_tags(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing release tags."""
        tags = client.releases.tags.list(workspace_slug)
        assert isinstance(tags, list)

    def test_create_release_tag(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test creating a release tag."""
        name = f"tag-{uuid4().hex[:6]}"
        data = CreateReleaseTag(name=name, color="#AABBCC")
        created = client.releases.tags.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name


class TestReleaseLabels:
    """Test Releases.labels sub-resource."""

    def test_list_release_labels(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing release labels."""
        labels = client.releases.labels.list(workspace_slug)
        assert isinstance(labels, list)

    def test_create_release_label(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test creating a release label."""
        name = f"label-{uuid4().hex[:6]}"
        data = CreateReleaseLabel(name=name, color="#112233")
        created = client.releases.labels.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name


class TestReleaseItemLabels:
    """Test Releases.item_labels sub-resource."""

    def test_list_item_labels_for_release(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing labels for a specific release."""
        releases = client.releases.list(workspace_slug)
        if not releases:
            pytest.skip("No releases available to test item labels listing")

        release = releases[0]
        assert release.id is not None
        labels = client.releases.item_labels.list(workspace_slug, release.id)
        assert isinstance(labels, list)

    def test_add_remove_label_to_release(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test adding and removing labels from a release."""
        # Create a release
        release_name = f"test-release-{uuid4().hex[:8]}"
        release = client.releases.create(
            workspace_slug, CreateRelease(name=release_name)
        )
        assert release is not None
        assert release.id is not None

        # Create a label
        label_name = f"label-{uuid4().hex[:6]}"
        label = client.releases.labels.create(
            workspace_slug, CreateReleaseLabel(name=label_name)
        )
        assert label is not None
        assert label.id is not None

        # Add label to release
        add_data = AddReleaseItemLabel(label_ids=[label.id])
        result = client.releases.item_labels.create(workspace_slug, release.id, add_data)
        assert isinstance(result, list)

        # Remove label from release
        client.releases.item_labels.delete(workspace_slug, release.id, label.id)
