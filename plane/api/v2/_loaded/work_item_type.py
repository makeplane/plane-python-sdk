"""Fetched work item type rows that are also the place their properties live.

Both scopes exist here, side by side, so they stay diffable: the project flavour
binds three ids (`slug`, `project`, `type` -- `bind3`) and the workspace flavour
binds two (`slug`, `type` -- `bind2`); each exposes the same one child
(`properties`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.work_item_types import WorkItemType
from .._kernel.loaded import Loaded, Owned, bind2, bind3

if TYPE_CHECKING:
    from ..work_item_types import (
        WorkItemTypeProperties,
        WorkItemTypes,
        WorkspaceWorkItemTypeProperties,
        WorkspaceWorkItemTypes,
    )

    # Typed views on `Owned`: the child resource's own methods with the parent's
    # path ids already supplied. Evaluated only by a type checker -- at runtime
    # these properties return a plain `Owned`.

    class _OwnedWorkItemTypeProperties(Owned["WorkItemTypeProperties"]):
        list = staticmethod(bind3(WorkItemTypeProperties.list))
        iterate = staticmethod(bind3(WorkItemTypeProperties.iterate))
        retrieve = staticmethod(bind3(WorkItemTypeProperties.retrieve))
        link = staticmethod(bind3(WorkItemTypeProperties.link))
        unlink = staticmethod(bind3(WorkItemTypeProperties.unlink))

    class _OwnedWorkspaceWorkItemTypeProperties(Owned["WorkspaceWorkItemTypeProperties"]):
        list = staticmethod(bind2(WorkspaceWorkItemTypeProperties.list))
        iterate = staticmethod(bind2(WorkspaceWorkItemTypeProperties.iterate))
        retrieve = staticmethod(bind2(WorkspaceWorkItemTypeProperties.retrieve))
        link = staticmethod(bind2(WorkspaceWorkItemTypeProperties.link))
        unlink = staticmethod(bind2(WorkspaceWorkItemTypeProperties.unlink))


class LoadedWorkItemType(Loaded, WorkItemType):
    """A project-scoped work item type row that is also the place its properties
    live."""

    model_config = {**WorkItemType.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `WorkItemTypes._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: WorkItemTypes

    @property
    def properties(self) -> _OwnedWorkItemTypeProperties:
        return cast(
            "_OwnedWorkItemTypeProperties",
            Owned(self._resources.properties, self._ids, self._id_names),
        )


class LoadedWorkspaceWorkItemType(Loaded, WorkItemType):
    """A workspace-scoped work item type row that is also the place its properties
    live."""

    model_config = {**WorkItemType.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        _resources: WorkspaceWorkItemTypes

    @property
    def properties(self) -> _OwnedWorkspaceWorkItemTypeProperties:
        return cast(
            "_OwnedWorkspaceWorkItemTypeProperties",
            Owned(self._resources.properties, self._ids, self._id_names),
        )
