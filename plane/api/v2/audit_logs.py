"""Workspace audit logs (api_v2). Read-only, and **cursor-paginated only**.

`AuditLogViewSet.count_styles_enabled` is `False` server-side, so the default offset
envelope is refused with `count_pagination_disabled`: every call here must pass
`paginate="cursor"`, and `order_by` must be a cursor-eligible column (`created_at`
or `id` -- the two the golden offers). Until `paginate` existed on the methods
(see `tests/v2/test_pagination_coverage.py`) this resource could not be listed at
all."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.audit_logs import AuditLog
from ._generated.constants import (
    AuditLogsListField,
    AuditLogsListFilters,
    AuditLogsListOrderBy,
    AuditLogsRetrieveField,
)
from ._kernel.pagination import Page, PaginateStyle
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
        slug: str,
        *,
        fields: Sequence[AuditLogsListField] | None = None,
        order_by: AuditLogsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[AuditLogsListFilters],
    ) -> Page[AuditLog]:
        """One page of audit log entries. Pass `paginate="cursor"` -- see the module
        docstring; the offset envelope this defaults to is refused by the server.

        `**filters` covers `actor_id`, `category`, `outcome`, `created_after`, `search`."""
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
        fields: Sequence[AuditLogsListField] | None = None,
        order_by: AuditLogsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[AuditLogsListFilters],
    ) -> Iterator[AuditLog]:
        """Every audit log entry, following pages automatically. Pass
        `paginate="cursor"` and a cursor-eligible `order_by` -- see the module
        docstring."""
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
        self,
        slug: str,
        log: str,
        *,
        fields: Sequence[AuditLogsRetrieveField] | None = None,
    ) -> AuditLog:
        return self._retrieve(pk=log, params={"fields": fields}, slug=slug)
