"""Live coverage for `client.v2.workspaces.audit_logs`. Offline coverage lives in
`tests/v2/test_audit_logs_resource.py`.

Every call here needs `paginate="cursor"`, and until the pagination fix the SDK had
no such parameter -- so this whole file was untestable as well as unreachable. See
`tests/v2/test_pagination_coverage.py`."""

from __future__ import annotations

from typing import Any

import pytest

from plane.api.v2.audit_logs import AuditLogs
from plane.client import PlaneClient


@pytest.fixture
def audit_logs(client: PlaneClient) -> AuditLogs:
    return client.v2.workspaces.audit_logs


class TestAuditLogs:
    """Offset pagination is refused here (`count_pagination_disabled`,
    `AuditLogViewSet.count_styles_enabled=False`) -- every list call in this
    class must pass `paginate="cursor"`."""

    def test_list_reflects_workspace_activity(
        self, audit_logs: AuditLogs, workspace_slug: str, work_item: Any
    ) -> None:
        """Creating a work item (via the `work_item` fixture) is itself an
        audited action -- the list should not be empty afterwards."""
        page = audit_logs.list(workspace_slug, per_page=50, paginate="cursor")
        assert page.data

    def test_retrieve_round_trips_a_listed_entry(
        self, audit_logs: AuditLogs, workspace_slug: str, work_item: Any
    ) -> None:
        first = audit_logs.list(workspace_slug, per_page=1, paginate="cursor").data[0]
        fetched = audit_logs.retrieve(workspace_slug, first.id)
        assert fetched.id == first.id

    def test_category_filter_narrows_results(
        self, audit_logs: AuditLogs, workspace_slug: str
    ) -> None:
        page = audit_logs.list(workspace_slug, category="project", per_page=50, paginate="cursor")
        assert all(row.category == "project" for row in page.data)

    def test_iterate_follows_the_cursor_envelope(
        self, audit_logs: AuditLogs, workspace_slug: str, work_item: Any
    ) -> None:
        """`iterate` needs `paginate` too: without it the auto-pager asks for the offset
        envelope this endpoint refuses, and the traversal 400s on its first request."""
        rows = []
        for row in audit_logs.iterate(workspace_slug, per_page=2, paginate="cursor"):
            rows.append(row)
            if len(rows) >= 5:
                break
        assert rows
        assert len({row.id for row in rows}) == len(rows)
