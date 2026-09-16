"""Fetched workflow rows that are also the place their `states`/`transitions`
live -- the same one-scope shape as `_loaded/work_item_type.py`, minus the
workspace flavour: workflows are project-only."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.workflows import Workflow
from .._kernel.loaded import Loaded, Owned, bind3

if TYPE_CHECKING:
    from ..workflows import Workflows, WorkflowStates, WorkflowTransitions

    # Typed views on `Owned`: each child resource's own methods with the parent's
    # path ids already supplied. Evaluated only by a type checker -- at runtime
    # these properties return a plain `Owned`.

    class _OwnedWorkflowStates(Owned["WorkflowStates"]):
        list = staticmethod(bind3(WorkflowStates.list))
        iterate = staticmethod(bind3(WorkflowStates.iterate))
        retrieve = staticmethod(bind3(WorkflowStates.retrieve))
        attach = staticmethod(bind3(WorkflowStates.attach))
        update = staticmethod(bind3(WorkflowStates.update))
        delete = staticmethod(bind3(WorkflowStates.delete))

    class _OwnedWorkflowTransitions(Owned["WorkflowTransitions"]):
        list = staticmethod(bind3(WorkflowTransitions.list))
        iterate = staticmethod(bind3(WorkflowTransitions.iterate))
        retrieve = staticmethod(bind3(WorkflowTransitions.retrieve))
        create = staticmethod(bind3(WorkflowTransitions.create))
        update = staticmethod(bind3(WorkflowTransitions.update))
        delete = staticmethod(bind3(WorkflowTransitions.delete))


class LoadedWorkflow(Loaded, Workflow):
    """A fetched workflow row that is also the place its `states`/`transitions`
    live."""

    model_config = {**Workflow.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Workflows._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Workflows

    @property
    def states(self) -> _OwnedWorkflowStates:
        return cast(
            "_OwnedWorkflowStates", Owned(self._resources.states, self._ids, self._id_names)
        )

    @property
    def transitions(self) -> _OwnedWorkflowTransitions:
        return cast(
            "_OwnedWorkflowTransitions",
            Owned(self._resources.transitions, self._ids, self._id_names),
        )
