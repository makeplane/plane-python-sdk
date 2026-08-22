"""Automation nodes (api_v2). A node is one trigger/action/condition step in an
automation's graph. Project- and workspace-scoped families mirror
`ProjectAutomations`/`WorkspaceAutomations`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.automations import (
    AutomationNode,
    AutomationWebhookSecret,
    CreateAutomationNode,
    UpdateAutomationNode,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class ProjectAutomationNodes(
    V2Resource[AutomationNode, CreateAutomationNode, UpdateAutomationNode]
):
    path = "/workspaces/{slug}/projects/{project_id}/automations/{automation_id}/nodes/"
    model = AutomationNode
    operations = {
        "list": "project_automation_nodes_list",
        "retrieve": "project_automation_nodes_retrieve",
        "create": "project_automation_nodes_create",
        "update": "project_automation_nodes_partial_update",
        "delete": "project_automation_nodes_destroy",
        "regenerate_webhook_secret": "project_automation_nodes_regenerate_webhook_secret",
    }

    def list(
        self,
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[AutomationNode]:
        """One page of nodes in a project automation's graph.

        `**filters` covers `handler_name`, `is_enabled`, `name`, `node_type`, `search`."""
        return self._list(automation_id=automation_id, params={"fields": fields, **filters})

    def iterate(
        self,
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[AutomationNode]:
        """Every node in a project automation's graph, following pages automatically."""
        return self._iter(automation_id=automation_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        automation_id: str,
        node_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> AutomationNode:
        return self._retrieve(pk=node_id, automation_id=automation_id, params={"fields": fields})

    def find_by_name(self, automation_id: str, name: str) -> AutomationNode:
        """The one node with this name; raises if none or several match."""
        return self._find_one(filters={"name": name}, automation_id=automation_id)

    def create(self, automation_id: str, data: CreateAutomationNode) -> AutomationNode:
        return self._create(data, automation_id=automation_id)

    def update(
        self,
        automation_id: str,
        node_id: str,
        data: UpdateAutomationNode,
    ) -> AutomationNode:
        return self._update(data, pk=node_id, automation_id=automation_id)

    def delete(self, automation_id: str, node_id: str) -> None:
        return self._delete(pk=node_id, automation_id=automation_id)

    def regenerate_webhook_secret(
        self, automation_id: str, node_id: str
    ) -> AutomationWebhookSecret:
        """Rotate the webhook secret for a webhook-trigger node, returning the new one.

        Not built on `_action`: the response model here isn't this resource's own `self.model`."""
        detail_url = self._detail_url(node_id, automation_id=automation_id)
        payload = self.transport.request("POST", f"{detail_url}regenerate-webhook-secret/")
        return AutomationWebhookSecret.model_validate(payload or {})


class WorkspaceAutomationNodes(
    V2Resource[AutomationNode, CreateAutomationNode, UpdateAutomationNode]
):
    path = "/workspaces/{slug}/automations/{automation_id}/nodes/"
    model = AutomationNode
    operations = {
        "list": "workspace_automation_nodes_list",
        "retrieve": "workspace_automation_nodes_retrieve",
        "create": "workspace_automation_nodes_create",
        "update": "workspace_automation_nodes_partial_update",
        "delete": "workspace_automation_nodes_destroy",
        "regenerate_webhook_secret": "workspace_automation_nodes_regenerate_webhook_secret",
    }

    def list(
        self,
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[AutomationNode]:
        """One page of nodes in a workspace automation's graph."""
        return self._list(automation_id=automation_id, params={"fields": fields, **filters})

    def iterate(
        self,
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[AutomationNode]:
        """Every node in a workspace automation's graph, following pages automatically."""
        return self._iter(automation_id=automation_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        automation_id: str,
        node_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> AutomationNode:
        return self._retrieve(pk=node_id, automation_id=automation_id, params={"fields": fields})

    def find_by_name(self, automation_id: str, name: str) -> AutomationNode:
        """The one node with this name; raises if none or several match."""
        return self._find_one(filters={"name": name}, automation_id=automation_id)

    def create(self, automation_id: str, data: CreateAutomationNode) -> AutomationNode:
        return self._create(data, automation_id=automation_id)

    def update(
        self, automation_id: str, node_id: str, data: UpdateAutomationNode
    ) -> AutomationNode:
        return self._update(data, pk=node_id, automation_id=automation_id)

    def delete(self, automation_id: str, node_id: str) -> None:
        return self._delete(pk=node_id, automation_id=automation_id)

    def regenerate_webhook_secret(
        self, automation_id: str, node_id: str
    ) -> AutomationWebhookSecret:
        """Rotate the webhook secret for a webhook-trigger node, returning the new
        one. See `ProjectAutomationNodes.regenerate_webhook_secret` for why this
        bypasses `_action`."""
        detail_url = self._detail_url(node_id, automation_id=automation_id)
        payload = self.transport.request("POST", f"{detail_url}regenerate-webhook-secret/")
        return AutomationWebhookSecret.model_validate(payload or {})
