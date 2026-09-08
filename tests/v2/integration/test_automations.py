"""Live coverage for `project.automations`/`workspace.automations`; not parametrized
through `helpers.SPECS` (separate scopes, sub-resources, custom actions).
Not verified against a live server yet.

Loaded rows two deep, on both scopes: the automation families off the loaded project
and workspace, and each automation's nodes, edges and activities off the loaded
*automation* -- so the automation id is written once, where it is created. The
uuid-vs-key parity check keeps the flat path for the usual reason."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedProject, LoadedWorkspace, PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.automations import (
    CreateAutomation,
    CreateAutomationEdge,
    CreateAutomationNode,
    UpdateAutomation,
    UpdateAutomationNode,
)

from .helpers import unique_name


@pytest.fixture
def project_automation(project: LoadedProject) -> Iterator[Any]:
    """One freshly created project automation, deleted afterwards."""
    created = project.automations.create(
        CreateAutomation(name=unique_name("automation"), scope="work-item")
    )
    yield created
    try:
        project.automations.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def workspace_automation(workspace: LoadedWorkspace) -> Iterator[Any]:
    """One freshly created workspace (global) automation, deleted afterwards."""
    created = workspace.automations.create(
        CreateAutomation(name=unique_name("automation"), scope="work-item")
    )
    yield created
    try:
        workspace.automations.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def project_trigger_node(project: LoadedProject, project_automation: Any) -> Iterator[Any]:
    """One trigger node on `project_automation`, deleted afterwards."""
    created = project_automation.nodes.create(
        CreateAutomationNode(
            handler_name="record_created", name=unique_name("node"), node_type="trigger"
        ),
    )
    yield created
    try:
        project_automation.nodes.delete(created.id)
    except Exception:
        pass


class TestProjectAutomationsCrud:
    def test_list_returns_a_page(self, project: LoadedProject) -> None:
        page = project.automations.list()
        assert isinstance(page.data, list)

    def test_list_by_project_key_agrees_with_list_by_id(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        project_automation: Any,
    ) -> None:
        automations = client.v2.workspaces.projects.automations
        by_id = {row.id for row in automations.list(workspace_slug, project_id).data}
        by_key = {row.id for row in automations.list(workspace_slug, project_key).data}
        assert project_automation.id in by_id
        assert by_id == by_key

    def test_create_returns_the_written_fields(self, project: LoadedProject) -> None:
        name = unique_name("automation")
        created = project.automations.create(CreateAutomation(name=name, scope="work-item"))
        try:
            assert created.name == name
            assert created.scope == "work-item"
            assert created.status == "draft"  # server default until `set_status` publishes it
            assert created.id
        finally:
            project.automations.delete(created.id)

    def test_retrieve_returns_the_created_row(
        self, project: LoadedProject, project_automation: Any
    ) -> None:
        fetched = project.automations.retrieve(project_automation.id)
        assert fetched.id == project_automation.id
        assert fetched.name == project_automation.name

    def test_retrieve_with_fields_is_sparse(
        self, project: LoadedProject, project_automation: Any
    ) -> None:
        fetched = project.automations.retrieve(project_automation.id, fields=["id", "name"])
        assert fetched.id == project_automation.id
        assert fetched.scope is None

    def test_find_by_name(self, project: LoadedProject, project_automation: Any) -> None:
        found = project.automations.find_by_name(project_automation.name)
        assert found.id == project_automation.id

    def test_patch_updates_only_the_given_fields(
        self, project: LoadedProject, project_automation: Any
    ) -> None:
        new_name = unique_name("automation-renamed")
        updated = project.automations.update(project_automation.id, UpdateAutomation(name=new_name))
        assert updated.id == project_automation.id
        assert updated.name == new_name
        assert updated.scope == project_automation.scope  # untouched field survives the PATCH

    def test_delete_then_retrieve_404s(self, project: LoadedProject) -> None:
        created = project.automations.create(
            CreateAutomation(name=unique_name("automation"), scope="work-item")
        )
        project.automations.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project.automations.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_set_status_enables_and_moves_out_of_draft(
        self, project: LoadedProject, project_automation: Any
    ) -> None:
        assert project_automation.status == "draft"
        # The server refuses to enable an automation with no trigger/action
        # ("Automation cannot be enabled until it has at least one trigger and
        # one action.") -- seed the minimum graph first.
        project_automation.nodes.create(
            CreateAutomationNode(
                handler_name="record_created", name=unique_name("trigger"), node_type="trigger"
            ),
        )
        project_automation.nodes.create(
            CreateAutomationNode(
                handler_name="add_comment",
                name=unique_name("action"),
                node_type="action",
                config={"comment_text": "Automated comment"},
            ),
        )
        result = project.automations.set_status(project_automation.id, is_enabled=True)
        assert result is None
        refetched = project.automations.retrieve(project_automation.id)
        assert refetched.is_enabled is True
        assert refetched.status != "draft"


class TestWorkspaceAutomationsCrud:
    def test_list_returns_a_page_and_excludes_project_scope(
        self, workspace: LoadedWorkspace
    ) -> None:
        page = workspace.automations.list()
        assert isinstance(page.data, list)

    def test_create_retrieve_delete_round_trip(self, workspace: LoadedWorkspace) -> None:
        name = unique_name("automation")
        created = workspace.automations.create(CreateAutomation(name=name, scope="work-item"))
        try:
            fetched = workspace.automations.retrieve(created.id)
            assert fetched.name == name
            assert fetched.scope == "work-item"
        finally:
            workspace.automations.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            workspace.automations.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_set_status_disables(
        self, workspace: LoadedWorkspace, workspace_automation: Any
    ) -> None:
        # Same enable precondition as the project-scoped test: at least one
        # trigger and one action.
        workspace_automation.nodes.create(
            CreateAutomationNode(
                handler_name="record_created", name=unique_name("trigger"), node_type="trigger"
            ),
        )
        workspace_automation.nodes.create(
            CreateAutomationNode(
                handler_name="add_comment",
                name=unique_name("action"),
                node_type="action",
                config={"comment_text": "Automated comment"},
            ),
        )
        workspace.automations.set_status(workspace_automation.id, is_enabled=True)
        result = workspace.automations.set_status(workspace_automation.id, is_enabled=False)
        assert result is None
        refetched = workspace.automations.retrieve(workspace_automation.id)
        assert refetched.is_enabled is False


class TestProjectAutomationNodes:
    def test_create_list_retrieve(
        self,
        project: LoadedProject,
        project_automation: Any,
        project_trigger_node: Any,
    ) -> None:
        page = project_automation.nodes.list()
        assert any(node.id == project_trigger_node.id for node in page.data)

        fetched = project_automation.nodes.retrieve(project_trigger_node.id)
        assert fetched.id == project_trigger_node.id
        assert fetched.node_type == "trigger"

    def test_update_and_delete(self, project: LoadedProject, project_automation: Any) -> None:
        created = project_automation.nodes.create(
            CreateAutomationNode(
                handler_name="record_created", name=unique_name("node"), node_type="trigger"
            ),
        )
        updated = project_automation.nodes.update(
            created.id, UpdateAutomationNode(is_enabled=False)
        )
        assert updated.is_enabled is False

        project_automation.nodes.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project_automation.nodes.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_regenerate_webhook_secret_returns_a_new_secret(
        self, project: LoadedProject, project_automation: Any
    ) -> None:
        """`regenerate_webhook_secret` only accepts a `send_webhook` action
        node -- any other handler 400s "Only send_webhook nodes can rotate
        webhook secrets." (no separate trigger handler exists)."""
        node = project_automation.nodes.create(
            CreateAutomationNode(
                handler_name="send_webhook",
                name=unique_name("webhook-node"),
                node_type="action",
                config={"url": "https://example.com/webhook-test", "secret": "test-secret-value"},
            ),
        )
        try:
            first = project_automation.nodes.regenerate_webhook_secret(node.id)
            second = project_automation.nodes.regenerate_webhook_secret(node.id)
            assert first.secret
            assert second.secret
            assert first.secret != second.secret  # rotation actually rotates
        finally:
            project_automation.nodes.delete(node.id)


class TestProjectAutomationEdges:
    def test_create_connects_two_nodes_and_lists(
        self, project: LoadedProject, project_automation: Any
    ) -> None:
        source = project_automation.nodes.create(
            CreateAutomationNode(
                handler_name="record_created", name=unique_name("source"), node_type="trigger"
            ),
        )
        target = project_automation.nodes.create(
            CreateAutomationNode(
                handler_name="add_comment",
                name=unique_name("target"),
                node_type="action",
                config={"comment_text": "Automated comment"},
            ),
        )
        try:
            edge = project_automation.edges.create(
                CreateAutomationEdge(source_node_id=source.id, target_node_id=target.id),
            )
            try:
                assert edge.source_node_id == source.id
                assert edge.target_node_id == target.id

                page = project_automation.edges.list(source_node_id=source.id)
                assert any(row.id == edge.id for row in page.data)

                fetched = project_automation.edges.retrieve(edge.id)
                assert fetched.id == edge.id
            finally:
                project_automation.edges.delete(edge.id)
            with pytest.raises(PlaneAPIError) as exc_info:
                project_automation.edges.retrieve(edge.id)
            assert exc_info.value.status == 404
        finally:
            project_automation.nodes.delete(source.id)
            project_automation.nodes.delete(target.id)


class TestAutomationActivities:
    def test_project_activities_list_returns_a_page(
        self, project: LoadedProject, project_automation: Any
    ) -> None:
        page = project_automation.activities.list()
        assert isinstance(page.data, list)

    def test_workspace_activities_list_returns_a_page(
        self, workspace: LoadedWorkspace, workspace_automation: Any
    ) -> None:
        page = workspace_automation.activities.list()
        assert isinstance(page.data, list)
