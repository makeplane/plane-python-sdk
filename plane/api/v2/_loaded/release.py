"""A fetched release row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.releases import Release
from .._kernel.loaded import Loaded, Owned, bind2

if TYPE_CHECKING:
    from ..releases import (
        ReleaseChangelogResource,
        ReleaseComments,
        ReleaseLabels,
        ReleaseLinks,
        Releases,
        ReleaseTags,
        ReleaseWorkItems,
    )

    # Typed views on `Owned`: the child resource's own methods with `slug` and
    # `release` already supplied -- `bind2`, because two path ids are bound
    # (releases are workspace-scoped, with no project ancestor). Evaluated only by
    # a type checker -- at runtime these properties return a plain `Owned`.

    class _OwnedReleaseLabels(Owned["ReleaseLabels"]):
        """Only the per-release bridge -- `ReleaseLabels`' catalog CRUD
        (`list`/`retrieve`/.../`find_by_name`) takes just `slug`, one id short of
        what this view binds, so it is deliberately not exposed here. Reach the
        catalog through `ws.releases.labels` directly instead."""

        add = staticmethod(bind2(ReleaseLabels.add))
        remove = staticmethod(bind2(ReleaseLabels.remove))

    class _OwnedReleaseTags(Owned[ReleaseTags]):
        """`ReleaseTags` has no per-release association at all -- a release points
        at a tag through its own `tag_id` field, not a bridge -- so this view binds
        nothing. It exists so `release.tags` still resolves to the right child
        resource for the loaded-navigation sweep; reach the tag catalog through
        `ws.releases.tags` directly instead."""

    class _OwnedReleaseComments(Owned["ReleaseComments"]):
        list = staticmethod(bind2(ReleaseComments.list))
        iterate = staticmethod(bind2(ReleaseComments.iterate))
        retrieve = staticmethod(bind2(ReleaseComments.retrieve))
        create = staticmethod(bind2(ReleaseComments.create))
        update = staticmethod(bind2(ReleaseComments.update))
        delete = staticmethod(bind2(ReleaseComments.delete))

    class _OwnedReleaseLinks(Owned["ReleaseLinks"]):
        list = staticmethod(bind2(ReleaseLinks.list))
        iterate = staticmethod(bind2(ReleaseLinks.iterate))
        retrieve = staticmethod(bind2(ReleaseLinks.retrieve))
        create = staticmethod(bind2(ReleaseLinks.create))
        update = staticmethod(bind2(ReleaseLinks.update))
        delete = staticmethod(bind2(ReleaseLinks.delete))

    class _OwnedReleaseChangelog(Owned["ReleaseChangelogResource"]):
        retrieve = staticmethod(bind2(ReleaseChangelogResource.retrieve))
        update = staticmethod(bind2(ReleaseChangelogResource.update))

    class _OwnedReleaseWorkItems(Owned["ReleaseWorkItems"]):
        add = staticmethod(bind2(ReleaseWorkItems.add))
        remove = staticmethod(bind2(ReleaseWorkItems.remove))


class LoadedRelease(Loaded, Release):
    """A release row that is also the place its children live."""

    model_config = {**Release.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Releases._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Releases

    @property
    def labels(self) -> _OwnedReleaseLabels:
        return cast("_OwnedReleaseLabels", Owned(self._resources.labels, self._ids, self._id_names))

    @property
    def tags(self) -> _OwnedReleaseTags:
        return cast("_OwnedReleaseTags", Owned(self._resources.tags, self._ids, self._id_names))

    @property
    def comments(self) -> _OwnedReleaseComments:
        return cast(
            "_OwnedReleaseComments", Owned(self._resources.comments, self._ids, self._id_names)
        )

    @property
    def links(self) -> _OwnedReleaseLinks:
        return cast("_OwnedReleaseLinks", Owned(self._resources.links, self._ids, self._id_names))

    @property
    def changelog(self) -> _OwnedReleaseChangelog:
        return cast(
            "_OwnedReleaseChangelog", Owned(self._resources.changelog, self._ids, self._id_names)
        )

    @property
    def work_items(self) -> _OwnedReleaseWorkItems:
        return cast(
            "_OwnedReleaseWorkItems", Owned(self._resources.work_items, self._ids, self._id_names)
        )
