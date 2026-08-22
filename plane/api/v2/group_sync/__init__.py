"""Group sync (api_v2) -- IdP group -> role/project mapping. `.config` is a
`get`/`update` singleton; `.project_mappings`/`.workspace_mappings` are plain
CRUD (no upsert or bulk)."""

from __future__ import annotations

from typing import Any

from .._kernel.transport import V2Transport
from .config import GroupSyncConfigResource
from .project_mappings import GroupSyncProjectMappings
from .workspace_mappings import GroupSyncWorkspaceMappings

__all__ = [
    "GroupSync",
    "GroupSyncConfigResource",
    "GroupSyncProjectMappings",
    "GroupSyncWorkspaceMappings",
]


class GroupSync:
    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        self.config = GroupSyncConfigResource(transport, **scope)
        self.project_mappings = GroupSyncProjectMappings(transport, **scope)
        self.workspace_mappings = GroupSyncWorkspaceMappings(transport, **scope)
