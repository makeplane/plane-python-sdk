"""Workspace invitations (api_v2). No PATCH; only `list`/`retrieve`/`create`/
`delete` plus `bulk`. Golden documents `bulk`'s 201 as one `WorkspaceInvite`, but
the view returns the whole created list -- this SDK follows the live behavior."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.invitations import (
    BulkCreateWorkspaceInvites,
    CreateWorkspaceInvite,
    WorkspaceInvite,
)
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


class Invitations(V2Resource[WorkspaceInvite, CreateWorkspaceInvite, CreateWorkspaceInvite]):
    path = "/workspaces/{slug}/invitations/"
    model = WorkspaceInvite
    operations = {
        "list": "members_list",
        "retrieve": "members_retrieve",
        "create": "members_create",
        "bulk": "members_bulk",
        "delete": "members_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkspaceInvite]:
        """One page of pending/accepted invitations. `**filters` covers the
        golden's query filters directly, e.g. `accepted=False`, `email="a@b.com"`."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkspaceInvite]:
        """Every invitation, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self,
        invitation_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WorkspaceInvite:
        return self._retrieve(pk=invitation_id, params={"fields": fields})

    def create(self, data: CreateWorkspaceInvite) -> WorkspaceInvite:
        return self._create(data)

    def delete(self, invitation_id: str) -> None:
        return self._delete(pk=invitation_id)

    def bulk(
        self,
        data: BulkCreateWorkspaceInvites,
        *,
        fields: Sequence[str] | None = None,
    ) -> builtins.list[WorkspaceInvite]:
        """Create up to 100 invitations in one call. Emails already invited are
        silently skipped server-side (not re-sent, not errored)."""
        payload = self.transport.request(
            "POST",
            f"{self._collection_url()}bulk/",
            params=self._query({"fields": fields}, action="bulk"),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        rows = payload if isinstance(payload, list) else [payload]
        return [WorkspaceInvite.model_validate(row) for row in rows]
