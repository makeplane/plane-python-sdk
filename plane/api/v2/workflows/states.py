"""States attached to a workflow (api_v2). `update`/`delete` operate on the
per-workflow membership row, not the underlying project `State` itself --
`delete` is the un-attach.

`attach` bulk-attaches existing project states by id and is named `attach`, not
`create`, for a specific reason: it POSTs `{state_ids}` to the *collection* URL
and answers an **array** of the resulting membership rows, not a single row. The
golden's own `$ref` for `workflow_states_create` claims a different response
shape (`WorkflowStateWriteRequest`, modeled on `type`/`is_default`/
`allow_issue_creation` -- the *update* body, not a bulk-attach response); this
project recorded that mismatch independently as a genuine spec defect (see
`plane/models/v2/workflows.py`). `attach` preserves the real, observed
behaviour rather than "fixing" the code to match the incorrect schema, so it
goes through the kernel's `_custom_action_list` (arbitrary-envelope, list of
`model`), not `_create`."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Sequence

from ....models.v2.workflows import UpdateWorkflowState, WorkflowState, WorkflowStateCreate
from .._generated.constants import (
    WorkflowStatesCreateField,
    WorkflowStatesListField,
    WorkflowStatesListOrderBy,
    WorkflowStatesPartialUpdateField,
    WorkflowStatesRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource


class WorkflowStates(V2Resource[WorkflowState, WorkflowStateCreate, UpdateWorkflowState]):
    path = "/workspaces/{slug}/projects/{project_id}/workflows/{workflow_id}/states/"
    model = WorkflowState
    operations = {
        "list": "workflow_states_list",
        "retrieve": "workflow_states_retrieve",
        "attach": "workflow_states_create",
        "update": "workflow_states_partial_update",
        "delete": "workflow_states_destroy",
    }

    def list(
        self,
        slug: str,
        project: str,
        workflow: str,
        *,
        fields: Sequence[WorkflowStatesListField] | None = None,
        order_by: WorkflowStatesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
    ) -> Page[WorkflowState]:
        """One page of states attached to a workflow. The golden declares no query
        filters for this operation beyond `fields`/`order_by`."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
            },
            slug=slug,
            project_id=project,
            workflow_id=workflow,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        workflow: str,
        *,
        fields: Sequence[WorkflowStatesListField] | None = None,
        order_by: WorkflowStatesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
    ) -> Iterator[WorkflowState]:
        """Every state attached to a workflow, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
            },
            slug=slug,
            project_id=project,
            workflow_id=workflow,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        workflow: str,
        state: str,
        *,
        fields: Sequence[WorkflowStatesRetrieveField] | None = None,
    ) -> WorkflowState:
        return self._retrieve(
            pk=state,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            workflow_id=workflow,
        )

    def attach(
        self,
        slug: str,
        project: str,
        workflow: str,
        state_ids: Sequence[str],
        *,
        fields: Sequence[WorkflowStatesCreateField] | None = None,
    ) -> builtins.list[WorkflowState]:
        """Bulk-attach existing project states to this workflow by id. See the
        module docstring for why this answers an array through
        `_custom_action_list` rather than going through `_create`."""
        return self._custom_action_list(
            "attach",
            model=self.model,
            data=WorkflowStateCreate(state_ids=list(state_ids)),
            params={"fields": fields},
            slug=slug,
            project_id=project,
            workflow_id=workflow,
        )

    def update(
        self,
        slug: str,
        project: str,
        workflow: str,
        state: str,
        data: UpdateWorkflowState,
        *,
        fields: Sequence[WorkflowStatesPartialUpdateField] | None = None,
    ) -> WorkflowState:
        """Update the per-workflow membership row (`type`/`is_default`/
        `allow_issue_creation`) -- not the underlying project `State`."""
        return self._update(
            data,
            pk=state,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            workflow_id=workflow,
        )

    def delete(self, slug: str, project: str, workflow: str, state: str) -> None:
        """Detach a state from this workflow -- the un-attach."""
        return self._delete(pk=state, slug=slug, project_id=project, workflow_id=workflow)
