"""Wiki (api_v2) -- a grouping node, not a resource: it owns workspace-level
wiki children but consumes no path id of its own. `slug` threads straight
through to each child's own methods (`ws.wiki.pages.list(slug)`); this class
never stores or accepts one itself."""

from __future__ import annotations

from ._kernel.pending import PendingMigration
from ._kernel.transport import V2Transport
from .pages import WikiPages


class Wiki:
    """Groups the workspace-level wiki resources. Consumes no path id of its own.

    `.collections` (wiki collections) is a placeholder: `Collections`
    (`plane/api/v2/collections/__init__.py`) still uses the retired bound-scope
    constructor (`__init__(self, transport, **scope)` reading `self._scope`, which
    no `V2Resource` sets any more), so constructing it eagerly would raise for every
    `V2Namespace(...)`, not just wiki-collection callers. Leaving the attribute off
    entirely gave a bare `AttributeError` that read like a typo, so it is wired to a
    `PendingMigration` that names the resource instead. Replace it with the real
    class once `Collections` is migrated to the flat form."""

    def __init__(self, transport: V2Transport) -> None:
        self.pages = WikiPages(transport)
        self.collections = PendingMigration("Collections", reached_as="wiki.collections")
