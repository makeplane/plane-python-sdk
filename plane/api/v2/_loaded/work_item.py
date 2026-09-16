"""A fetched work item row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.work_items import WorkItem
from .._kernel.loaded import Loaded, Owned, bind3

if TYPE_CHECKING:
    from ..work_items import WorkItems
    from ..work_items.activities import WorkItemActivities
    from ..work_items.attachments import WorkItemAttachments
    from ..work_items.comments import WorkItemComments
    from ..work_items.dependencies import WorkItemDependencies
    from ..work_items.links import WorkItemLinks
    from ..work_items.relations import WorkItemRelations
    from ..work_items.worklogs import WorkItemWorklogs

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

    class _OwnedAttachments(Owned["WorkItemAttachments"]):
        list = staticmethod(bind3(WorkItemAttachments.list))
        iterate = staticmethod(bind3(WorkItemAttachments.iterate))
        retrieve = staticmethod(bind3(WorkItemAttachments.retrieve))
        create = staticmethod(bind3(WorkItemAttachments.create))
        update = staticmethod(bind3(WorkItemAttachments.update))
        delete = staticmethod(bind3(WorkItemAttachments.delete))

    class _OwnedLinks(Owned["WorkItemLinks"]):
        list = staticmethod(bind3(WorkItemLinks.list))
        iterate = staticmethod(bind3(WorkItemLinks.iterate))
        retrieve = staticmethod(bind3(WorkItemLinks.retrieve))
        create = staticmethod(bind3(WorkItemLinks.create))
        update = staticmethod(bind3(WorkItemLinks.update))
        delete = staticmethod(bind3(WorkItemLinks.delete))

    class _OwnedWorklogs(Owned["WorkItemWorklogs"]):
        list = staticmethod(bind3(WorkItemWorklogs.list))
        iterate = staticmethod(bind3(WorkItemWorklogs.iterate))
        retrieve = staticmethod(bind3(WorkItemWorklogs.retrieve))
        create = staticmethod(bind3(WorkItemWorklogs.create))
        update = staticmethod(bind3(WorkItemWorklogs.update))
        delete = staticmethod(bind3(WorkItemWorklogs.delete))

    class _OwnedActivities(Owned["WorkItemActivities"]):
        list = staticmethod(bind3(WorkItemActivities.list))
        iterate = staticmethod(bind3(WorkItemActivities.iterate))
        retrieve = staticmethod(bind3(WorkItemActivities.retrieve))

    class _OwnedRelations(Owned["WorkItemRelations"]):
        list = staticmethod(bind3(WorkItemRelations.list))
        create = staticmethod(bind3(WorkItemRelations.create))
        delete = staticmethod(bind3(WorkItemRelations.delete))

    class _OwnedDependencies(Owned["WorkItemDependencies"]):
        list = staticmethod(bind3(WorkItemDependencies.list))
        create = staticmethod(bind3(WorkItemDependencies.create))
        delete = staticmethod(bind3(WorkItemDependencies.delete))


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

    @property
    def attachments(self) -> _OwnedAttachments:
        return cast(
            "_OwnedAttachments", Owned(self._resources.attachments, self._ids, self._id_names)
        )

    @property
    def links(self) -> _OwnedLinks:
        return cast("_OwnedLinks", Owned(self._resources.links, self._ids, self._id_names))

    @property
    def worklogs(self) -> _OwnedWorklogs:
        return cast("_OwnedWorklogs", Owned(self._resources.worklogs, self._ids, self._id_names))

    @property
    def activities(self) -> _OwnedActivities:
        return cast(
            "_OwnedActivities", Owned(self._resources.activities, self._ids, self._id_names)
        )

    @property
    def relations(self) -> _OwnedRelations:
        return cast("_OwnedRelations", Owned(self._resources.relations, self._ids, self._id_names))

    @property
    def dependencies(self) -> _OwnedDependencies:
        return cast(
            "_OwnedDependencies", Owned(self._resources.dependencies, self._ids, self._id_names)
        )
