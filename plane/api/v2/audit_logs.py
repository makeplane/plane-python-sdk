"""Workspace audit logs (api_v2). Read-only, cursor- or offset-paginated."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.audit_logs import AuditLog
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


# No write/patch DTO exists for audit logs -- the type parameters are filled
# with the read model itself as an unused placeholder (see PermissionSchemes).
class AuditLogs(V2Resource[AuditLog, AuditLog, AuditLog]):
    path = "/workspaces/{slug}/audit-logs/"
    model = AuditLog
    operations = {
        "list": "audit_logs_list",
        "retrieve": "audit_logs_retrieve",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[AuditLog]:
        """One page of audit log entries.

        `**filters` covers `actor_id`, `category`, `outcome`, `created_after`, `search`."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[AuditLog]:
        """Every audit log entry, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self,
        log_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> AuditLog:
        return self._retrieve(pk=log_id, params={"fields": fields})
