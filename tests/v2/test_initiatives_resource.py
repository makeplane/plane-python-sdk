"""Offline coverage for `Initiatives`: CRUD, `?expand=lead`, manage verbs, and the workspace-level
`labels` sibling collection."""

from __future__ import annotations

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.initiatives import Initiatives
from plane.config import Configuration
from plane.models.v2.initiatives import (
    CreateInitiative,
    CreateInitiativeLabel,
    InitiativeChildManageRequest,
    UpdateInitiative,
    UpdateInitiativeLabel,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/initiatives"


@pytest.fixture
def initiatives(config: Configuration) -> Initiatives:
    return Initiatives(V2Transport(config), slug="acme")


@responses.activate
def test_list_initiatives_is_workspace_scoped_not_project_scoped(
    initiatives: Initiatives,
) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "in1", "name": "Q3 push", "state": "ACTIVE"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = initiatives.list()

    assert page.data[0].state == "ACTIVE"
    assert "projects" not in responses.calls[0].request.url


@responses.activate
def test_list_passes_expand(initiatives: Initiatives) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    initiatives.list(expand=["lead"])

    assert "expand=lead" in responses.calls[0].request.url


def test_list_rejects_unknown_expand_before_the_request(initiatives: Initiatives) -> None:
    with pytest.raises(ValueError, match="bogus"):
        initiatives.list(expand=["bogus"])


@responses.activate
def test_create_then_patch_then_delete_initiative(initiatives: Initiatives) -> None:
    responses.post(f"{BASE}/", json={"id": "in1", "name": "Q3 push"}, status=201)
    responses.patch(f"{BASE}/in1/", json={"id": "in1", "state": "COMPLETED"})
    responses.delete(f"{BASE}/in1/", status=204)

    created = initiatives.create(CreateInitiative(name="Q3 push"))
    updated = initiatives.update(created.id, UpdateInitiative(state="COMPLETED"))

    assert updated.state == "COMPLETED"
    assert initiatives.delete("in1") is None


@responses.activate
def test_find_initiative_by_name(initiatives: Initiatives) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "in1", "name": "Q3 push"}], "pagination": {"style": "offset"}},
    )

    assert initiatives.find_by_name("Q3 push").id == "in1"


@responses.activate
def test_manage_labels_projects_work_items(initiatives: Initiatives) -> None:
    responses.post(f"{BASE}/in1/labels/", json={"added": ["lbl-1"], "removed": []})
    responses.post(f"{BASE}/in1/projects/", json={"added": ["proj-1"], "removed": []})
    responses.post(f"{BASE}/in1/work-items/", json={"added": ["wi-1"], "removed": ["wi-2"]})

    labels_result = initiatives.manage_labels("in1", InitiativeChildManageRequest(add=["lbl-1"]))
    assert labels_result.added == ["lbl-1"]

    projects_result = initiatives.manage_projects(
        "in1", InitiativeChildManageRequest(add=["proj-1"])
    )
    assert projects_result.added == ["proj-1"]

    work_items_result = initiatives.manage_work_items(
        "in1", InitiativeChildManageRequest(add=["wi-1"], remove=["wi-2"])
    )
    assert work_items_result.added == ["wi-1"]
    assert work_items_result.removed == ["wi-2"]

    # Each verb action hits its own sub-path, not a shared one.
    assert responses.calls[0].request.url.endswith("/in1/labels/")
    assert responses.calls[1].request.url.endswith("/in1/projects/")
    assert responses.calls[2].request.url.endswith("/in1/work-items/")


# -- Sibling collection: labels (workspace-level, not nested under an initiative) --


@responses.activate
def test_initiative_labels_crud_has_no_initiative_id_in_its_path(
    initiatives: Initiatives,
) -> None:
    responses.get(
        f"{BASE}/labels/",
        json={"data": [{"id": "lbl-1", "name": "priority"}], "pagination": {"style": "offset"}},
    )
    responses.post(f"{BASE}/labels/", json={"id": "lbl-1", "name": "priority"}, status=201)
    responses.patch(f"{BASE}/labels/lbl-1/", json={"id": "lbl-1", "color": "#f00"})
    responses.delete(f"{BASE}/labels/lbl-1/", status=204)

    page = initiatives.labels.list()
    assert page.data[0].name == "priority"
    assert responses.calls[0].request.url == f"{BASE}/labels/"

    created = initiatives.labels.create(CreateInitiativeLabel(name="priority"))
    assert created.id == "lbl-1"

    updated = initiatives.labels.update("lbl-1", UpdateInitiativeLabel(color="#f00"))
    assert updated.color == "#f00"

    assert initiatives.labels.delete("lbl-1") is None


@responses.activate
def test_initiative_labels_find_by_name(initiatives: Initiatives) -> None:
    responses.get(
        f"{BASE}/labels/",
        json={"data": [{"id": "lbl-1", "name": "priority"}], "pagination": {"style": "offset"}},
    )

    assert initiatives.labels.find_by_name("priority").id == "lbl-1"
