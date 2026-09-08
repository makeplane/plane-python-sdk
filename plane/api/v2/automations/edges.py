"""Automation edges (api_v2). An edge connects two nodes (`source_node_id` ->
`target_node_id`) in an automation's graph. Project- and workspace-scoped
families mirror `ProjectAutomations`/`WorkspaceAutomations`: project-scoped
methods open with `slug, project, automation` (depth 3); workspace-scoped ones
open with `slug, automation` (depth 2). The golden declares no `expand` for
either family."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.automations import AutomationEdge, CreateAutomationEdge, UpdateAutomationEdge
from .._generated.constants import (
    ProjectAutomationEdgesCreateField,
    ProjectAutomationEdgesListField,
    ProjectAutomationEdgesListFilters,
    ProjectAutomationEdgesListOrderBy,
    ProjectAutomationEdgesPartialUpdateField,
    ProjectAutomationEdgesRetrieveField,
    WorkspaceAutomationEdgesCreateField,
    WorkspaceAutomationEdgesListField,
    WorkspaceAutomationEdgesListFilters,
    WorkspaceAutomationEdgesListOrderBy,
    WorkspaceAutomationEdgesPartialUpdateField,
    WorkspaceAutomationEdgesRetrieveField,
)
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
        slug: str,
        project: str,
        automation: str,
        *,
        fields: Sequence[ProjectAutomationEdgesListField] | None = None,
        order_by: ProjectAutomationEdgesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[ProjectAutomationEdgesListFilters],
    ) -> Page[AutomationEdge]:
        """One page of edges in a project automation's graph.

        `**filters` covers `source_node_id`/`target_node_id`."""
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
        fields: Sequence[ProjectAutomationEdgesListField] | None = None,
        order_by: ProjectAutomationEdgesListOrderBy | None = None,
        **filters: Unpack[ProjectAutomationEdgesListFilters],
    ) -> Iterator[AutomationEdge]:
        """Every edge in a project automation's graph, following pages automatically."""
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
        edge: str,
        *,
        fields: Sequence[ProjectAutomationEdgesRetrieveField] | None = None,
    ) -> AutomationEdge:
        return self._retrieve(
            pk=edge,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            automation_id=automation,
        )

    def create(
        self,
        slug: str,
        project: str,
        automation: str,
        data: CreateAutomationEdge,
        *,
        fields: Sequence[ProjectAutomationEdgesCreateField] | None = None,
    ) -> AutomationEdge:
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
        edge: str,
        data: UpdateAutomationEdge,
        *,
        fields: Sequence[ProjectAutomationEdgesPartialUpdateField] | None = None,
    ) -> AutomationEdge:
        return self._update(
            data,
            pk=edge,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            automation_id=automation,
        )

    def delete(self, slug: str, project: str, automation: str, edge: str) -> None:
        return self._delete(pk=edge, slug=slug, project_id=project, automation_id=automation)


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
        slug: str,
        automation: str,
        *,
        fields: Sequence[WorkspaceAutomationEdgesListField] | None = None,
        order_by: WorkspaceAutomationEdgesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[WorkspaceAutomationEdgesListFilters],
    ) -> Page[AutomationEdge]:
        """One page of edges in a workspace automation's graph."""
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
        fields: Sequence[WorkspaceAutomationEdgesListField] | None = None,
        order_by: WorkspaceAutomationEdgesListOrderBy | None = None,
        **filters: Unpack[WorkspaceAutomationEdgesListFilters],
    ) -> Iterator[AutomationEdge]:
        """Every edge in a workspace automation's graph, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            automation_id=automation,
        )

    def retrieve(
        self,
        slug: str,
        automation: str,
        edge: str,
        *,
        fields: Sequence[WorkspaceAutomationEdgesRetrieveField] | None = None,
    ) -> AutomationEdge:
        return self._retrieve(
            pk=edge, params={"fields": fields}, slug=slug, automation_id=automation
        )

    def create(
        self,
        slug: str,
        automation: str,
        data: CreateAutomationEdge,
        *,
        fields: Sequence[WorkspaceAutomationEdgesCreateField] | None = None,
    ) -> AutomationEdge:
        return self._create(data, params={"fields": fields}, slug=slug, automation_id=automation)

    def update(
        self,
        slug: str,
        automation: str,
        edge: str,
        data: UpdateAutomationEdge,
        *,
        fields: Sequence[WorkspaceAutomationEdgesPartialUpdateField] | None = None,
    ) -> AutomationEdge:
        return self._update(
            data,
            pk=edge,
            params={"fields": fields},
            slug=slug,
            automation_id=automation,
        )

    def delete(self, slug: str, automation: str, edge: str) -> None:
        return self._delete(pk=edge, slug=slug, automation_id=automation)
