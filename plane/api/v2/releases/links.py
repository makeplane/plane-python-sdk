"""Release links (api_v2) -- nested under a release."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.releases import CreateReleaseLink, ReleaseLink, UpdateReleaseLink
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class ReleaseLinks(V2Resource[ReleaseLink, CreateReleaseLink, UpdateReleaseLink]):
    path = "/workspaces/{slug}/releases/{release_id}/links/"
    model = ReleaseLink
    operations = {
        "list": "release_links_list",
        "retrieve": "release_links_retrieve",
        "create": "release_links_create",
        "update": "release_links_partial_update",
        "delete": "release_links_destroy",
    }

    def list(
        self,
        release_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[ReleaseLink]:
        """One page of links on a release."""
        return self._list(release_id=release_id, params={"fields": fields, **filters})

    def iterate(
        self,
        release_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[ReleaseLink]:
        """Every link on a release, following pages automatically."""
        return self._iter(release_id=release_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        release_id: str,
        link_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> ReleaseLink:
        return self._retrieve(pk=link_id, release_id=release_id, params={"fields": fields})

    def create(self, release_id: str, data: CreateReleaseLink) -> ReleaseLink:
        return self._create(data, release_id=release_id)

    def update(self, release_id: str, link_id: str, data: UpdateReleaseLink) -> ReleaseLink:
        return self._update(data, pk=link_id, release_id=release_id)

    def delete(self, release_id: str, link_id: str) -> None:
        return self._delete(pk=link_id, release_id=release_id)
