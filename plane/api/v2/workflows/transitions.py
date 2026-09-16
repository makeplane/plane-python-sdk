"""State transitions attached to a workflow (api_v2). On create, `state_id` is the
source, `transition_state_id` the target, with an optional `rejection_state_id`
and approval gating (`required_approvals`, `member_ids`)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from ....models.v2.workflows import (
    CreateWorkflowTransition,
    UpdateWorkflowTransition,
    WorkflowTransition,
)
from .._generated.constants import (
    WorkflowTransitionsCreateField,
    WorkflowTransitionsListField,
    WorkflowTransitionsListOrderBy,
    WorkflowTransitionsPartialUpdateField,
    WorkflowTransitionsRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
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
        slug: str,
        project: str,
        workflow: str,
        *,
        fields: Sequence[WorkflowTransitionsListField] | None = None,
        order_by: WorkflowTransitionsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
    ) -> Page[WorkflowTransition]:
        """One page of transitions attached to a workflow. The golden declares no
        query filters for this operation beyond `fields`/`order_by`."""
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
        fields: Sequence[WorkflowTransitionsListField] | None = None,
        order_by: WorkflowTransitionsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
    ) -> Iterator[WorkflowTransition]:
        """Every transition attached to a workflow, following pages automatically."""
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
        transition: str,
        *,
        fields: Sequence[WorkflowTransitionsRetrieveField] | None = None,
    ) -> WorkflowTransition:
        return self._retrieve(
            pk=transition,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            workflow_id=workflow,
        )

    def create(
        self,
        slug: str,
        project: str,
        workflow: str,
        data: CreateWorkflowTransition,
        *,
        fields: Sequence[WorkflowTransitionsCreateField] | None = None,
    ) -> WorkflowTransition:
        return self._create(
            data,
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
        transition: str,
        data: UpdateWorkflowTransition,
        *,
        fields: Sequence[WorkflowTransitionsPartialUpdateField] | None = None,
    ) -> WorkflowTransition:
        return self._update(
            data,
            pk=transition,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            workflow_id=workflow,
        )

    def delete(self, slug: str, project: str, workflow: str, transition: str) -> None:
        return self._delete(pk=transition, slug=slug, project_id=project, workflow_id=workflow)
