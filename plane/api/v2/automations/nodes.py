"""Automation nodes (api_v2). A node is one trigger/action/condition step in an
automation's graph. Project- and workspace-scoped families mirror
`ProjectAutomations`/`WorkspaceAutomations`: project-scoped methods open with
`slug, project, automation` (depth 3); workspace-scoped ones open with
`slug, automation` (depth 2). The golden declares no `expand` for either family."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.automations import (
    AutomationNode,
    AutomationWebhookSecret,
    CreateAutomationNode,
    UpdateAutomationNode,
)
from .._generated.constants import (
    ProjectAutomationNodesCreateField,
    ProjectAutomationNodesListField,
    ProjectAutomationNodesListFilters,
    ProjectAutomationNodesListOrderBy,
    ProjectAutomationNodesPartialUpdateField,
    ProjectAutomationNodesRetrieveField,
    WorkspaceAutomationNodesCreateField,
    WorkspaceAutomationNodesListField,
    WorkspaceAutomationNodesListFilters,
    WorkspaceAutomationNodesListOrderBy,
    WorkspaceAutomationNodesPartialUpdateField,
    WorkspaceAutomationNodesRetrieveField,
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
        "regenerate-webhook-secret": "project_automation_nodes_regenerate_webhook_secret",
    }

    def list(
        self,
        slug: str,
        project: str,
        automation: str,
        *,
        fields: Sequence[ProjectAutomationNodesListField] | None = None,
        order_by: ProjectAutomationNodesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[ProjectAutomationNodesListFilters],
    ) -> Page[AutomationNode]:
        """One page of nodes in a project automation's graph.

        `**filters` covers `handler_name`, `is_enabled`, `name`, `node_type`, `search`."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
            project_id=project,
            automation_id=automation,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        automation: str,
        *,
        fields: Sequence[ProjectAutomationNodesListField] | None = None,
        order_by: ProjectAutomationNodesListOrderBy | None = None,
        **filters: Unpack[ProjectAutomationNodesListFilters],
    ) -> Iterator[AutomationNode]:
        """Every node in a project automation's graph, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
            automation_id=automation,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        automation: str,
        node: str,
        *,
        fields: Sequence[ProjectAutomationNodesRetrieveField] | None = None,
    ) -> AutomationNode:
        return self._retrieve(
            pk=node,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            automation_id=automation,
        )

    def find_by_name(self, slug: str, project: str, automation: str, name: str) -> AutomationNode:
        """The one node with this name; raises if none or several match."""
        return self._find_one(
            filters={"name": name}, slug=slug, project_id=project, automation_id=automation
        )

    def create(
        self,
        slug: str,
        project: str,
        automation: str,
        data: CreateAutomationNode,
        *,
        fields: Sequence[ProjectAutomationNodesCreateField] | None = None,
    ) -> AutomationNode:
        return self._create(
            data,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            automation_id=automation,
        )

    def update(
        self,
        slug: str,
        project: str,
        automation: str,
        node: str,
        data: UpdateAutomationNode,
        *,
        fields: Sequence[ProjectAutomationNodesPartialUpdateField] | None = None,
    ) -> AutomationNode:
        return self._update(
            data,
            pk=node,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            automation_id=automation,
        )

    def delete(self, slug: str, project: str, automation: str, node: str) -> None:
        return self._delete(pk=node, slug=slug, project_id=project, automation_id=automation)

    def regenerate_webhook_secret(
        self, slug: str, project: str, automation: str, node: str
    ) -> AutomationWebhookSecret:
        """Rotate the webhook secret for a webhook-trigger node, returning the new
        one. Not built on `_action`: the response is `AutomationWebhookSecret`, not
        this resource's own `AutomationNode`, so `_custom_action` is used instead.

        No `fields` param: the golden declares no `?fields=` for this operation at
        all (it is absent from `FIELDS` in `_generated/constants.py`), so there is
        nothing to project even before weighing the one-time-secret exception --
        the same secret-shown-once shape as `Webhooks.regenerate`, but here the
        question of projecting it never arises."""
        return self._custom_action(
            "regenerate-webhook-secret",
            model=AutomationWebhookSecret,
            pk=node,
            slug=slug,
            project_id=project,
            automation_id=automation,
        )


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
        "regenerate-webhook-secret": "workspace_automation_nodes_regenerate_webhook_secret",
    }

    def list(
        self,
        slug: str,
        automation: str,
        *,
        fields: Sequence[WorkspaceAutomationNodesListField] | None = None,
        order_by: WorkspaceAutomationNodesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[WorkspaceAutomationNodesListFilters],
    ) -> Page[AutomationNode]:
        """One page of nodes in a workspace automation's graph."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
            automation_id=automation,
        )

    def iterate(
        self,
        slug: str,
        automation: str,
        *,
        fields: Sequence[WorkspaceAutomationNodesListField] | None = None,
        order_by: WorkspaceAutomationNodesListOrderBy | None = None,
        **filters: Unpack[WorkspaceAutomationNodesListFilters],
    ) -> Iterator[AutomationNode]:
        """Every node in a workspace automation's graph, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            automation_id=automation,
        )

    def retrieve(
        self,
        slug: str,
        automation: str,
        node: str,
        *,
        fields: Sequence[WorkspaceAutomationNodesRetrieveField] | None = None,
    ) -> AutomationNode:
        return self._retrieve(
            pk=node, params={"fields": fields}, slug=slug, automation_id=automation
        )

    def find_by_name(self, slug: str, automation: str, name: str) -> AutomationNode:
        """The one node with this name; raises if none or several match."""
        return self._find_one(filters={"name": name}, slug=slug, automation_id=automation)

    def create(
        self,
        slug: str,
        automation: str,
        data: CreateAutomationNode,
        *,
        fields: Sequence[WorkspaceAutomationNodesCreateField] | None = None,
    ) -> AutomationNode:
        return self._create(data, params={"fields": fields}, slug=slug, automation_id=automation)

    def update(
        self,
        slug: str,
        automation: str,
        node: str,
        data: UpdateAutomationNode,
        *,
        fields: Sequence[WorkspaceAutomationNodesPartialUpdateField] | None = None,
    ) -> AutomationNode:
        return self._update(
            data,
            pk=node,
            params={"fields": fields},
            slug=slug,
            automation_id=automation,
        )

    def delete(self, slug: str, automation: str, node: str) -> None:
        return self._delete(pk=node, slug=slug, automation_id=automation)

    def regenerate_webhook_secret(
        self, slug: str, automation: str, node: str
    ) -> AutomationWebhookSecret:
        """Rotate the webhook secret for a webhook-trigger node, returning the new
        one. See `ProjectAutomationNodes.regenerate_webhook_secret` for why this
        bypasses `_action` and omits `fields`: the golden declares no `?fields=`
        for this operation at all."""
        return self._custom_action(
            "regenerate-webhook-secret",
            model=AutomationWebhookSecret,
            pk=node,
            slug=slug,
            automation_id=automation,
        )
