"""`Wiki` -- the workspace's wiki container: pages and collections.
Constructing it makes no request."""

from __future__ import annotations

from ._kernel.transport import V2Transport
from .collections import Collections
from .pages import WikiPages


class Wiki:
    """A workspace's wiki, bound to `slug`. Makes no request to construct."""

    def __init__(self, transport: V2Transport, slug: str) -> None:
        self.transport = transport
        self.slug = slug
        self.pages = WikiPages(transport, slug=slug)
        self.collections = Collections(transport, slug=slug)
