"""Shared pytest fixtures for API unit tests."""

import os
from datetime import datetime

import pytest

from plane.client import PlaneClient
from plane.models.projects import CreateProject, Project


@pytest.fixture(scope="session")
def base_url() -> str:
    """Get base URL from environment variable."""
    url = os.getenv("PLANE_BASE_URL")
    if not url:
        pytest.skip("PLANE_BASE_URL environment variable not set")
    return url


@pytest.fixture(scope="session")
def api_key() -> str | None:
    """Get API key from environment variable."""
    return os.getenv("PLANE_API_KEY")


@pytest.fixture(scope="session")
def access_token() -> str | None:
    """Get access token from environment variable."""
    return os.getenv("PLANE_ACCESS_TOKEN")


@pytest.fixture(scope="session")
def workspace_slug() -> str:
    """Get workspace slug from environment variable."""
    slug = os.getenv("WORKSPACE_SLUG")
    if not slug:
        pytest.skip("WORKSPACE_SLUG environment variable not set")
    return slug


@pytest.fixture(scope="session")
def client(base_url: str, api_key: str | None, access_token: str | None) -> PlaneClient:
    """Create and return a configured PlaneClient instance."""
    if not api_key and not access_token:
        pytest.skip("Either PLANE_API_KEY or PLANE_ACCESS_TOKEN environment variable must be set")

    return PlaneClient(
        base_url=base_url,
        api_key=api_key,
        access_token=access_token,
    )


@pytest.fixture(scope="session")
def user_id(client: PlaneClient) -> str:
    """Get current user ID (cached for entire test session)."""
    user = client.users.get_me()
    return user.id


@pytest.fixture(scope="session")
def project(client: PlaneClient, workspace_slug: str) -> Project:
    """Create a shared test project for the module and clean up after all tests."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    project_data = CreateProject(
        name=f"Test Project {timestamp}",
        identifier=f"TP{timestamp[-8:]}",
    )
    project = client.projects.create(workspace_slug, project_data)
    yield project
    try:
        client.projects.delete(workspace_slug, project.id)
    except Exception:
        pass
