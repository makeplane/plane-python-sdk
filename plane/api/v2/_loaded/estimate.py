"""A fetched estimate row that is also the place its points live.

`Estimate.points` is itself a real API field -- inline point data the server
returns when the caller passes `expand=["points"]` -- so the navigation
property here cannot be named `points` without shadowing it; it is
`estimate_points` instead."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.estimates import Estimate
from .._kernel.loaded import Loaded, Owned, bind3

if TYPE_CHECKING:
    from ..estimates import Estimates
    from ..estimates.points import EstimatePoints

    # Typed view on `Owned`: `EstimatePoints`' own methods with `slug`, `project` and
    # `estimate` already supplied -- `bind3`, because three path ids are bound.
    # Evaluated only by a type checker -- at runtime this property returns a plain
    # `Owned`.

    class _OwnedEstimatePoints(Owned["EstimatePoints"]):
        list = staticmethod(bind3(EstimatePoints.list))
        iterate = staticmethod(bind3(EstimatePoints.iterate))
        retrieve = staticmethod(bind3(EstimatePoints.retrieve))
        find_by_key = staticmethod(bind3(EstimatePoints.find_by_key))
        create = staticmethod(bind3(EstimatePoints.create))
        update = staticmethod(bind3(EstimatePoints.update))
        delete = staticmethod(bind3(EstimatePoints.delete))
        upsert = staticmethod(bind3(EstimatePoints.upsert))
        bulk_create = staticmethod(bind3(EstimatePoints.bulk_create))
        bulk_update = staticmethod(bind3(EstimatePoints.bulk_update))
        bulk_delete = staticmethod(bind3(EstimatePoints.bulk_delete))


class LoadedEstimate(Loaded, Estimate):
    """An estimate row that is also the place its points live."""

    model_config = {**Estimate.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Estimates._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Estimates

    @property
    def estimate_points(self) -> _OwnedEstimatePoints:
        """Navigable access to this estimate's points -- not named `points`,
        which is the row's own inline-expand field (see the module docstring)."""
        return cast(
            "_OwnedEstimatePoints", Owned(self._resources.points, self._ids, self._id_names)
        )
