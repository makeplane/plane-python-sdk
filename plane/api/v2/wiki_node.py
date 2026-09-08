"""Wiki (api_v2) -- a grouping node, not a resource: it owns workspace-level
wiki children but consumes no path id of its own. `slug` threads straight
through to each child's own methods (`ws.wiki.pages.list(slug)`); this class
never stores or accepts one itself."""

from __future__ import annotations

from ._kernel.transport import V2Transport
from .collections import Collections
from .pages import WikiPages


class Wiki:
    """Groups the workspace-level wiki resources. Consumes no path id of its own.

    `.collections` (wiki collections, plus their `.members` and `.pages` children)
    was a `PendingMigration` placeholder for two plans -- present so the attribute
    did not read like a typo, but raising `NotImplementedError` on use, because
    `Collections` still took a bound scope its callers could not supply. It is the
    real resource now, and nothing on the tree is a placeholder any more."""

    def __init__(self, transport: V2Transport) -> None:
        self.pages = WikiPages(transport)
        self.collections = Collections(transport)
