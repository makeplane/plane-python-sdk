"""A fetched collection row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.collections import Collection
from .._kernel.loaded import Loaded, Owned, bind2

if TYPE_CHECKING:
    from ..collections import CollectionMembers, CollectionPages, Collections

    # Typed views on `Owned`: the child resource's own methods with `slug` and
    # `collection` already supplied -- `bind2`, because two path ids are bound.
    # Evaluated only by a type checker -- at runtime these properties return a
    # plain `Owned`.

    class _OwnedCollectionMembers(Owned["CollectionMembers"]):
        list = staticmethod(bind2(CollectionMembers.list))
        add = staticmethod(bind2(CollectionMembers.add))
        remove = staticmethod(bind2(CollectionMembers.remove))

    class _OwnedCollectionPages(Owned["CollectionPages"]):
        add = staticmethod(bind2(CollectionPages.add))
        remove = staticmethod(bind2(CollectionPages.remove))
        search = staticmethod(bind2(CollectionPages.search))


class LoadedCollection(Loaded, Collection):
    """A collection row that is also the place its children live."""

    model_config = {**Collection.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Collections._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Collections

    @property
    def members(self) -> _OwnedCollectionMembers:
        return cast(
            "_OwnedCollectionMembers", Owned(self._resources.members, self._ids, self._id_names)
        )

    @property
    def pages(self) -> _OwnedCollectionPages:
        return cast(
            "_OwnedCollectionPages", Owned(self._resources.pages, self._ids, self._id_names)
        )
