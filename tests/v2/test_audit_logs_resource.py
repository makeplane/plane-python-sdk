"""Offline coverage for `ws.audit_logs`: filtered list, cursor pagination, retrieve, and rejection
of an unknown `order_by`."""

from __future__ import annotations

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.audit_logs import AuditLogs
from plane.config import Configuration

BASE = "https://api.example.com/api/v2"


@pytest.fixture
def audit_logs(config: Configuration) -> AuditLogs:
    return AuditLogs(V2Transport(config), slug="acme")


@responses.activate
def test_audit_logs_list_with_filters(audit_logs: AuditLogs) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/audit-logs/",
        json={
            "data": [
                {"id": "a1", "category": "member", "outcome": "success", "actor_type": "user"}
            ],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = audit_logs.list(category="member", outcome="success")

    assert page.data[0].outcome == "success"
    sent_url = responses.calls[0].request.url
    assert sent_url is not None
    assert "category=member" in sent_url
    assert "outcome=success" in sent_url


@responses.activate
def test_audit_logs_cursor_page(audit_logs: AuditLogs) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/audit-logs/",
        json={
            "data": [{"id": "a1"}],
            "pagination": {"style": "cursor"},
            "has_more": False,
            "next_cursor": None,
        },
    )

    page = audit_logs.list(paginate="cursor")

    assert page.has_more is False


@responses.activate
def test_audit_logs_retrieve(audit_logs: AuditLogs) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/audit-logs/a1/",
        json={"id": "a1", "event_name": "member.invited"},
    )

    entry = audit_logs.retrieve("a1")

    assert entry.event_name == "member.invited"


def test_audit_logs_unknown_order_by_rejected(audit_logs: AuditLogs) -> None:
    """`order_by` is a closed enum for `audit_logs_list` -- negative assertion,
    proven capable of failing below."""
    with pytest.raises(ValueError, match="Unknown order_by"):
        audit_logs.list(order_by="-not_a_real_column")
