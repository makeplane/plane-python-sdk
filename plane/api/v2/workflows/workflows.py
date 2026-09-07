"""Workflows (api_v2) -- a project's per-work-item-type workflow configuration,
with nested `.states`/`.transitions`. No `upsert`/bulk operations -- CRUD-only."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.workflows import CreateWorkflow, UpdateWorkflow, Workflow
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .states import WorkflowStates
from .transitions import WorkflowTransitions

__all__ = ["WorkflowStates", "WorkflowTransitions", "Workflows"]


class Workflows(V2Resource[Workflow, CreateWorkflow, UpdateWorkflow]):
    path = "/workspaces/{slug}/projects/{project_id}/workflows/"
    model = Workflow
    operations = {
        "list": "workflows_list",
        "retrieve": "workflows_retrieve",
        "create": "workflows_create",
        "update": "workflows_partial_update",
        "delete": "workflows_destroy",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.states = WorkflowStates(transport, **self._scope)
        self.transitions = WorkflowTransitions(transport, **self._scope)

    def list(self, *, fields: Sequence[str] | None = None, **filters: Any) -> Page[Workflow]:
        """One page of workflows in this project."""
        return self._list(params={"fields": fields, **filters})

    def iterate(self, *, fields: Sequence[str] | None = None, **filters: Any) -> Iterator[Workflow]:
        """Every workflow in this project, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, workflow_id: str, *, fields: Sequence[str] | None = None) -> Workflow:
        return self._retrieve(pk=workflow_id, params={"fields": fields})

    def create(self, data: CreateWorkflow) -> Workflow:
        return self._create(data)

    def update(self, workflow_id: str, data: UpdateWorkflow) -> Workflow:
        return self._update(data, pk=workflow_id)

    def delete(self, workflow_id: str) -> None:
        return self._delete(pk=workflow_id)
