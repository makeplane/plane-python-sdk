"""Release comments (api_v2) -- nested under a release. Plain CRUD five only: no
upsert, no bulk-* operationIds exist for this shard (unlike work-item comments)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.releases import CreateReleaseComment, ReleaseComment, UpdateReleaseComment
from .._generated.constants import (
    ReleaseCommentsCreateField,
    ReleaseCommentsListField,
    ReleaseCommentsListFilters,
    ReleaseCommentsListOrderBy,
    ReleaseCommentsPartialUpdateField,
    ReleaseCommentsRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource


class ReleaseComments(V2Resource[ReleaseComment, CreateReleaseComment, UpdateReleaseComment]):
    path = "/workspaces/{slug}/releases/{release_id}/comments/"
    model = ReleaseComment
    operations = {
        "list": "release_comments_list",
        "retrieve": "release_comments_retrieve",
        "create": "release_comments_create",
        "update": "release_comments_partial_update",
        "delete": "release_comments_destroy",
    }

    def list(
        self,
        slug: str,
        release: str,
        *,
        fields: Sequence[ReleaseCommentsListField] | None = None,
        order_by: ReleaseCommentsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[ReleaseCommentsListFilters],
    ) -> Page[ReleaseComment]:
        """One page of comments on a release."""
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
            release_id=release,
        )

    def iterate(
        self,
        slug: str,
        release: str,
        *,
        fields: Sequence[ReleaseCommentsListField] | None = None,
        order_by: ReleaseCommentsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[ReleaseCommentsListFilters],
    ) -> Iterator[ReleaseComment]:
        """Every comment on a release, following pages automatically."""
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
            release_id=release,
        )

    def retrieve(
        self,
        slug: str,
        release: str,
        comment: str,
        *,
        fields: Sequence[ReleaseCommentsRetrieveField] | None = None,
    ) -> ReleaseComment:
        return self._retrieve(pk=comment, params={"fields": fields}, slug=slug, release_id=release)

    def create(
        self,
        slug: str,
        release: str,
        data: CreateReleaseComment,
        *,
        fields: Sequence[ReleaseCommentsCreateField] | None = None,
    ) -> ReleaseComment:
        return self._create(data, params={"fields": fields}, slug=slug, release_id=release)

    def update(
        self,
        slug: str,
        release: str,
        comment: str,
        data: UpdateReleaseComment,
        *,
        fields: Sequence[ReleaseCommentsPartialUpdateField] | None = None,
    ) -> ReleaseComment:
        return self._update(
            data, pk=comment, params={"fields": fields}, slug=slug, release_id=release
        )

    def delete(self, slug: str, release: str, comment: str) -> None:
        return self._delete(pk=comment, slug=slug, release_id=release)
