"""Offline coverage for `Initiatives`: CRUD, `?expand=lead`, the `.work_items`/`.projects`/
`.labels` membership bridges (`add`/`remove`), and the workspace-level `labels` sibling
collection."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.initiatives import Initiatives
from plane.config import Configuration
from plane.models.v2.initiatives import (
    CreateInitiative,
    CreateInitiativeLabel,
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


# -- Membership bridge: work_items ------------------------------------------------


@responses.activate
def test_work_items_add_sends_add_body_and_returns_added(initiatives: Initiatives) -> None:
    responses.post(f"{BASE}/in1/work-items/", json={"added": ["wi-1"], "removed": []})

    result = initiatives.work_items.add("in1", ["wi-1"])

    assert result == ["wi-1"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": ["wi-1"]}
    assert responses.calls[0].request.url == f"{BASE}/in1/work-items/"


@responses.activate
def test_work_items_remove_sends_remove_body_and_returns_removed(initiatives: Initiatives) -> None:
    responses.post(f"{BASE}/in1/work-items/", json={"added": [], "removed": ["wi-2"]})

    result = initiatives.work_items.remove("in1", ["wi-2"])

    assert result == ["wi-2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"remove": ["wi-2"]}
    assert responses.calls[0].request.url == f"{BASE}/in1/work-items/"


@responses.activate
def test_work_items_bridge_rejects_empty_or_oversized_ids(initiatives: Initiatives) -> None:
    with pytest.raises(ValueError):
        initiatives.work_items.add("in1", [])
    with pytest.raises(ValueError):
        initiatives.work_items.add("in1", [f"wi-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        initiatives.work_items.remove("in1", [])
    with pytest.raises(ValueError):
        initiatives.work_items.remove("in1", [f"wi-{i}" for i in range(101)])

    assert len(responses.calls) == 0


# -- Membership bridge: projects ---------------------------------------------------


@responses.activate
def test_projects_add_sends_add_body_and_returns_added(initiatives: Initiatives) -> None:
    responses.post(f"{BASE}/in1/projects/", json={"added": ["proj-1"], "removed": []})

    result = initiatives.projects.add("in1", ["proj-1"])

    assert result == ["proj-1"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": ["proj-1"]}
    assert responses.calls[0].request.url == f"{BASE}/in1/projects/"


@responses.activate
def test_projects_remove_sends_remove_body_and_returns_removed(initiatives: Initiatives) -> None:
    responses.post(f"{BASE}/in1/projects/", json={"added": [], "removed": ["proj-2"]})

    result = initiatives.projects.remove("in1", ["proj-2"])

    assert result == ["proj-2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"remove": ["proj-2"]}
    assert responses.calls[0].request.url == f"{BASE}/in1/projects/"


@responses.activate
def test_projects_bridge_rejects_empty_or_oversized_ids(initiatives: Initiatives) -> None:
    with pytest.raises(ValueError):
        initiatives.projects.add("in1", [])
    with pytest.raises(ValueError):
        initiatives.projects.add("in1", [f"proj-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        initiatives.projects.remove("in1", [])
    with pytest.raises(ValueError):
        initiatives.projects.remove("in1", [f"proj-{i}" for i in range(101)])

    assert len(responses.calls) == 0


# -- Membership bridge: labels (per-initiative association) ----------------------


@responses.activate
def test_initiative_labels_bridge_add_sends_add_body_and_returns_added(
    initiatives: Initiatives,
) -> None:
    responses.post(f"{BASE}/in1/labels/", json={"added": ["lbl-1"], "removed": []})

    result = initiatives.labels.add("in1", ["lbl-1"])

    assert result == ["lbl-1"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": ["lbl-1"]}
    assert responses.calls[0].request.url == f"{BASE}/in1/labels/"


@responses.activate
def test_initiative_labels_bridge_remove_sends_remove_body_and_returns_removed(
    initiatives: Initiatives,
) -> None:
    responses.post(f"{BASE}/in1/labels/", json={"added": [], "removed": ["lbl-2"]})

    result = initiatives.labels.remove("in1", ["lbl-2"])

    assert result == ["lbl-2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"remove": ["lbl-2"]}
    assert responses.calls[0].request.url == f"{BASE}/in1/labels/"


@responses.activate
def test_initiative_labels_bridge_rejects_empty_or_oversized_ids(
    initiatives: Initiatives,
) -> None:
    with pytest.raises(ValueError):
        initiatives.labels.add("in1", [])
    with pytest.raises(ValueError):
        initiatives.labels.add("in1", [f"lbl-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        initiatives.labels.remove("in1", [])
    with pytest.raises(ValueError):
        initiatives.labels.remove("in1", [f"lbl-{i}" for i in range(101)])

    assert len(responses.calls) == 0


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
