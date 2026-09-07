"""Workspaces (api_v2) -- the root of the flat tree:
`client.v2.workspaces.projects.states.list(slug, project)`."""

from __future__ import annotations

from collections.abc import Sequence

from typing_extensions import Never

from ...models.v2.workspaces import Workspace
from ._generated.constants import WorkspacesRetrieveField
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport
from .projects import Projects


class Workspaces(V2Resource[Workspace, Never, Never]):
    path = "/workspaces/{slug}/"
    model = Workspace
    operations = {"retrieve": "workspaces_retrieve"}

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.projects = Projects(transport)

    def retrieve(
        self, slug: str, *, fields: Sequence[WorkspacesRetrieveField] | None = None
    ) -> Workspace:
        """The workspace detail route has no pk -- the slug is the key -- so this
        goes straight to the transport rather than through `_retrieve` (which would
        append a `None` pk segment)."""
        payload = self.transport.request(
            "GET",
            self.url_for("retrieve", slug=slug),
            params=self._query({"fields": fields}, action="retrieve"),
        )
        return self.model.model_validate(payload)
