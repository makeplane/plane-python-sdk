"""Offline coverage for `ProjectWorklogs`: a read-only endpoint returning a bare JSON array, not a
paginated envelope."""

from __future__ import annotations

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.worklogs import ProjectWorklogs
from plane.config import Configuration

BASE = "https://api.example.com/api/v2"


@pytest.fixture
def worklogs(config: Configuration) -> ProjectWorklogs:
    return ProjectWorklogs(V2Transport(config), slug="acme", project_id="ENG")


@responses.activate
def test_worklogs_summary_parses_bare_array(worklogs: ProjectWorklogs) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/projects/ENG/worklogs/summary/",
        json=[
            {"work_item_id": "wi-1", "duration": 120},
            {"work_item_id": "wi-2", "duration": 45},
        ],
    )

    rows = worklogs.summary()

    assert [row.duration for row in rows] == [120, 45]
    assert rows[0].work_item_id == "wi-1"


@responses.activate
def test_worklogs_summary_empty_project_returns_empty_list(worklogs: ProjectWorklogs) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/projects/ENG/worklogs/summary/",
        json=[],
    )

    assert worklogs.summary() == []
