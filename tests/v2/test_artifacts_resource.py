"""Offline coverage for artifacts; pins the differently-shaped envelope each action actually
validates against."""

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.artifacts import Artifacts
from plane.config import Configuration
from plane.models.v2.artifacts import CreateArtifact, UpdateArtifactUpdate

BASE = "https://api.example.com/api/v2/workspaces/acme/artifacts"


@pytest.fixture
def artifacts(config: Configuration) -> Artifacts:
    return Artifacts(V2Transport(config))


@responses.activate
def test_create_returns_the_artifact_envelope(artifacts: Artifacts) -> None:
    responses.post(
        f"{BASE}/",
        json={
            "id": "1",
            "name": "Report",
            "current_version": 1,
            "is_published": False,
            "anchor": None,
            "data_mode": "snapshot",
        },
        status=201,
    )

    created = artifacts.create("acme", CreateArtifact(name="Report", html="<p>hi</p>"))

    assert created.is_published is False
    assert created.anchor is None
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_retrieve_returns_the_detail_envelope_with_html(artifacts: Artifacts) -> None:
    responses.get(
        f"{BASE}/1/",
        json={
            "id": "1",
            "name": "Report",
            "description": "",
            "data_mode": "snapshot",
            "current_version": 1,
            "html": "<p>hi</p>",
        },
    )

    detail = artifacts.retrieve("acme", "1")

    assert detail.html == "<p>hi</p>"
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_publish_sends_no_body_and_returns_the_publish_envelope(artifacts: Artifacts) -> None:
    responses.post(f"{BASE}/1/publish/", json={"anchor": "anc123", "is_active": True}, status=201)

    published = artifacts.publish("acme", "1")

    assert published.anchor == "anc123"
    assert responses.calls[0].request.body is None
    assert responses.calls[0].request.url == f"{BASE}/1/publish/"


@responses.activate
def test_update_hits_the_update_sub_path_and_returns_the_updated_envelope(
    artifacts: Artifacts,
) -> None:
    responses.patch(
        f"{BASE}/1/update/", json={"id": "1", "current_version": 2, "data_mode": "snapshot"}
    )

    updated = artifacts.update("acme", "1", UpdateArtifactUpdate(html="<p>v2</p>"))

    assert updated.current_version == 2
    assert responses.calls[0].request.url == f"{BASE}/1/update/"
