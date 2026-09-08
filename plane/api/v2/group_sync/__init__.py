"""Group sync (api_v2) -- IdP group -> role/project mapping. `.config` is a
`get`/`update` singleton; `.project_mappings`/`.workspace_mappings` are plain
CRUD (no upsert or bulk)."""

from __future__ import annotations

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
    """Groups `.config`/`.project_mappings`/`.workspace_mappings` under one
    namespace; every method on each still takes its own leading `slug`, same
    as reaching them directly -- this wires no scope of its own."""

    def __init__(self, transport: V2Transport) -> None:
        self.config = GroupSyncConfigResource(transport)
        self.project_mappings = GroupSyncProjectMappings(transport)
        self.workspace_mappings = GroupSyncWorkspaceMappings(transport)
