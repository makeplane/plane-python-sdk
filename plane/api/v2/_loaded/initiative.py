"""A fetched initiative row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.initiatives import Initiative
from .._kernel.loaded import Loaded, Owned, bind2

if TYPE_CHECKING:
    from ..initiatives.initiatives import Initiatives
    from ..initiatives.labels import InitiativeLabels
    from ..initiatives.projects import InitiativeProjects
    from ..initiatives.work_items import InitiativeWorkItems

    # Typed views on `Owned`: the child resource's own methods with `slug` and
    # `initiative` already supplied -- `bind2`, because two path ids are bound
    # (initiatives are workspace-scoped, with no project ancestor). Evaluated only
    # by a type checker -- at runtime these properties return a plain `Owned`.

    class _OwnedInitiativeLabels(Owned["InitiativeLabels"]):
        """Only the per-initiative bridge -- `InitiativeLabels`' catalog CRUD
        takes just `slug`, one id short of what this view binds, so it is
        deliberately not exposed here. Reach the catalog through
        `ws.initiatives.labels` directly instead."""

        add = staticmethod(bind2(InitiativeLabels.add))
        remove = staticmethod(bind2(InitiativeLabels.remove))

    class _OwnedInitiativeProjects(Owned["InitiativeProjects"]):
        add = staticmethod(bind2(InitiativeProjects.add))
        remove = staticmethod(bind2(InitiativeProjects.remove))

    class _OwnedInitiativeWorkItems(Owned["InitiativeWorkItems"]):
        add = staticmethod(bind2(InitiativeWorkItems.add))
        remove = staticmethod(bind2(InitiativeWorkItems.remove))


class LoadedInitiative(Loaded, Initiative):
    """An initiative row that is also the place its children live."""

    model_config = {**Initiative.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Initiatives._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Initiatives

    @property
    def labels(self) -> _OwnedInitiativeLabels:
        return cast(
            "_OwnedInitiativeLabels", Owned(self._resources.labels, self._ids, self._id_names)
        )

    @property
    def projects(self) -> _OwnedInitiativeProjects:
        return cast(
            "_OwnedInitiativeProjects", Owned(self._resources.projects, self._ids, self._id_names)
        )

    @property
    def work_items(self) -> _OwnedInitiativeWorkItems:
        return cast(
            "_OwnedInitiativeWorkItems",
            Owned(self._resources.work_items, self._ids, self._id_names),
        )
