"""Initiative projects (api_v2) -- membership bridge between an initiative and
projects."""

from __future__ import annotations

import builtins
from collections.abc import Sequence

from ....models.v2.initiatives import InitiativeChildManageRequest, InitiativeChildManageResponse
from .._kernel.resource import V2Resource

__all__ = ["InitiativeProjects"]


class InitiativeProjects(
    V2Resource[
        InitiativeChildManageResponse, InitiativeChildManageRequest, InitiativeChildManageRequest
    ]
):
    """Membership bridge between an initiative and projects: `add` attaches
    projects to the initiative, `remove` detaches them. Both POST to
    `.../initiatives/{initiative_id}/projects/` and return the ids actually
    changed."""

    path = "/workspaces/{slug}/initiatives/{initiative_id}/projects/"
    model = InitiativeChildManageResponse
    operations = {
        "bridge": "initiatives_projects",
    }

    def add(self, initiative_id: str, project_ids: Sequence[str]) -> builtins.list[str]:
        """Attach 1..100 projects to this initiative; returns the ids actually
        added (already-attached ones are omitted)."""
        return self._bridge(key="add", ids=project_ids, initiative_id=initiative_id)

    def remove(self, initiative_id: str, project_ids: Sequence[str]) -> builtins.list[str]:
        """Detach 1..100 projects from this initiative; returns the ids
        actually removed."""
        return self._bridge(key="remove", ids=project_ids, initiative_id=initiative_id)
