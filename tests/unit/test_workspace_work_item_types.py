"""Unit tests for WorkspaceWorkItemTypes API resource (smoke tests with real HTTP requests)."""

from uuid import uuid4

import pytest

from plane.client import PlaneClient
from plane.models.work_item_types import (
    CreateWorkItemType,
    UpdateWorkItemType,
    WorkspaceWorkItemTypePropertyLink,
)


class TestWorkspaceWorkItemTypes:
    """Test WorkspaceWorkItemTypes API resource."""

    def test_list_workspace_work_item_types(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing workspace-level work item types."""
        types = client.workspace_work_item_types.list(workspace_slug)
        assert isinstance(types, list)

    def test_create_update_workspace_work_item_type(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test creating and updating a workspace-level work item type."""
        name = f"test-wit-{uuid4().hex[:8]}"
        data = CreateWorkItemType(name=name, description="Test workspace WIT", is_active=True)
        created = client.workspace_work_item_types.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name

        updated = client.workspace_work_item_types.update(
            workspace_slug,
            created.id,
            UpdateWorkItemType(description="Updated description"),
        )
        assert updated.id == created.id
        assert updated.description == "Updated description"
        # No delete endpoint on workspace WITs per spec.


class TestWorkspaceWorkItemTypeProperties:
    """Test WorkspaceWorkItemTypes.properties sub-resource."""

    def test_list_properties_for_workspace_wit(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing properties for a workspace work item type."""
        types = client.workspace_work_item_types.list(workspace_slug)
        if not types:
            pytest.skip("No workspace work item types available to test properties listing")

        wit = types[0]
        assert wit.id is not None, f"Expected work item type to have an id, got: {wit}"
        props = client.workspace_work_item_types.properties.list(workspace_slug, wit.id)
        assert isinstance(props, list)

    def test_create_delete_property_link(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test linking and unlinking a property on a workspace work item type."""
        types = client.workspace_work_item_types.list(workspace_slug)
        if not types:
            pytest.skip("No workspace work item types available to test property link/unlink")

        props = client.workspace_work_item_properties.list(workspace_slug)
        if not props:
            pytest.skip("No workspace work item properties available to link")

        wit = types[0]
        assert wit.id is not None

        prop = props[0]
        assert prop.id is not None

        data = WorkspaceWorkItemTypePropertyLink(property_id=prop.id)
        linked = client.workspace_work_item_types.properties.create(
            workspace_slug, wit.id, data
        )
        assert linked is not None

        current = client.workspace_work_item_types.properties.list(workspace_slug, wit.id)
        linked_ids = [p.id for p in current]
        assert prop.id in linked_ids

        client.workspace_work_item_types.properties.delete(workspace_slug, wit.id, prop.id)
