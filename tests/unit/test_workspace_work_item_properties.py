"""Unit tests for WorkspaceWorkItemProperties API resource (smoke tests with real HTTP requests)."""

import warnings
from uuid import uuid4

import pytest

from plane.client import PlaneClient
from plane.models.enums import PropertyType
from plane.models.work_item_properties import (
    CreateWorkItemProperty,
    CreateWorkItemPropertyOption,
    UpdateWorkItemProperty,
    UpdateWorkItemPropertyOption,
)
from plane.models.work_item_property_configurations import TextAttributeSettings


class TestWorkspaceWorkItemProperties:
    """Test WorkspaceWorkItemProperties API resource."""

    def test_list_workspace_work_item_properties(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing workspace-level work item properties."""
        props = client.workspace_work_item_properties.list(workspace_slug)
        assert isinstance(props, list)

    def test_retrieve_workspace_work_item_property(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test retrieving a single workspace work item property by ID."""
        props = client.workspace_work_item_properties.list(workspace_slug)
        if not props:
            pytest.skip("No workspace properties available to test retrieve")

        prop = props[0]
        retrieved = client.workspace_work_item_properties.retrieve(workspace_slug, prop.id)
        assert retrieved is not None
        assert retrieved.id == prop.id

    def test_create_update_delete_workspace_property(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test creating, updating, and deleting a workspace work item property."""
        display_name = f"test-prop-{uuid4().hex[:8]}"
        data = CreateWorkItemProperty(
            display_name=display_name,
            description="Test workspace property",
            property_type=PropertyType.TEXT,
            is_active=True,
            settings=TextAttributeSettings(display_format="multi-line"),
        )
        created = client.workspace_work_item_properties.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.display_name == display_name

        try:
            updated = client.workspace_work_item_properties.update(
                workspace_slug,
                created.id,
                UpdateWorkItemProperty(description="Updated description"),
            )
            assert updated.id == created.id
            assert updated.description == "Updated description"
        finally:
            try:
                client.workspace_work_item_properties.delete(workspace_slug, created.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for workspace property {created.id}: {exc}", stacklevel=1
                )


class TestWorkspaceWorkItemPropertyOptions:
    """Test WorkspaceWorkItemProperties.options sub-resource."""

    def test_list_options_for_workspace_property(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing options for a workspace work item property."""
        props = client.workspace_work_item_properties.list(workspace_slug)
        option_props = [
            p for p in props if getattr(p, "property_type", None) == PropertyType.OPTION
        ]
        if not option_props:
            pytest.skip("No OPTION-type workspace properties available to test options listing")

        prop = option_props[0]
        options = client.workspace_work_item_properties.options.list(workspace_slug, prop.id)
        assert isinstance(options, list)

    def test_create_update_option_for_workspace_property(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test creating and updating an option for a workspace work item property."""
        display_name = f"test-opt-prop-{uuid4().hex[:8]}"
        prop_data = CreateWorkItemProperty(
            display_name=display_name,
            description="Test option property",
            property_type=PropertyType.OPTION,
            is_active=True,
        )
        prop = client.workspace_work_item_properties.create(workspace_slug, prop_data)
        assert prop is not None

        try:
            option_name = f"opt-{uuid4().hex[:6]}"
            opt = client.workspace_work_item_properties.options.create(
                workspace_slug,
                prop.id,
                CreateWorkItemPropertyOption(name=option_name),
            )
            assert opt is not None
            assert opt.id is not None
            assert opt.name == option_name

            updated_opt = client.workspace_work_item_properties.options.update(
                workspace_slug,
                prop.id,
                opt.id,
                UpdateWorkItemPropertyOption(name=f"{option_name}-updated"),
            )
            assert updated_opt.id == opt.id
            assert updated_opt.name == f"{option_name}-updated"
        finally:
            try:
                client.workspace_work_item_properties.delete(workspace_slug, prop.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for workspace property {prop.id}: {exc}",
                    stacklevel=1,
                )

    def test_retrieve_and_delete_option_for_workspace_property(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test retrieve and delete on a workspace property option."""
        display_name = f"test-del-opt-prop-{uuid4().hex[:8]}"
        prop_data = CreateWorkItemProperty(
            display_name=display_name,
            description="Test option property for retrieve/delete",
            property_type=PropertyType.OPTION,
            is_active=True,
        )
        prop = client.workspace_work_item_properties.create(workspace_slug, prop_data)
        assert prop is not None

        try:
            opt = client.workspace_work_item_properties.options.create(
                workspace_slug,
                prop.id,
                CreateWorkItemPropertyOption(name=f"opt-{uuid4().hex[:6]}"),
            )
            assert opt is not None
            assert opt.id is not None

            retrieved = client.workspace_work_item_properties.options.retrieve(
                workspace_slug, prop.id, opt.id
            )
            assert retrieved.id == opt.id
            assert retrieved.name == opt.name

            client.workspace_work_item_properties.options.delete(
                workspace_slug, prop.id, opt.id
            )
            remaining = client.workspace_work_item_properties.options.list(
                workspace_slug, prop.id
            )
            assert all(o.id != opt.id for o in remaining)
        finally:
            try:
                client.workspace_work_item_properties.delete(workspace_slug, prop.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for workspace property {prop.id}: {exc}",
                    stacklevel=1,
                )
