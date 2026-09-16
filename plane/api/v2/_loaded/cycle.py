"""A fetched cycle row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.cycles import Cycle
from .._kernel.loaded import Loaded, Owned, bind3

if TYPE_CHECKING:
    from ..cycles import Cycles, CycleWorkItems

    # Typed view on `Owned`: `CycleWorkItems`' own methods with `slug`, `project` and
    # `cycle` already supplied -- `bind3`, because three path ids are bound. Evaluated
    # only by a type checker -- at runtime this property returns a plain `Owned`.

    class _OwnedCycleWorkItems(Owned["CycleWorkItems"]):
        add = staticmethod(bind3(CycleWorkItems.add))
        remove = staticmethod(bind3(CycleWorkItems.remove))


class LoadedCycle(Loaded, Cycle):
    """A cycle row that is also the place its children live."""

    model_config = {**Cycle.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Cycles._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Cycles

    @property
    def work_items(self) -> _OwnedCycleWorkItems:
        return cast(
            "_OwnedCycleWorkItems", Owned(self._resources.work_items, self._ids, self._id_names)
        )
