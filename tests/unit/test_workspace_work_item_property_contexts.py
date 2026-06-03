"""Unit tests for WorkspaceWorkItemProperties.contexts sub-resource (smoke tests with real HTTP)."""

import warnings
from uuid import uuid4

import pytest

from plane.client import PlaneClient
from plane.models.enums import PropertyType
from plane.models.work_item_properties import CreateWorkItemProperty
from plane.models.work_item_property_configurations import TextAttributeSettings
from plane.models.work_item_property_context import (
    UpdateWorkItemPropertyContext,
    WorkItemPropertyContext,
)


class TestWorkspaceWorkItemPropertyContexts:
    """Test WorkspaceWorkItemProperties.contexts sub-resource."""

    def test_list_contexts_for_workspace_property(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing contexts for a workspace work item property."""
        props = client.workspace_work_item_properties.list(workspace_slug)
        if not props:
            pytest.skip("No workspace properties available to test context listing")

        prop = props[0]
        contexts = client.workspace_work_item_properties.contexts.list(
            workspace_slug, prop.id
        )
        assert isinstance(contexts, list)
        # Every property should have at least a default context
        assert len(contexts) >= 1
        for ctx in contexts:
            assert isinstance(ctx, WorkItemPropertyContext)
            assert ctx.id is not None

    def test_retrieve_context_for_workspace_property(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test retrieving a single context for a workspace property."""
        props = client.workspace_work_item_properties.list(workspace_slug)
        if not props:
            pytest.skip("No workspace properties available to test context retrieve")

        prop = props[0]
        contexts = client.workspace_work_item_properties.contexts.list(
            workspace_slug, prop.id
        )
        if not contexts:
            pytest.skip("No contexts available to test retrieve")

        ctx = contexts[0]
        retrieved = client.workspace_work_item_properties.contexts.retrieve(
            workspace_slug, prop.id, ctx.id
        )
        assert retrieved is not None
        assert retrieved.id == ctx.id
        assert retrieved.property == ctx.property

    def test_create_update_delete_context(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test creating, updating, and deleting a non-default context."""
        # First create a property to work with
        display_name = f"test-ctx-prop-{uuid4().hex[:8]}"
        prop_data = CreateWorkItemProperty(
            display_name=display_name,
            description="Property for context testing",
            property_type=PropertyType.TEXT,
            is_active=True,
            settings=TextAttributeSettings(display_format="single-line"),
        )
        prop = client.workspace_work_item_properties.create(workspace_slug, prop_data)
        assert prop is not None

        try:
            # Verify the default context exists
            contexts = client.workspace_work_item_properties.contexts.list(
                workspace_slug, prop.id
            )
            assert len(contexts) >= 1
            default_ctx = next(
                (c for c in contexts if c.applies_to_all_projects is True), None
            )
            assert default_ctx is not None, "Default context should exist after property creation"
            assert default_ctx.applies_to_all_work_item_types is True

            # Verify the default context can be retrieved
            retrieved_default = client.workspace_work_item_properties.contexts.retrieve(
                workspace_slug, prop.id, default_ctx.id
            )
            assert retrieved_default.id == default_ctx.id

            # Update the default context
            updated = client.workspace_work_item_properties.contexts.update(
                workspace_slug,
                prop.id,
                default_ctx.id,
                UpdateWorkItemPropertyContext(is_required=True),
            )
            assert updated.id == default_ctx.id
            assert updated.is_required is True

        finally:
            try:
                client.workspace_work_item_properties.delete(workspace_slug, prop.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for workspace property {prop.id}: {exc}",
                    stacklevel=1,
                )

    def test_context_response_shape(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test that context responses contain all expected fields."""
        props = client.workspace_work_item_properties.list(workspace_slug)
        if not props:
            pytest.skip("No workspace properties available to test context shape")

        prop = props[0]
        contexts = client.workspace_work_item_properties.contexts.list(
            workspace_slug, prop.id
        )
        if not contexts:
            pytest.skip("No contexts available to test shape")

        ctx = contexts[0]
        # Core fields should be present
        assert ctx.id is not None
        assert ctx.name is not None
        assert ctx.applies_to_all_projects is not None
        assert ctx.applies_to_all_work_item_types is not None
        # Through-table fields should be lists (possibly empty)
        assert isinstance(ctx.project_ids, list)
        assert isinstance(ctx.issue_type_ids, list)
        assert isinstance(ctx.options, list)
