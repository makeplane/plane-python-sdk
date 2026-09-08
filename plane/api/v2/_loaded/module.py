"""A fetched module row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.modules import Module
from .._kernel.loaded import Loaded, Owned, bind3

if TYPE_CHECKING:
    from ..modules import Modules, ModuleWorkItems

    # Typed view on `Owned`: `ModuleWorkItems`' own methods with `slug`, `project` and
    # `module` already supplied -- `bind3`, because three path ids are bound. Evaluated
    # only by a type checker -- at runtime this property returns a plain `Owned`.

    class _OwnedModuleWorkItems(Owned["ModuleWorkItems"]):
        add = staticmethod(bind3(ModuleWorkItems.add))
        remove = staticmethod(bind3(ModuleWorkItems.remove))


class LoadedModule(Loaded, Module):
    """A module row that is also the place its children live."""

    model_config = {**Module.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Modules._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Modules

    @property
    def work_items(self) -> _OwnedModuleWorkItems:
        return cast(
            "_OwnedModuleWorkItems", Owned(self._resources.work_items, self._ids, self._id_names)
        )
