import pytest
import responses

from plane.api.v2 import PlaneAPIError
from plane.api.v2._kernel.transport import V2Transport
from plane.config import Configuration


def test_api_root_has_no_version_suffix() -> None:
    config = Configuration(base_path="https://api.example.com/", api_key="secret")
    assert config.api_root == "https://api.example.com"
    assert config.base_path == "https://api.example.com/api/v1"


@responses.activate
def test_request_builds_v2_url_and_sends_api_key(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [], "pagination": {"style": "offset"}},
    )
    transport = V2Transport(config)

    transport.request("GET", "/workspaces/acme/projects/ENG/states/")

    assert responses.calls[0].request.headers["X-Api-Key"] == "secret"


@responses.activate
def test_problem_json_becomes_plane_api_error(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/x/",
        status=404,
        content_type="application/problem+json",
        json={
            "type": "not_found",
            "title": "Not found",
            "status": 404,
            "code": "not_found",
            "detail": "No State matches the given query.",
        },
    )
    transport = V2Transport(config)

    with pytest.raises(PlaneAPIError) as excinfo:
        transport.request("GET", "/workspaces/acme/projects/ENG/states/x/")

    assert excinfo.value.status == 404
    assert excinfo.value.code == "not_found"
    assert excinfo.value.type == "not_found"
    assert "No State matches" in excinfo.value.detail


@responses.activate
def test_validation_problem_exposes_field_errors(config: Configuration) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        status=400,
        content_type="application/problem+json",
        json={
            "type": "invalid_request",
            "title": "Invalid request",
            "status": 400,
            "code": "invalid_request",
            "detail": "One or more fields failed validation.",
            "errors": [{"field": "name", "message": "This field is required."}],
        },
    )
    transport = V2Transport(config)

    with pytest.raises(PlaneAPIError) as excinfo:
        transport.request("POST", "/workspaces/acme/projects/ENG/states/", json={})

    assert excinfo.value.errors is not None
    assert excinfo.value.errors[0].field == "name"


@responses.activate
def test_204_returns_none(config: Configuration) -> None:
    responses.delete(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/x/", status=204
    )
    transport = V2Transport(config)

    assert transport.request("DELETE", "/workspaces/acme/projects/ENG/states/x/") is None
