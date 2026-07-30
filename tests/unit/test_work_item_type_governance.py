"""Unit tests for WorkItemTypeGovernance API resource (smoke tests with real HTTP requests)."""

import warnings
from uuid import uuid4

import pytest

from plane.client import PlaneClient
from plane.models.work_item_type_governance import TypeGovernancePreviewRequest
from plane.models.work_item_types import CreateWorkItemType


@pytest.fixture(scope="module")
def governed(client: PlaneClient, workspace_slug: str) -> bool:
    """Whether the test workspace owns states and workflows (workspace governance)."""
    features = client.workspaces.get_features(workspace_slug)
    return bool(features.states_owned_by_workspace)


@pytest.fixture(scope="module")
def workspace_type(client: PlaneClient, workspace_slug: str, governed: bool):
    """A throwaway workspace-level work item type for governance reads."""
    if not governed:
        pytest.skip("workspace does not own states and workflows")
    created = client.workspace_work_item_types.create(
        workspace_slug, CreateWorkItemType(name=f"test-gov-type-{uuid4().hex[:8]}")
    )
    yield created
    try:
        client.workspace_work_item_types.delete(workspace_slug, created.id)
    except Exception as exc:
        warnings.warn(f"Teardown failed for work item type {created.id}: {exc}", stacklevel=1)


class TestWorkItemTypeGovernance:
    """Test WorkItemTypeGovernance API resource."""

    def test_retrieve_governance_defaults(
        self, client: PlaneClient, workspace_slug: str, workspace_type
    ) -> None:
        """A fresh type starts in mode 'any' with an empty allowlist."""
        governance = client.work_item_type_governance.retrieve(workspace_slug, workspace_type.id)
        assert governance.mode == "any"
        assert governance.allowlist == []

    def test_preview_mode_any_is_empty(
        self, client: PlaneClient, workspace_slug: str, workspace_type
    ) -> None:
        """Previewing mode 'any' is a no-op impact report."""
        preview = client.work_item_type_governance.preview(
            workspace_slug, workspace_type.id, TypeGovernancePreviewRequest(mode="any")
        )
        assert preview.total == 0

    def test_list_pins_empty(
        self, client: PlaneClient, workspace_slug: str, workspace_type
    ) -> None:
        """A fresh type has no pins."""
        pins = client.work_item_type_governance.pins.list(workspace_slug, workspace_type.id)
        assert pins == []

    def test_project_type_workflows(
        self, client: PlaneClient, workspace_slug: str, governed: bool, project
    ) -> None:
        """The project-side view lists an entry per active type."""
        if not governed:
            pytest.skip("workspace does not own states and workflows")
        entries = client.work_item_type_governance.project_workflows.list(
            workspace_slug, project.id
        )
        assert isinstance(entries, list)
        for entry in entries:
            assert entry.type_id is not None
            assert entry.governance in ("any", "constrained", "required", "pinned")
