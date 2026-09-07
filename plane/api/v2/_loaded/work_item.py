"""A fetched work item row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.work_items import WorkItem
from .._kernel.loaded import Loaded, Owned, bind3

if TYPE_CHECKING:
    from ..work_items import WorkItems
    from ..work_items.comments import WorkItemComments

    # Typed view on `Owned`: `WorkItemComments`' own methods with `slug`, `project`
    # and `work_item` already supplied -- `bind3`, because three path ids are bound.

    class _OwnedComments(Owned["WorkItemComments"]):
        list = staticmethod(bind3(WorkItemComments.list))
        iterate = staticmethod(bind3(WorkItemComments.iterate))
        retrieve = staticmethod(bind3(WorkItemComments.retrieve))
        create = staticmethod(bind3(WorkItemComments.create))
        update = staticmethod(bind3(WorkItemComments.update))
        delete = staticmethod(bind3(WorkItemComments.delete))
        upsert = staticmethod(bind3(WorkItemComments.upsert))
        bulk_create = staticmethod(bind3(WorkItemComments.bulk_create))
        bulk_update = staticmethod(bind3(WorkItemComments.bulk_update))
        bulk_delete = staticmethod(bind3(WorkItemComments.bulk_delete))


class LoadedWorkItem(Loaded, WorkItem):
    """A work item row that is also the place its children live."""

    model_config = {**WorkItem.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `WorkItems._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: WorkItems

    @property
    def comments(self) -> _OwnedComments:
        return cast("_OwnedComments", Owned(self._resources.comments, self._ids, self._id_names))
