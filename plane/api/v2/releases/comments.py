"""Release comments (api_v2) -- nested under a release."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.releases import CreateReleaseComment, ReleaseComment, UpdateReleaseComment
from .._kernel.pagination import Page
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
        release_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[ReleaseComment]:
        """One page of comments on a release."""
        return self._list(release_id=release_id, params={"fields": fields, **filters})

    def iterate(
        self,
        release_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[ReleaseComment]:
        """Every comment on a release, following pages automatically."""
        return self._iter(release_id=release_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        release_id: str,
        comment_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> ReleaseComment:
        return self._retrieve(pk=comment_id, release_id=release_id, params={"fields": fields})

    def create(self, release_id: str, data: CreateReleaseComment) -> ReleaseComment:
        return self._create(data, release_id=release_id)

    def update(
        self,
        release_id: str,
        comment_id: str,
        data: UpdateReleaseComment,
    ) -> ReleaseComment:
        return self._update(data, pk=comment_id, release_id=release_id)

    def delete(self, release_id: str, comment_id: str) -> None:
        return self._delete(pk=comment_id, release_id=release_id)
