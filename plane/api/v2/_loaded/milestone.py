"""A fetched milestone row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.milestones import Milestone
from .._kernel.loaded import Loaded, Owned, bind3

if TYPE_CHECKING:
    from ..milestones import Milestones, MilestoneWorkItems

    # Typed view on `Owned`: `MilestoneWorkItems`' own methods with `slug`, `project`
    # and `milestone` already supplied -- `bind3`, because three path ids are bound.
    # Evaluated only by a type checker -- at runtime this property returns a plain
    # `Owned`.

    class _OwnedMilestoneWorkItems(Owned["MilestoneWorkItems"]):
        add = staticmethod(bind3(MilestoneWorkItems.add))
        remove = staticmethod(bind3(MilestoneWorkItems.remove))


class LoadedMilestone(Loaded, Milestone):
    """A milestone row that is also the place its children live."""

    model_config = {**Milestone.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Milestones._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Milestones

    @property
    def work_items(self) -> _OwnedMilestoneWorkItems:
        return cast(
            "_OwnedMilestoneWorkItems",
            Owned(self._resources.work_items, self._ids, self._id_names),
        )
