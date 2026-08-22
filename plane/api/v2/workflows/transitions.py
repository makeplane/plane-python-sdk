"""State transitions attached to a workflow (api_v2). On create, `state_id` is the
source, `transition_state_id` the target, with an optional `rejection_state_id`
and approval gating (`required_approvals`, `member_ids`)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.workflows import (
    CreateWorkflowTransition,
    UpdateWorkflowTransition,
    WorkflowTransition,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkflowTransitions(
    V2Resource[WorkflowTransition, CreateWorkflowTransition, UpdateWorkflowTransition]
):
    path = "/workspaces/{slug}/projects/{project_id}/workflows/{workflow_id}/state-transitions/"
    model = WorkflowTransition
    operations = {
        "list": "workflow_transitions_list",
        "retrieve": "workflow_transitions_retrieve",
        "create": "workflow_transitions_create",
        "update": "workflow_transitions_partial_update",
        "delete": "workflow_transitions_destroy",
    }

    def list(
        self,
        workflow_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkflowTransition]:
        """One page of transitions attached to a workflow."""
        return self._list(workflow_id=workflow_id, params={"fields": fields, **filters})

    def iterate(
        self,
        workflow_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkflowTransition]:
        """Every transition attached to a workflow, following pages automatically."""
        return self._iter(workflow_id=workflow_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        workflow_id: str,
        pk: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WorkflowTransition:
        return self._retrieve(pk=pk, workflow_id=workflow_id, params={"fields": fields})

    def create(self, workflow_id: str, data: CreateWorkflowTransition) -> WorkflowTransition:
        return self._create(data, workflow_id=workflow_id)

    def update(
        self, workflow_id: str, pk: str, data: UpdateWorkflowTransition
    ) -> WorkflowTransition:
        return self._update(data, pk=pk, workflow_id=workflow_id)

    def delete(self, workflow_id: str, pk: str) -> None:
        return self._delete(pk=pk, workflow_id=workflow_id)
