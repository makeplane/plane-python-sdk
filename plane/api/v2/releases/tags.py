"""Release tag catalog (api_v2). Workspace-level catalog of release tags.
**Golden/server mismatch (confirmed live):** golden implies `tag_id` accepts
`version:<value>`; it 404s -- resolve via `find_by_version` first."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.releases import CreateReleaseTag, ReleaseTag, UpdateReleaseTag
from .._kernel.pagination import Page
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
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[ReleaseTag]:
        """One page of the workspace's release-tag catalog."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[ReleaseTag]:
        """Every release tag in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, tag_id: str, *, fields: Sequence[str] | None = None) -> ReleaseTag:
        """`tag_id` is the tag's UUID -- see the module docstring for why a
        `version:<value>` form is not accepted despite the golden's summary
        implying it is."""
        return self._retrieve(pk=tag_id, params={"fields": fields})

    def find_by_version(self, version: str) -> ReleaseTag:
        """The one release tag with this version; raises if none or several
        match. The way to resolve a version to an id -- see the module
        docstring on why `retrieve(f"version:{v}")` is not."""
        return self._find_one(filters={"version": version})

    def create(self, data: CreateReleaseTag) -> ReleaseTag:
        return self._create(data)

    def update(self, tag_id: str, data: UpdateReleaseTag) -> ReleaseTag:
        """`tag_id` is the tag's UUID -- see the module docstring."""
        return self._update(data, pk=tag_id)

    def delete(self, tag_id: str) -> None:
        """`tag_id` is the tag's UUID -- see the module docstring."""
        return self._delete(pk=tag_id)
