"""Unit tests for WorkspaceStates API resource (smoke tests with real HTTP requests)."""

import warnings
from uuid import uuid4

import pytest

from plane.client import PlaneClient
from plane.errors.errors import HttpError
from plane.models.states import CreateWorkspaceState, UpdateWorkspaceState


@pytest.fixture(scope="module")
def governed(client: PlaneClient, workspace_slug: str) -> bool:
    """Whether the test workspace owns states and workflows (workspace governance)."""
    features = client.workspaces.get_features(workspace_slug)
    return bool(features.states_owned_by_workspace)


class TestWorkspaceStates:
    """Test WorkspaceStates API resource."""

    def test_list_workspace_states(self, client: PlaneClient, workspace_slug: str) -> None:
        """The list endpoint is dual-mode and must work in every workspace."""
        response = client.workspace_states.list(workspace_slug)
        assert isinstance(response.results, list)
        for state in response.results:
            assert state.id is not None
            assert state.name

    def test_features_report_governance_flag(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """states_owned_by_workspace must be present and typed on the features payload."""
        features = client.workspaces.get_features(workspace_slug)
        assert features.states_owned_by_workspace in (True, False)

    def test_create_rejected_when_ungoverned(
        self, client: PlaneClient, workspace_slug: str, governed: bool
    ) -> None:
        """Catalog writes must respond 400 workspace_not_managed in ungoverned workspaces."""
        if governed:
            pytest.skip("workspace is governed; the ungoverned rejection does not apply")
        data = CreateWorkspaceState(
            name=f"test-ws-state-{uuid4().hex[:8]}", color="#FF0000", group="unstarted"
        )
        with pytest.raises(HttpError) as exc_info:
            client.workspace_states.create(workspace_slug, data)
        assert exc_info.value.status_code == 400

    def test_create_update_delete_workspace_state(
        self, client: PlaneClient, workspace_slug: str, governed: bool
    ) -> None:
        """Full CRUD cycle against the workspace states catalog (governed only)."""
        if not governed:
            pytest.skip("workspace does not own states and workflows")

        name = f"test-ws-state-{uuid4().hex[:8]}"
        created = client.workspace_states.create(
            workspace_slug,
            CreateWorkspaceState(
                name=name, color="#FF0000", group="unstarted", description="SDK test state"
            ),
        )
        try:
            assert created.id is not None
            assert created.name == name
            assert created.project is None

            retrieved = client.workspace_states.retrieve(workspace_slug, created.id)
            assert retrieved.id == created.id

            updated = client.workspace_states.update(
                workspace_slug,
                created.id,
                UpdateWorkspaceState(description="Updated description"),
            )
            assert updated.id == created.id
            assert updated.description == "Updated description"
        finally:
            try:
                client.workspace_states.delete(workspace_slug, created.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for workspace state {created.id}: {exc}", stacklevel=1
                )
