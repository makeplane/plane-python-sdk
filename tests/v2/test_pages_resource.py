"""Offline coverage for `ProjectPages`/`WikiPages`; pins that each variant hits its own distinct
URL despite sharing `Page`/`CreatePage`/`UpdatePage`."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.pages import ProjectPages, WikiPages
from plane.config import Configuration
from plane.models.v2.pages import CreatePage, UpdatePage

PROJECT_BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/pages"
WORKSPACE_BASE = "https://api.example.com/api/v2/workspaces/acme/pages"


@pytest.fixture
def project_pages(config: Configuration) -> ProjectPages:
    return ProjectPages(V2Transport(config), slug="acme", project_id="ENG")


@pytest.fixture
def workspace_pages(config: Configuration) -> WikiPages:
    return WikiPages(V2Transport(config), slug="acme")


# -- ProjectPages ------------------------------------------------------------------


@responses.activate
def test_project_pages_list(project_pages: ProjectPages) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "p1", "name": "Runbook"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = project_pages.list()

    assert page.total_count == 1
    assert page.data[0].name == "Runbook"


@responses.activate
def test_project_pages_list_passes_expand(project_pages: ProjectPages) -> None:
    responses.get(f"{PROJECT_BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    project_pages.list(expand=["owned_by", "parent"])

    assert "expand=owned_by%2Cparent" in responses.calls[0].request.url


def test_project_pages_list_rejects_unknown_expand(project_pages: ProjectPages) -> None:
    with pytest.raises(ValueError, match="bogus"):
        project_pages.list(expand=["bogus"])


@responses.activate
def test_project_pages_retrieve(project_pages: ProjectPages) -> None:
    responses.get(f"{PROJECT_BASE}/p1/", json={"id": "p1", "name": "Runbook"})

    row = project_pages.retrieve("p1")

    assert row.id == "p1"


@responses.activate
def test_project_pages_find_by_name(project_pages: ProjectPages) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={"data": [{"id": "p1", "name": "Runbook"}], "pagination": {"style": "offset"}},
    )

    assert project_pages.find_by_name("Runbook").id == "p1"


@responses.activate
def test_project_pages_create_requires_only_name(project_pages: ProjectPages) -> None:
    responses.post(f"{PROJECT_BASE}/", json={"id": "p1", "name": "Runbook"}, status=201)

    project_pages.create(CreatePage(name="Runbook"))

    body = json.loads(responses.calls[0].request.body)
    assert body == {"name": "Runbook"}


@responses.activate
def test_project_pages_create_carries_collection_id(project_pages: ProjectPages) -> None:
    responses.post(f"{PROJECT_BASE}/", json={"id": "p1", "name": "Runbook"}, status=201)

    project_pages.create(CreatePage(name="Runbook", collection_id="c1"))

    body = json.loads(responses.calls[0].request.body)
    assert body["collection_id"] == "c1"


@responses.activate
def test_project_pages_update_uses_patch(project_pages: ProjectPages) -> None:
    responses.patch(f"{PROJECT_BASE}/p1/", json={"id": "p1", "name": "Renamed"})

    updated = project_pages.update("p1", UpdatePage(name="Renamed"))

    assert updated.name == "Renamed"


@responses.activate
def test_project_pages_delete_returns_none(project_pages: ProjectPages) -> None:
    responses.delete(f"{PROJECT_BASE}/p1/", status=204)

    assert project_pages.delete("p1") is None


# -- WikiPages ------------------------------------------------------------------


@responses.activate
def test_workspace_pages_hits_the_workspace_level_path_not_the_project_one(
    workspace_pages: WikiPages,
) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/",
        json={"data": [{"id": "p1", "is_global": True}], "pagination": {"style": "offset"}},
    )

    page = workspace_pages.list()

    assert page.data[0].is_global is True
    assert "projects" not in responses.calls[0].request.url


@responses.activate
def test_workspace_pages_retrieve(workspace_pages: WikiPages) -> None:
    responses.get(f"{WORKSPACE_BASE}/p1/", json={"id": "p1", "is_global": True})

    row = workspace_pages.retrieve("p1")

    assert row.id == "p1"


@responses.activate
def test_workspace_pages_create(workspace_pages: WikiPages) -> None:
    responses.post(f"{WORKSPACE_BASE}/", json={"id": "p1", "name": "Wiki Home"}, status=201)

    created = workspace_pages.create(CreatePage(name="Wiki Home"))

    assert created.id == "p1"


@responses.activate
def test_workspace_pages_update(workspace_pages: WikiPages) -> None:
    responses.patch(f"{WORKSPACE_BASE}/p1/", json={"id": "p1", "is_locked": True})

    updated = workspace_pages.update("p1", UpdatePage(is_locked=True))

    assert updated.is_locked is True


@responses.activate
def test_workspace_pages_delete_returns_none(workspace_pages: WikiPages) -> None:
    responses.delete(f"{WORKSPACE_BASE}/p1/", status=204)

    assert workspace_pages.delete("p1") is None
