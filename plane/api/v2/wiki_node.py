"""Wiki (api_v2) -- a grouping node, not a resource: it owns workspace-level
wiki children but consumes no path id of its own. `slug` threads straight
through to each child's own methods (`ws.wiki.pages.list(slug)`); this class
never stores or accepts one itself."""

from __future__ import annotations

from ._kernel.transport import V2Transport
from .pages import WikiPages


class Wiki:
    """Groups the workspace-level wiki resources. Consumes no path id of its own.

    `.collections` (wiki collections) is deliberately not wired here: `Collections`
    (`plane/api/v2/collections/__init__.py`) still uses the retired bound-scope
    constructor (`__init__(self, transport, **scope)` reading `self._scope`, which
    no `V2Resource` sets any more) -- constructing it eagerly here would raise for
    every `V2Namespace(...)`, not just wiki-collection callers. Wire it once that
    class is migrated to the flat form; see the Task 11 report."""

    def __init__(self, transport: V2Transport) -> None:
        self.pages = WikiPages(transport)
