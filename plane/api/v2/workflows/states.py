"""States attached to a workflow (api_v2). `attach` bulk-attaches existing project
states; `update`/`delete` operate on the per-workflow membership row, not the
underlying project `State` itself."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.workflows import UpdateWorkflowState, WorkflowState, WorkflowStateCreate
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkflowStates(V2Resource[WorkflowState, WorkflowStateCreate, UpdateWorkflowState]):
    path = "/workspaces/{slug}/projects/{project_id}/workflows/{workflow_id}/states/"
    model = WorkflowState
    operations = {
        "list": "workflow_states_list",
        "retrieve": "workflow_states_retrieve",
        "create": "workflow_states_create",
        "update": "workflow_states_partial_update",
        "delete": "workflow_states_destroy",
    }

    def list(
        self,
        workflow_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkflowState]:
        """One page of states attached to a workflow."""
        return self._list(workflow_id=workflow_id, params={"fields": fields, **filters})

    def iterate(
        self,
        workflow_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkflowState]:
        """Every state attached to a workflow, following pages automatically."""
        return self._iter(workflow_id=workflow_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        workflow_id: str,
        pk: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WorkflowState:
        return self._retrieve(pk=pk, workflow_id=workflow_id, params={"fields": fields})

    def attach(self, workflow_id: str, data: WorkflowStateCreate) -> WorkflowState:
        """Bulk-attach existing project states by id (`state_ids`). Named `attach`,
        not `create`: the golden's op posts ids and returns an array, not a row creation."""
        return self._create(data, workflow_id=workflow_id)

    def update(self, workflow_id: str, pk: str, data: UpdateWorkflowState) -> WorkflowState:
        """Update the per-workflow membership row (`type`/`is_default`/
        `allow_issue_creation`) -- not the underlying project `State`."""
        return self._update(data, pk=pk, workflow_id=workflow_id)

    def delete(self, workflow_id: str, pk: str) -> None:
        """Detach a state from this workflow."""
        return self._delete(pk=pk, workflow_id=workflow_id)
