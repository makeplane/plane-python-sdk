"""A fetched project row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.projects import Project
from .._kernel.loaded import Loaded, Owned, bind2

if TYPE_CHECKING:
    from ..labels import Labels
    from ..projects import Projects
    from ..states import States
    from ..work_items import WorkItems

    # Typed views on `Owned`: the child resource's own methods with `slug` and
    # `project` already supplied. One line per method, `bind2` because two path ids
    # are bound. Evaluated only by a type checker -- at runtime these properties
    # return a plain `Owned`.

    class _OwnedStates(Owned["States"]):
        list = staticmethod(bind2(States.list))
        iterate = staticmethod(bind2(States.iterate))
        retrieve = staticmethod(bind2(States.retrieve))
        find_by_name = staticmethod(bind2(States.find_by_name))
        create = staticmethod(bind2(States.create))
        update = staticmethod(bind2(States.update))
        delete = staticmethod(bind2(States.delete))
        upsert = staticmethod(bind2(States.upsert))
        bulk_create = staticmethod(bind2(States.bulk_create))
        bulk_update = staticmethod(bind2(States.bulk_update))
        bulk_delete = staticmethod(bind2(States.bulk_delete))

    class _OwnedLabels(Owned["Labels"]):
        list = staticmethod(bind2(Labels.list))
        iterate = staticmethod(bind2(Labels.iterate))
        retrieve = staticmethod(bind2(Labels.retrieve))
        find_by_name = staticmethod(bind2(Labels.find_by_name))
        create = staticmethod(bind2(Labels.create))
        update = staticmethod(bind2(Labels.update))
        delete = staticmethod(bind2(Labels.delete))
        upsert = staticmethod(bind2(Labels.upsert))
        bulk_create = staticmethod(bind2(Labels.bulk_create))
        bulk_update = staticmethod(bind2(Labels.bulk_update))
        bulk_delete = staticmethod(bind2(Labels.bulk_delete))

    class _OwnedWorkItems(Owned["WorkItems"]):
        list = staticmethod(bind2(WorkItems.list))
        iterate = staticmethod(bind2(WorkItems.iterate))
        retrieve = staticmethod(bind2(WorkItems.retrieve))
        create = staticmethod(bind2(WorkItems.create))
        update = staticmethod(bind2(WorkItems.update))
        delete = staticmethod(bind2(WorkItems.delete))
        upsert = staticmethod(bind2(WorkItems.upsert))
        archive = staticmethod(bind2(WorkItems.archive))
        unarchive = staticmethod(bind2(WorkItems.unarchive))
        bulk_create = staticmethod(bind2(WorkItems.bulk_create))
        bulk_update = staticmethod(bind2(WorkItems.bulk_update))
        bulk_delete = staticmethod(bind2(WorkItems.bulk_delete))


class LoadedProject(Loaded, Project):
    """A project row that is also the place its children live."""

    model_config = {**Project.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Declared for the type checker only: a runtime annotation here would make
        # pydantic treat it as a private attribute. `Projects._load` sets it with
        # `object.__setattr__`.
        _resources: Projects

    @property
    def states(self) -> _OwnedStates:
        return cast("_OwnedStates", Owned(self._resources.states, self._ids, self._id_names))

    @property
    def labels(self) -> _OwnedLabels:
        return cast("_OwnedLabels", Owned(self._resources.labels, self._ids, self._id_names))

    @property
    def work_items(self) -> _OwnedWorkItems:
        return cast("_OwnedWorkItems", Owned(self._resources.work_items, self._ids, self._id_names))
