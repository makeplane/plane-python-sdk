"""Workspaces (api_v2) -- the root of the flat tree:
`client.v2.workspaces.projects.states.list(slug, project)`."""

from __future__ import annotations

from collections.abc import Sequence

from typing_extensions import Never

from ...models.v2.workspaces import Workspace
from ._generated.constants import WorkspacesRetrieveField
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport
from .features import WorkspaceFeatures
from .projects import Projects
from .releases import Releases
from .wiki_node import Wiki


class Workspaces(V2Resource[Workspace, Never, Never]):
    path = "/workspaces/{slug}/"
    model = Workspace
    operations = {"retrieve": "workspaces_retrieve"}

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.projects = Projects(transport)
        self.wiki = Wiki(transport)
        self.features = WorkspaceFeatures(transport)
        self.releases = Releases(transport)

    def retrieve(
        self, slug: str, *, fields: Sequence[WorkspacesRetrieveField] | None = None
    ) -> Workspace:
        """The workspace detail route has no pk -- the slug is the key -- so this is a
        singleton read, not `_retrieve` (which would append a `None` pk segment)."""
        return self._retrieve_singleton(action="retrieve", params={"fields": fields}, slug=slug)
