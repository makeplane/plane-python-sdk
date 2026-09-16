"""Release tag catalog (api_v2). Workspace-level catalog of release tags.
**Golden/server mismatch (confirmed live):** golden implies `tag` accepts
`version:<value>`; it 404s -- resolve via `find_by_version` first."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.releases import CreateReleaseTag, ReleaseTag, UpdateReleaseTag
from .._generated.constants import (
    ReleaseTagsCreateField,
    ReleaseTagsListField,
    ReleaseTagsListFilters,
    ReleaseTagsListOrderBy,
    ReleaseTagsPartialUpdateField,
    ReleaseTagsRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource


class ReleaseTags(V2Resource[ReleaseTag, CreateReleaseTag, UpdateReleaseTag]):
    path = "/workspaces/{slug}/releases/tags/"
    model = ReleaseTag
    operations = {
        "list": "release_tags_list",
        "retrieve": "release_tags_retrieve",
        "create": "release_tags_create",
        "update": "release_tags_partial_update",
        "delete": "release_tags_destroy",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[ReleaseTagsListField] | None = None,
        order_by: ReleaseTagsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[ReleaseTagsListFilters],
    ) -> Page[ReleaseTag]:
        """One page of the workspace's release-tag catalog."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[ReleaseTagsListField] | None = None,
        order_by: ReleaseTagsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[ReleaseTagsListFilters],
    ) -> Iterator[ReleaseTag]:
        """Every release tag in the workspace, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )

    def retrieve(
        self, slug: str, tag: str, *, fields: Sequence[ReleaseTagsRetrieveField] | None = None
    ) -> ReleaseTag:
        """`tag` is the tag's UUID -- see the module docstring for why a
        `version:<value>` form is not accepted despite the golden's summary
        implying it is."""
        return self._retrieve(pk=tag, params={"fields": fields}, slug=slug)

    def find_by_version(self, slug: str, version: str) -> ReleaseTag:
        """The one release tag with this version; raises if none or several
        match. The way to resolve a version to an id -- see the module
        docstring on why `retrieve(f"version:{v}")` is not."""
        return self._find_one(filters={"version": version}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateReleaseTag,
        *,
        fields: Sequence[ReleaseTagsCreateField] | None = None,
    ) -> ReleaseTag:
        return self._create(data, params={"fields": fields}, slug=slug)

    def update(
        self,
        slug: str,
        tag: str,
        data: UpdateReleaseTag,
        *,
        fields: Sequence[ReleaseTagsPartialUpdateField] | None = None,
    ) -> ReleaseTag:
        """`tag` is the tag's UUID -- see the module docstring."""
        return self._update(data, pk=tag, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, tag: str) -> None:
        """`tag` is the tag's UUID -- see the module docstring."""
        return self._delete(pk=tag, slug=slug)
