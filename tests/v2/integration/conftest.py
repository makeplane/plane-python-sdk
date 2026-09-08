"""Fixtures for the live v2 integration suite.

Whether this suite runs at all is decided once, at collection time, by `_guard`
(see its module docstring): with any required env var absent every test is stamped
with the one sanctioned dormant reason, and the fixtures below never run. So they
do *not* skip -- a fixture that can skip is a fixture that can hide a real failure
behind a green `s`, which is exactly how all 385 of these tests came to be dead
while reporting success.
"""

from __future__ import annotations

import os
import random
import re
import string
import time
from collections.abc import Callable, Iterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.projects import CreateProject
from plane.models.v2.work_items import CreateWorkItem

from ._guard import register
from .helpers import SPECS, ResourceSpec, unique_name


def pytest_configure(config: pytest.Config) -> None:
    register(config, Path(__file__).parent)


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
    """`os.environ`, not `os.getenv` + skip: reaching here with the var unset is a
    guard bug, and must read as the error it is rather than as another quiet skip."""
    return os.environ["PLANE_BASE_URL"]


@pytest.fixture(scope="session")
def api_key() -> str:
    return os.environ["PLANE_API_KEY"]


@pytest.fixture(scope="session")
def workspace_slug() -> str:
    return os.environ["WORKSPACE_SLUG"]


@pytest.fixture(scope="session")
def client(base_url: str, api_key: str) -> PlaneClient:
    plane_client = PlaneClient(base_url=base_url, api_key=api_key)
    _install_rate_limit_retry(plane_client.v2.transport)
    return plane_client


@pytest.fixture(scope="session")
def project(client: PlaneClient, workspace_slug: str) -> Iterator[LoadedProject]:
    """Session-shared project seeded with 5 default states and no labels;
    `is_time_tracking_enabled`/`intake_view` are set explicitly -- omitting either
    404s/400s worklog and intake calls elsewhere in this suite (verified live).

    This is the suite's **loaded row**: `Projects.create` answers a `LoadedProject`,
    so every test taking this fixture can navigate straight off it
    (`project.states.list()`) with no ids repeated. It used to hand-roll
    `transport.request`, which meant the one object the whole suite is built around
    never went through the surface under test at all."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    identifier = f"I{_short_suffix()}"  # the server caps identifiers at 10 chars
    projects = client.v2.workspaces.projects
    created = projects.create(
        workspace_slug,
        CreateProject(
            name=f"SDK v2 IT {timestamp}",
            identifier=identifier,
            is_time_tracking_enabled=True,
            intake_view=True,
        ),
    )
    yield created
    try:
        projects.delete(workspace_slug, created.id)
    except Exception:
        pass


@pytest.fixture(scope="session")
def project_id(project: LoadedProject) -> str:
    return str(project.id)


@pytest.fixture(scope="session")
def project_key(project: LoadedProject) -> str:
    return str(project.identifier)


@pytest.fixture(params=sorted(SPECS), ids=sorted(SPECS))
def spec(request: pytest.FixtureRequest) -> ResourceSpec:
    """Parametrizes a test over both `states` and `labels`."""
    return SPECS[request.param]


@pytest.fixture
def work_item(client: PlaneClient, workspace_slug: str, project_id: str) -> Iterator[Any]:
    """Throwaway work item in the shared project; files needing different
    setup define their own, shadowing this one."""
    work_items = client.v2.workspaces.projects.work_items
    created = work_items.create(
        workspace_slug, project_id, CreateWorkItem(name=unique_name("work-item"))
    )
    yield created
    try:
        work_items.delete(workspace_slug, project_id, created.id)
    except Exception:
        pass
