"""Live coverage for `ws.audit_logs`, reached through the chain
(`client.v2.workspace(slug).audit_logs`). Offline coverage lives in
`tests/v2/test_audit_logs_resource.py`."""

from __future__ import annotations

from typing import Any

import pytest

from plane.api.v2.audit_logs import AuditLogs
from plane.client import PlaneClient


@pytest.fixture
def audit_logs(client: PlaneClient, workspace_slug: str) -> AuditLogs:
    return client.v2.workspace(workspace_slug).audit_logs


class TestAuditLogs:
    """Offset pagination is refused here (`count_pagination_disabled`,
    `AuditLogViewSet.count_styles_enabled=False`) -- every list call in this
    class must pass `paginate="cursor"`."""

    def test_list_reflects_workspace_activity(self, audit_logs: AuditLogs, work_item: Any) -> None:
        """Creating a work item (via the `work_item` fixture) is itself an
        audited action -- the list should not be empty afterwards."""
        page = audit_logs.list(per_page=50, paginate="cursor")
        assert page.data

    def test_retrieve_round_trips_a_listed_entry(
        self, audit_logs: AuditLogs, work_item: Any
    ) -> None:
        first = audit_logs.list(per_page=1, paginate="cursor").data[0]
        fetched = audit_logs.retrieve(first.id)
        assert fetched.id == first.id

    def test_category_filter_narrows_results(self, audit_logs: AuditLogs) -> None:
        page = audit_logs.list(category="project", per_page=50, paginate="cursor")
        assert all(row.category == "project" for row in page.data)
