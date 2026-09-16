"""Fetched work item property rows that are also the place their options (and,
workspace-scoped, contexts) live.

Both scopes exist here, side by side, so they stay diffable: the project flavour
binds three ids (`slug`, `project`, `property` -- `bind3`) and the workspace
flavour binds two (`slug`, `property` -- `bind2`). The workspace flavour also
carries `.contexts`, which the project one has no equivalent of.

`options` collides with `WorkItemProperty.options`, a real API field (the
inlined choices for OPTION-type properties), so the navigation property is
`property_options` on both flavours -- see `NAVIGATION_ALIASES` in
`tests/v2/test_loaded_navigation.py`. `contexts` has no such collision."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.work_item_properties import WorkItemProperty
from .._kernel.loaded import Loaded, Owned, bind2, bind3

if TYPE_CHECKING:
    from ..work_item_properties import (
        WorkItemProperties,
        WorkItemPropertyContexts,
        WorkItemPropertyOptions,
        WorkspaceWorkItemProperties,
        WorkspaceWorkItemPropertyOptions,
    )

    # Typed views on `Owned`: the child resource's own methods with the parent's
    # path ids already supplied. Evaluated only by a type checker -- at runtime
    # these properties return a plain `Owned`.

    class _OwnedWorkItemPropertyOptions(Owned["WorkItemPropertyOptions"]):
        list = staticmethod(bind3(WorkItemPropertyOptions.list))
        iterate = staticmethod(bind3(WorkItemPropertyOptions.iterate))
        retrieve = staticmethod(bind3(WorkItemPropertyOptions.retrieve))
        find_by_name = staticmethod(bind3(WorkItemPropertyOptions.find_by_name))
        create = staticmethod(bind3(WorkItemPropertyOptions.create))
        update = staticmethod(bind3(WorkItemPropertyOptions.update))
        delete = staticmethod(bind3(WorkItemPropertyOptions.delete))

    class _OwnedWorkspaceWorkItemPropertyOptions(Owned["WorkspaceWorkItemPropertyOptions"]):
        list = staticmethod(bind2(WorkspaceWorkItemPropertyOptions.list))
        iterate = staticmethod(bind2(WorkspaceWorkItemPropertyOptions.iterate))
        retrieve = staticmethod(bind2(WorkspaceWorkItemPropertyOptions.retrieve))
        find_by_name = staticmethod(bind2(WorkspaceWorkItemPropertyOptions.find_by_name))
        create = staticmethod(bind2(WorkspaceWorkItemPropertyOptions.create))
        update = staticmethod(bind2(WorkspaceWorkItemPropertyOptions.update))
        delete = staticmethod(bind2(WorkspaceWorkItemPropertyOptions.delete))

    class _OwnedWorkItemPropertyContexts(Owned["WorkItemPropertyContexts"]):
        list = staticmethod(bind2(WorkItemPropertyContexts.list))
        iterate = staticmethod(bind2(WorkItemPropertyContexts.iterate))
        retrieve = staticmethod(bind2(WorkItemPropertyContexts.retrieve))
        find_by_name = staticmethod(bind2(WorkItemPropertyContexts.find_by_name))
        create = staticmethod(bind2(WorkItemPropertyContexts.create))
        update = staticmethod(bind2(WorkItemPropertyContexts.update))
        delete = staticmethod(bind2(WorkItemPropertyContexts.delete))


class LoadedWorkItemProperty(Loaded, WorkItemProperty):
    """A project-scoped work item property row that is also the place its options
    live."""

    model_config = {**WorkItemProperty.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `WorkItemProperties._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: WorkItemProperties

    @property
    def property_options(self) -> _OwnedWorkItemPropertyOptions:
        """Aliased from `options`: `WorkItemProperty.options` is itself a real API
        field (the inlined choices for OPTION-type properties), so the navigation
        property cannot reuse that name."""
        return cast(
            "_OwnedWorkItemPropertyOptions",
            Owned(self._resources.options, self._ids, self._id_names),
        )


class LoadedWorkspaceWorkItemProperty(Loaded, WorkItemProperty):
    """A workspace-scoped work item property row that is also the place its
    options and contexts live."""

    model_config = {**WorkItemProperty.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        _resources: WorkspaceWorkItemProperties

    @property
    def property_options(self) -> _OwnedWorkspaceWorkItemPropertyOptions:
        """Aliased from `options` -- see
        `LoadedWorkItemProperty.property_options`."""
        return cast(
            "_OwnedWorkspaceWorkItemPropertyOptions",
            Owned(self._resources.options, self._ids, self._id_names),
        )

    @property
    def contexts(self) -> _OwnedWorkItemPropertyContexts:
        return cast(
            "_OwnedWorkItemPropertyContexts",
            Owned(self._resources.contexts, self._ids, self._id_names),
        )
