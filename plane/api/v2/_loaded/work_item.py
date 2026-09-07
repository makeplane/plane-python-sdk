"""A fetched work item row that is also the place its children live."""

from __future__ import annotations

from ....models.v2.work_items import WorkItem
from .._kernel.loaded import Loaded, Owned


class LoadedWorkItem(Loaded, WorkItem):
    """A work item row that is also the place its children live."""

    model_config = {**WorkItem.model_config, "arbitrary_types_allowed": True}

    @property
    def comments(self) -> Owned:
        return Owned(self._resources.comments, self._ids, self._id_names)
