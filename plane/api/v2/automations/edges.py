"""Automation edges (api_v2). An edge connects two nodes (`source_node_id` ->
`target_node_id`) in an automation's graph. Project- and workspace-scoped
families mirror `ProjectAutomations`/`WorkspaceAutomations`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.automations import AutomationEdge, CreateAutomationEdge, UpdateAutomationEdge
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class ProjectAutomationEdges(
    V2Resource[AutomationEdge, CreateAutomationEdge, UpdateAutomationEdge]
):
    path = "/workspaces/{slug}/projects/{project_id}/automations/{automation_id}/edges/"
    model = AutomationEdge
    operations = {
        "list": "project_automation_edges_list",
        "retrieve": "project_automation_edges_retrieve",
        "create": "project_automation_edges_create",
        "update": "project_automation_edges_partial_update",
        "delete": "project_automation_edges_destroy",
    }

    def list(
        self,
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[AutomationEdge]:
        """One page of edges in a project automation's graph.

        `**filters` covers `source_node_id`/`target_node_id`."""
        return self._list(automation_id=automation_id, params={"fields": fields, **filters})

    def iterate(
        self,
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[AutomationEdge]:
        """Every edge in a project automation's graph, following pages automatically."""
        return self._iter(automation_id=automation_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        automation_id: str,
        edge_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> AutomationEdge:
        return self._retrieve(pk=edge_id, automation_id=automation_id, params={"fields": fields})

    def create(self, automation_id: str, data: CreateAutomationEdge) -> AutomationEdge:
        return self._create(data, automation_id=automation_id)

    def update(
        self,
        automation_id: str,
        edge_id: str,
        data: UpdateAutomationEdge,
    ) -> AutomationEdge:
        return self._update(data, pk=edge_id, automation_id=automation_id)

    def delete(self, automation_id: str, edge_id: str) -> None:
        return self._delete(pk=edge_id, automation_id=automation_id)


class WorkspaceAutomationEdges(
    V2Resource[AutomationEdge, CreateAutomationEdge, UpdateAutomationEdge]
):
    path = "/workspaces/{slug}/automations/{automation_id}/edges/"
    model = AutomationEdge
    operations = {
        "list": "workspace_automation_edges_list",
        "retrieve": "workspace_automation_edges_retrieve",
        "create": "workspace_automation_edges_create",
        "update": "workspace_automation_edges_partial_update",
        "delete": "workspace_automation_edges_destroy",
    }

    def list(
        self,
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[AutomationEdge]:
        """One page of edges in a workspace automation's graph."""
        return self._list(automation_id=automation_id, params={"fields": fields, **filters})

    def iterate(
        self,
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[AutomationEdge]:
        """Every edge in a workspace automation's graph, following pages automatically."""
        return self._iter(automation_id=automation_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        automation_id: str,
        edge_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> AutomationEdge:
        return self._retrieve(pk=edge_id, automation_id=automation_id, params={"fields": fields})

    def create(self, automation_id: str, data: CreateAutomationEdge) -> AutomationEdge:
        return self._create(data, automation_id=automation_id)

    def update(
        self, automation_id: str, edge_id: str, data: UpdateAutomationEdge
    ) -> AutomationEdge:
        return self._update(data, pk=edge_id, automation_id=automation_id)

    def delete(self, automation_id: str, edge_id: str) -> None:
        return self._delete(pk=edge_id, automation_id=automation_id)
