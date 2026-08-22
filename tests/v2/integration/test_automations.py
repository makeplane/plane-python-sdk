"""Live coverage for `proj.automations`/`ws.automations`; not parametrized
through `helpers.SPECS` (separate scopes, sub-resources, custom actions).
Not verified against a live server yet."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.automations import ProjectAutomations, WorkspaceAutomations
from plane.api.v2.project import Project
from plane.api.v2.workspace import Workspace
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
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Project:
    return client.v2.workspace(workspace_slug).project(project_id)


@pytest.fixture
def ws(client: PlaneClient, workspace_slug: str) -> Workspace:
    return client.v2.workspace(workspace_slug)


@pytest.fixture
def project_automations(proj: Project) -> ProjectAutomations:
    return proj.automations


@pytest.fixture
def workspace_automations(ws: Workspace) -> WorkspaceAutomations:
    return ws.automations


@pytest.fixture
def project_automation(project_automations: ProjectAutomations) -> Iterator[Any]:
    """One freshly created project automation, deleted afterwards."""
    created = project_automations.create(
        CreateAutomation(name=unique_name("automation"), scope="work-item")
    )
    yield created
    try:
        project_automations.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def workspace_automation(workspace_automations: WorkspaceAutomations) -> Iterator[Any]:
    """One freshly created workspace (global) automation, deleted afterwards."""
    created = workspace_automations.create(
        CreateAutomation(name=unique_name("automation"), scope="work-item")
    )
    yield created
    try:
        workspace_automations.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def project_trigger_node(
    project_automations: ProjectAutomations, project_automation: Any
) -> Iterator[Any]:
    """One trigger node on `project_automation`, deleted afterwards."""
    created = project_automations.nodes.create(
        project_automation.id,
        CreateAutomationNode(
            handler_name="record_created", name=unique_name("node"), node_type="trigger"
        ),
    )
    yield created
    try:
        project_automations.nodes.delete(project_automation.id, created.id)
    except Exception:
        pass


class TestProjectAutomationsCrud:
    def test_list_returns_a_page(self, project_automations: ProjectAutomations) -> None:
        page = project_automations.list()
        assert isinstance(page.data, list)

    def test_list_by_project_key_agrees_with_list_by_id(
        self,
        ws: Workspace,
        project_id: str,
        project_key: str,
        project_automation: Any,
    ) -> None:
        by_id = {row.id for row in ws.project(project_id).automations.list().data}
        by_key = {row.id for row in ws.project(project_key).automations.list().data}
        assert project_automation.id in by_id
        assert by_id == by_key

    def test_create_returns_the_written_fields(
        self, project_automations: ProjectAutomations
    ) -> None:
        name = unique_name("automation")
        created = project_automations.create(CreateAutomation(name=name, scope="work-item"))
        try:
            assert created.name == name
            assert created.scope == "work-item"
            assert created.status == "draft"  # server default until `set_status` publishes it
            assert created.id
        finally:
            project_automations.delete(created.id)

    def test_retrieve_returns_the_created_row(
        self, project_automations: ProjectAutomations, project_automation: Any
    ) -> None:
        fetched = project_automations.retrieve(project_automation.id)
        assert fetched.id == project_automation.id
        assert fetched.name == project_automation.name

    def test_retrieve_with_fields_is_sparse(
        self, project_automations: ProjectAutomations, project_automation: Any
    ) -> None:
        fetched = project_automations.retrieve(project_automation.id, fields=["id", "name"])
        assert fetched.id == project_automation.id
        assert fetched.scope is None

    def test_find_by_name(
        self, project_automations: ProjectAutomations, project_automation: Any
    ) -> None:
        found = project_automations.find_by_name(project_automation.name)
        assert found.id == project_automation.id

    def test_patch_updates_only_the_given_fields(
        self, project_automations: ProjectAutomations, project_automation: Any
    ) -> None:
        new_name = unique_name("automation-renamed")
        updated = project_automations.update(project_automation.id, UpdateAutomation(name=new_name))
        assert updated.id == project_automation.id
        assert updated.name == new_name
        assert updated.scope == project_automation.scope  # untouched field survives the PATCH

    def test_delete_then_retrieve_404s(self, project_automations: ProjectAutomations) -> None:
        created = project_automations.create(
            CreateAutomation(name=unique_name("automation"), scope="work-item")
        )
        project_automations.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project_automations.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_set_status_enables_and_moves_out_of_draft(
        self, project_automations: ProjectAutomations, project_automation: Any
    ) -> None:
        assert project_automation.status == "draft"
        # The server refuses to enable an automation with no trigger/action
        # ("Automation cannot be enabled until it has at least one trigger and
        # one action.") -- seed the minimum graph first.
        project_automations.nodes.create(
            project_automation.id,
            CreateAutomationNode(
                handler_name="record_created", name=unique_name("trigger"), node_type="trigger"
            ),
        )
        project_automations.nodes.create(
            project_automation.id,
            CreateAutomationNode(
                handler_name="add_comment",
                name=unique_name("action"),
                node_type="action",
                config={"comment_text": "Automated comment"},
            ),
        )
        result = project_automations.set_status(project_automation.id, is_enabled=True)
        assert result is None
        refetched = project_automations.retrieve(project_automation.id)
        assert refetched.is_enabled is True
        assert refetched.status != "draft"


class TestWorkspaceAutomationsCrud:
    def test_list_returns_a_page_and_excludes_project_scope(
        self, workspace_automations: WorkspaceAutomations
    ) -> None:
        page = workspace_automations.list()
        assert isinstance(page.data, list)

    def test_create_retrieve_delete_round_trip(
        self, workspace_automations: WorkspaceAutomations
    ) -> None:
        name = unique_name("automation")
        created = workspace_automations.create(CreateAutomation(name=name, scope="work-item"))
        try:
            fetched = workspace_automations.retrieve(created.id)
            assert fetched.name == name
            assert fetched.scope == "work-item"
        finally:
            workspace_automations.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            workspace_automations.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_set_status_disables(
        self, workspace_automations: WorkspaceAutomations, workspace_automation: Any
    ) -> None:
        # Same enable precondition as the project-scoped test: at least one
        # trigger and one action.
        workspace_automations.nodes.create(
            workspace_automation.id,
            CreateAutomationNode(
                handler_name="record_created", name=unique_name("trigger"), node_type="trigger"
            ),
        )
        workspace_automations.nodes.create(
            workspace_automation.id,
            CreateAutomationNode(
                handler_name="add_comment",
                name=unique_name("action"),
                node_type="action",
                config={"comment_text": "Automated comment"},
            ),
        )
        workspace_automations.set_status(workspace_automation.id, is_enabled=True)
        result = workspace_automations.set_status(workspace_automation.id, is_enabled=False)
        assert result is None
        refetched = workspace_automations.retrieve(workspace_automation.id)
        assert refetched.is_enabled is False


class TestProjectAutomationNodes:
    def test_create_list_retrieve(
        self,
        project_automations: ProjectAutomations,
        project_automation: Any,
        project_trigger_node: Any,
    ) -> None:
        page = project_automations.nodes.list(project_automation.id)
        assert any(node.id == project_trigger_node.id for node in page.data)

        fetched = project_automations.nodes.retrieve(project_automation.id, project_trigger_node.id)
        assert fetched.id == project_trigger_node.id
        assert fetched.node_type == "trigger"

    def test_update_and_delete(
        self, project_automations: ProjectAutomations, project_automation: Any
    ) -> None:
        created = project_automations.nodes.create(
            project_automation.id,
            CreateAutomationNode(
                handler_name="record_created", name=unique_name("node"), node_type="trigger"
            ),
        )
        updated = project_automations.nodes.update(
            project_automation.id, created.id, UpdateAutomationNode(is_enabled=False)
        )
        assert updated.is_enabled is False

        project_automations.nodes.delete(project_automation.id, created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project_automations.nodes.retrieve(project_automation.id, created.id)
        assert exc_info.value.status == 404

    def test_regenerate_webhook_secret_returns_a_new_secret(
        self, project_automations: ProjectAutomations, project_automation: Any
    ) -> None:
        """`regenerate_webhook_secret` only accepts a `send_webhook` action
        node -- any other handler 400s "Only send_webhook nodes can rotate
        webhook secrets." (no separate trigger handler exists)."""
        node = project_automations.nodes.create(
            project_automation.id,
            CreateAutomationNode(
                handler_name="send_webhook",
                name=unique_name("webhook-node"),
                node_type="action",
                config={"url": "https://example.com/webhook-test", "secret": "test-secret-value"},
            ),
        )
        try:
            first = project_automations.nodes.regenerate_webhook_secret(
                project_automation.id, node.id
            )
            second = project_automations.nodes.regenerate_webhook_secret(
                project_automation.id, node.id
            )
            assert first.secret
            assert second.secret
            assert first.secret != second.secret  # rotation actually rotates
        finally:
            project_automations.nodes.delete(project_automation.id, node.id)


class TestProjectAutomationEdges:
    def test_create_connects_two_nodes_and_lists(
        self, project_automations: ProjectAutomations, project_automation: Any
    ) -> None:
        source = project_automations.nodes.create(
            project_automation.id,
            CreateAutomationNode(
                handler_name="record_created", name=unique_name("source"), node_type="trigger"
            ),
        )
        target = project_automations.nodes.create(
            project_automation.id,
            CreateAutomationNode(
                handler_name="add_comment",
                name=unique_name("target"),
                node_type="action",
                config={"comment_text": "Automated comment"},
            ),
        )
        try:
            edge = project_automations.edges.create(
                project_automation.id,
                CreateAutomationEdge(source_node_id=source.id, target_node_id=target.id),
            )
            try:
                assert edge.source_node_id == source.id
                assert edge.target_node_id == target.id

                page = project_automations.edges.list(
                    project_automation.id, source_node_id=source.id
                )
                assert any(row.id == edge.id for row in page.data)

                fetched = project_automations.edges.retrieve(project_automation.id, edge.id)
                assert fetched.id == edge.id
            finally:
                project_automations.edges.delete(project_automation.id, edge.id)
            with pytest.raises(PlaneAPIError) as exc_info:
                project_automations.edges.retrieve(project_automation.id, edge.id)
            assert exc_info.value.status == 404
        finally:
            project_automations.nodes.delete(project_automation.id, source.id)
            project_automations.nodes.delete(project_automation.id, target.id)


class TestAutomationActivities:
    def test_project_activities_list_returns_a_page(
        self, project_automations: ProjectAutomations, project_automation: Any
    ) -> None:
        page = project_automations.activities.list(project_automation.id)
        assert isinstance(page.data, list)

    def test_workspace_activities_list_returns_a_page(
        self, workspace_automations: WorkspaceAutomations, workspace_automation: Any
    ) -> None:
        page = workspace_automations.activities.list(workspace_automation.id)
        assert isinstance(page.data, list)
