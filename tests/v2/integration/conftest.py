"""Fixtures for the live v2 integration suite; every fixture skips (never fails)
when its required env var is absent, so tests collect cleanly with no credentials."""

from __future__ import annotations

import os
import random
import re
import string
import time
from collections.abc import Callable, Iterator
from datetime import datetime, timezone
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.work_items import CreateWorkItem

from .helpers import SPECS, ResourceSpec, unique_name

_RETRY_AFTER_RE = re.compile(r"(\d+(?:\.\d+)?)\s*seconds?", re.IGNORECASE)


def _short_suffix(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def _install_rate_limit_retry(transport: Any, max_attempts: int = 8) -> None:
    """Retries every request on HTTP 429, sleeping for the server's own
    Retry-After hint (falls back to 15s) -- the API key's free-plan rate
    limit is otherwise exceeded within seconds by this suite's volume."""
    original_request: Callable[..., Any] = transport.request

    def request_with_retry(*args: Any, **kwargs: Any) -> Any:
        for attempt in range(max_attempts):
            try:
                return original_request(*args, **kwargs)
            except PlaneAPIError as exc:
                if exc.status != 429 or attempt == max_attempts - 1:
                    raise
                match = _RETRY_AFTER_RE.search(exc.detail or "")
                delay = float(match.group(1)) + 1.0 if match else 15.0
                time.sleep(delay)
        raise AssertionError("unreachable")  # pragma: no cover

    transport.request = request_with_retry


@pytest.fixture(scope="session")
def base_url() -> str:
    value = os.getenv("PLANE_BASE_URL")
    if not value:
        pytest.skip("PLANE_BASE_URL not set; skipping live v2 integration tests")
    return value


@pytest.fixture(scope="session")
def api_key() -> str:
    value = os.getenv("PLANE_API_KEY")
    if not value:
        pytest.skip("PLANE_API_KEY not set; skipping live v2 integration tests")
    return value


@pytest.fixture(scope="session")
def workspace_slug() -> str:
    value = os.getenv("WORKSPACE_SLUG")
    if not value:
        pytest.skip("WORKSPACE_SLUG not set; skipping live v2 integration tests")
    return value


@pytest.fixture(scope="session")
def client(base_url: str, api_key: str) -> PlaneClient:
    plane_client = PlaneClient(base_url=base_url, api_key=api_key)
    _install_rate_limit_retry(plane_client.v2.transport)
    return plane_client


@pytest.fixture(scope="session")
def project(client: PlaneClient, workspace_slug: str) -> Iterator[dict[str, Any]]:
    """Session-shared project seeded with 5 default states and no labels;
    `is_time_tracking_enabled`/`intake_view` are set explicitly -- omitting either
    404s/400s worklog and intake calls elsewhere in this suite (verified live)."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    identifier = f"I{_short_suffix()}"  # the server caps identifiers at 10 chars
    payload = {
        "name": f"SDK v2 IT {timestamp}",
        "identifier": identifier,
        "is_time_tracking_enabled": True,
        "intake_view": True,
    }
    created: dict[str, Any] = client.v2.transport.request(
        "POST", f"/workspaces/{workspace_slug}/projects/", json=payload
    )
    yield created
    try:
        client.v2.transport.request(
            "DELETE", f"/workspaces/{workspace_slug}/projects/{created['id']}/"
        )
    except Exception:
        pass


@pytest.fixture(scope="session")
def project_id(project: dict[str, Any]) -> str:
    return str(project["id"])


@pytest.fixture(scope="session")
def project_key(project: dict[str, Any]) -> str:
    return str(project["identifier"])


@pytest.fixture(params=sorted(SPECS), ids=sorted(SPECS))
def spec(request: pytest.FixtureRequest) -> ResourceSpec:
    """Parametrizes a test over both `states` and `labels`."""
    return SPECS[request.param]


@pytest.fixture
def work_item(client: PlaneClient, workspace_slug: str, project_id: str) -> Iterator[Any]:
    """Throwaway work item in the shared project; files needing different
    setup define their own, shadowing this one."""
    work_items = client.v2.workspace(workspace_slug).project(project_id).work_items
    created = work_items.create(CreateWorkItem(name=unique_name("work-item")))
    yield created
    try:
        work_items.delete(created.id)
    except Exception:
        pass
