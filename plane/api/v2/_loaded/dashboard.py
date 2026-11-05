"""A fetched dashboard row that is also the place its widgets live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.dashboards import Dashboard
from .._kernel.loaded import Loaded, Owned, bind2

if TYPE_CHECKING:
    from ..dashboards import Dashboards, Widgets

    # Typed view on `Owned`: `Widgets`' own methods with `slug` and `dashboard` already
    # supplied -- `bind2`, because two path ids are bound. Evaluated only by a type
    # checker -- at runtime the property returns a plain `Owned`.

    class _OwnedWidgets(Owned["Widgets"]):
        list = staticmethod(bind2(Widgets.list))
        iterate = staticmethod(bind2(Widgets.iterate))
        retrieve = staticmethod(bind2(Widgets.retrieve))
        create = staticmethod(bind2(Widgets.create))
        update = staticmethod(bind2(Widgets.update))
        delete = staticmethod(bind2(Widgets.delete))
        chart = staticmethod(bind2(Widgets.chart))
        charts = staticmethod(bind2(Widgets.charts))


class LoadedDashboard(Loaded, Dashboard):
    """A dashboard row that is also the place its widgets live."""

    model_config = {**Dashboard.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Dashboards._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Dashboards

    @property
    def widgets(self) -> _OwnedWidgets:
        return cast("_OwnedWidgets", Owned(self._resources.widgets, self._ids, self._id_names))
