"""A fetched agent run row that is also the place its activities live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.agent_runs import AgentRun
from .._kernel.loaded import Loaded, Owned, bind2

if TYPE_CHECKING:
    from ..agent_runs import AgentRunActivities, AgentRuns

    # Typed view on `Owned`: `AgentRunActivities`' own methods with `slug` and `run`
    # already supplied -- `bind2`, because two path ids are bound. Evaluated only by a
    # type checker -- at runtime the property returns a plain `Owned`.

    class _OwnedAgentRunActivities(Owned["AgentRunActivities"]):
        list = staticmethod(bind2(AgentRunActivities.list))
        iterate = staticmethod(bind2(AgentRunActivities.iterate))
        retrieve = staticmethod(bind2(AgentRunActivities.retrieve))
        create = staticmethod(bind2(AgentRunActivities.create))


class LoadedAgentRun(Loaded, AgentRun):
    """An agent run row that is also the place its activities live."""

    model_config = {**AgentRun.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `AgentRuns._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: AgentRuns

    @property
    def activities(self) -> _OwnedAgentRunActivities:
        return cast(
            "_OwnedAgentRunActivities",
            Owned(self._resources.activities, self._ids, self._id_names),
        )
