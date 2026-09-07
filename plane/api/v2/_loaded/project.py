"""A fetched project row that is also the place its children live."""

from __future__ import annotations

from ....models.v2.projects import Project
from .._kernel.loaded import Loaded, Owned


class LoadedProject(Loaded, Project):
    """A project row that is also the place its children live."""

    model_config = {**Project.model_config, "arbitrary_types_allowed": True}

    @property
    def states(self) -> Owned:
        return Owned(self._resources.states, self._ids, self._id_names)

    @property
    def labels(self) -> Owned:
        return Owned(self._resources.labels, self._ids, self._id_names)

    @property
    def work_items(self) -> Owned:
        return Owned(self._resources.work_items, self._ids, self._id_names)
