"""Release links (api_v2) -- nested under a release. Plain CRUD five: no upsert, no
bulk-* operationIds exist for this shard."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.releases import CreateReleaseLink, ReleaseLink, UpdateReleaseLink
from .._generated.constants import (
    ReleaseLinksCreateField,
    ReleaseLinksListField,
    ReleaseLinksListFilters,
    ReleaseLinksListOrderBy,
    ReleaseLinksPartialUpdateField,
    ReleaseLinksRetrieveField,
)
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
        slug: str,
        release: str,
        *,
        fields: Sequence[ReleaseLinksListField] | None = None,
        order_by: ReleaseLinksListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[ReleaseLinksListFilters],
    ) -> Page[ReleaseLink]:
        """One page of links on a release."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
            release_id=release,
        )

    def iterate(
        self,
        slug: str,
        release: str,
        *,
        fields: Sequence[ReleaseLinksListField] | None = None,
        order_by: ReleaseLinksListOrderBy | None = None,
        **filters: Unpack[ReleaseLinksListFilters],
    ) -> Iterator[ReleaseLink]:
        """Every link on a release, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            release_id=release,
        )

    def retrieve(
        self,
        slug: str,
        release: str,
        link: str,
        *,
        fields: Sequence[ReleaseLinksRetrieveField] | None = None,
    ) -> ReleaseLink:
        return self._retrieve(pk=link, params={"fields": fields}, slug=slug, release_id=release)

    def create(
        self,
        slug: str,
        release: str,
        data: CreateReleaseLink,
        *,
        fields: Sequence[ReleaseLinksCreateField] | None = None,
    ) -> ReleaseLink:
        return self._create(data, params={"fields": fields}, slug=slug, release_id=release)

    def update(
        self,
        slug: str,
        release: str,
        link: str,
        data: UpdateReleaseLink,
        *,
        fields: Sequence[ReleaseLinksPartialUpdateField] | None = None,
    ) -> ReleaseLink:
        return self._update(data, pk=link, params={"fields": fields}, slug=slug, release_id=release)

    def delete(self, slug: str, release: str, link: str) -> None:
        return self._delete(pk=link, slug=slug, release_id=release)
