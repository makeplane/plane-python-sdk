"""Automations (api_v2). Project- and workspace-scoped families have their own
path templates/operationIds, hence separate `ProjectAutomations`/`WorkspaceAutomations`
classes; `set_status` (204, no body) is the only way to enable/disable one."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.automations import (
    Automation,
    CreateAutomation,
    SetAutomationStatus,
    UpdateAutomation,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .activities import ProjectAutomationActivities, WorkspaceAutomationActivities
from .edges import ProjectAutomationEdges, WorkspaceAutomationEdges
from .nodes import ProjectAutomationNodes, WorkspaceAutomationNodes

__all__ = [
    "ProjectAutomationActivities",
    "ProjectAutomationEdges",
    "ProjectAutomationNodes",
    "ProjectAutomations",
    "WorkspaceAutomationActivities",
    "WorkspaceAutomationEdges",
    "WorkspaceAutomationNodes",
    "WorkspaceAutomations",
]


class ProjectAutomations(V2Resource[Automation, CreateAutomation, UpdateAutomation]):
    path = "/workspaces/{slug}/projects/{project_id}/automations/"
    model = Automation
    operations = {
        "list": "project_automations_list",
        "retrieve": "project_automations_retrieve",
        "create": "project_automations_create",
        "update": "project_automations_partial_update",
        "delete": "project_automations_destroy",
        "set_status": "project_automations_status",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.edges = ProjectAutomationEdges(transport, **self._scope)
        self.nodes = ProjectAutomationNodes(transport, **self._scope)
        self.activities = ProjectAutomationActivities(transport, **self._scope)

    def list(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Page[Automation]:
        """One page of automations in this project.

        `**filters` covers `is_enabled`, `is_global`, `name`, `scope`, `status`, `search`."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[Automation]:
        """Every automation in this project, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self, automation_id: str, *, fields: Sequence[str] | None = None
    ) -> Automation:
        return self._retrieve(pk=automation_id, params={"fields": fields})

    def find_by_name(self, name: str) -> Automation:
        """The one automation with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateAutomation) -> Automation:
        return self._create(data)

    def update(self, automation_id: str, data: UpdateAutomation) -> Automation:
        return self._update(data, pk=automation_id)

    def delete(self, automation_id: str) -> None:
        return self._delete(pk=automation_id)

    def set_status(self, automation_id: str, *, is_enabled: bool) -> None:
        """Enable/disable a project automation (and move it out of draft). 204,
        no row returned -- unlike most custom actions, there is nothing to parse."""
        data = SetAutomationStatus(is_enabled=is_enabled)
        self.transport.request(
            "POST",
            f"{self._detail_url(automation_id)}status/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return None


class WorkspaceAutomations(V2Resource[Automation, CreateAutomation, UpdateAutomation]):
    path = "/workspaces/{slug}/automations/"
    model = Automation
    operations = {
        "list": "workspace_automations_list",
        "retrieve": "workspace_automations_retrieve",
        "create": "workspace_automations_create",
        "update": "workspace_automations_partial_update",
        "delete": "workspace_automations_destroy",
        "set_status": "workspace_automations_status",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.edges = WorkspaceAutomationEdges(transport, **self._scope)
        self.nodes = WorkspaceAutomationNodes(transport, **self._scope)
        self.activities = WorkspaceAutomationActivities(transport, **self._scope)

    def list(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Page[Automation]:
        """One page of workspace-level (global, not-project-tied) automations."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[Automation]:
        """Every workspace-level automation, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self, automation_id: str, *, fields: Sequence[str] | None = None
    ) -> Automation:
        return self._retrieve(pk=automation_id, params={"fields": fields})

    def find_by_name(self, name: str) -> Automation:
        """The one automation with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateAutomation) -> Automation:
        return self._create(data)

    def update(self, automation_id: str, data: UpdateAutomation) -> Automation:
        return self._update(data, pk=automation_id)

    def delete(self, automation_id: str) -> None:
        return self._delete(pk=automation_id)

    def set_status(self, automation_id: str, *, is_enabled: bool) -> None:
        """Enable/disable a workspace automation (and move it out of draft). 204,
        no row returned."""
        data = SetAutomationStatus(is_enabled=is_enabled)
        self.transport.request(
            "POST",
            f"{self._detail_url(automation_id)}status/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return None

