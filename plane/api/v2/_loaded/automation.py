"""Fetched automation rows that are also the place their children live.

Both scopes exist here, side by side, precisely so they stay diffable: the project
flavour binds three ids (`slug`, `project`, `automation` -- `bind3`) and the
workspace flavour binds two (`slug`, `automation` -- `bind2`), and each exposes the
same three children (`edges`, `nodes`, `activities`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.automations import Automation
from .._kernel.loaded import Loaded, Owned, bind2, bind3

if TYPE_CHECKING:
    from ..automations import (
        ProjectAutomationActivities,
        ProjectAutomationEdges,
        ProjectAutomationNodes,
        ProjectAutomations,
        WorkspaceAutomationActivities,
        WorkspaceAutomationEdges,
        WorkspaceAutomationNodes,
        WorkspaceAutomations,
    )

    # Typed views on `Owned`: each child resource's own methods with the parent's
    # path ids already supplied. Evaluated only by a type checker -- at runtime
    # these properties return a plain `Owned`.

    class _OwnedProjectAutomationEdges(Owned["ProjectAutomationEdges"]):
        list = staticmethod(bind3(ProjectAutomationEdges.list))
        iterate = staticmethod(bind3(ProjectAutomationEdges.iterate))
        retrieve = staticmethod(bind3(ProjectAutomationEdges.retrieve))
        create = staticmethod(bind3(ProjectAutomationEdges.create))
        update = staticmethod(bind3(ProjectAutomationEdges.update))
        delete = staticmethod(bind3(ProjectAutomationEdges.delete))

    class _OwnedProjectAutomationNodes(Owned["ProjectAutomationNodes"]):
        list = staticmethod(bind3(ProjectAutomationNodes.list))
        iterate = staticmethod(bind3(ProjectAutomationNodes.iterate))
        retrieve = staticmethod(bind3(ProjectAutomationNodes.retrieve))
        find_by_name = staticmethod(bind3(ProjectAutomationNodes.find_by_name))
        create = staticmethod(bind3(ProjectAutomationNodes.create))
        update = staticmethod(bind3(ProjectAutomationNodes.update))
        delete = staticmethod(bind3(ProjectAutomationNodes.delete))
        regenerate_webhook_secret = staticmethod(
            bind3(ProjectAutomationNodes.regenerate_webhook_secret)
        )

    class _OwnedProjectAutomationActivities(Owned["ProjectAutomationActivities"]):
        list = staticmethod(bind3(ProjectAutomationActivities.list))
        iterate = staticmethod(bind3(ProjectAutomationActivities.iterate))
        retrieve = staticmethod(bind3(ProjectAutomationActivities.retrieve))

    class _OwnedWorkspaceAutomationEdges(Owned["WorkspaceAutomationEdges"]):
        list = staticmethod(bind2(WorkspaceAutomationEdges.list))
        iterate = staticmethod(bind2(WorkspaceAutomationEdges.iterate))
        retrieve = staticmethod(bind2(WorkspaceAutomationEdges.retrieve))
        create = staticmethod(bind2(WorkspaceAutomationEdges.create))
        update = staticmethod(bind2(WorkspaceAutomationEdges.update))
        delete = staticmethod(bind2(WorkspaceAutomationEdges.delete))

    class _OwnedWorkspaceAutomationNodes(Owned["WorkspaceAutomationNodes"]):
        list = staticmethod(bind2(WorkspaceAutomationNodes.list))
        iterate = staticmethod(bind2(WorkspaceAutomationNodes.iterate))
        retrieve = staticmethod(bind2(WorkspaceAutomationNodes.retrieve))
        find_by_name = staticmethod(bind2(WorkspaceAutomationNodes.find_by_name))
        create = staticmethod(bind2(WorkspaceAutomationNodes.create))
        update = staticmethod(bind2(WorkspaceAutomationNodes.update))
        delete = staticmethod(bind2(WorkspaceAutomationNodes.delete))
        regenerate_webhook_secret = staticmethod(
            bind2(WorkspaceAutomationNodes.regenerate_webhook_secret)
        )

    class _OwnedWorkspaceAutomationActivities(Owned["WorkspaceAutomationActivities"]):
        list = staticmethod(bind2(WorkspaceAutomationActivities.list))
        iterate = staticmethod(bind2(WorkspaceAutomationActivities.iterate))
        retrieve = staticmethod(bind2(WorkspaceAutomationActivities.retrieve))


class LoadedProjectAutomation(Loaded, Automation):
    """A project-scoped automation row that is also the place its children live."""

    model_config = {**Automation.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `ProjectAutomations._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: ProjectAutomations

    @property
    def edges(self) -> _OwnedProjectAutomationEdges:
        return cast(
            "_OwnedProjectAutomationEdges", Owned(self._resources.edges, self._ids, self._id_names)
        )

    @property
    def nodes(self) -> _OwnedProjectAutomationNodes:
        return cast(
            "_OwnedProjectAutomationNodes", Owned(self._resources.nodes, self._ids, self._id_names)
        )

    @property
    def activities(self) -> _OwnedProjectAutomationActivities:
        return cast(
            "_OwnedProjectAutomationActivities",
            Owned(self._resources.activities, self._ids, self._id_names),
        )


class LoadedWorkspaceAutomation(Loaded, Automation):
    """A workspace-scoped automation row that is also the place its children live."""

    model_config = {**Automation.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `WorkspaceAutomations._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: WorkspaceAutomations

    @property
    def edges(self) -> _OwnedWorkspaceAutomationEdges:
        return cast(
            "_OwnedWorkspaceAutomationEdges",
            Owned(self._resources.edges, self._ids, self._id_names),
        )

    @property
    def nodes(self) -> _OwnedWorkspaceAutomationNodes:
        return cast(
            "_OwnedWorkspaceAutomationNodes",
            Owned(self._resources.nodes, self._ids, self._id_names),
        )

    @property
    def activities(self) -> _OwnedWorkspaceAutomationActivities:
        return cast(
            "_OwnedWorkspaceAutomationActivities",
            Owned(self._resources.activities, self._ids, self._id_names),
        )
