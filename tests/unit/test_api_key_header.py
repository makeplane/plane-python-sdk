"""Unit tests for the configurable API-key header (no network, no env)."""

from __future__ import annotations

import pytest

from plane.api.base_resource import BaseResource
from plane.api.v2._kernel.transport import V2Transport
from plane.client import PlaneClient
from plane.config import Configuration
from plane.errors.errors import ConfigurationError


def test_default_header_is_x_api_key() -> None:
    config = Configuration(base_path="https://api.plane.so", api_key="k")
    headers = BaseResource(config, "/workspaces/")._headers()
    assert headers["X-Api-Key"] == "k"


def test_custom_header_replaces_x_api_key_in_v1_and_v2() -> None:
    config = Configuration(
        base_path="http://gateway/plane-api", api_key="k", api_key_header="X-Gravitee-Api-Key"
    )
    for headers in (BaseResource(config, "/workspaces/")._headers(), V2Transport(config)._headers()):
        assert headers["X-Gravitee-Api-Key"] == "k"
        assert "X-Api-Key" not in headers


def test_plane_client_passes_the_header_through() -> None:
    client = PlaneClient(base_url="http://gateway", api_key="k", api_key_header="X-Custom-Key")
    assert client.config.api_key_header == "X-Custom-Key"
    assert client.work_items._headers()["X-Custom-Key"] == "k"


def test_blank_header_is_refused() -> None:
    with pytest.raises(ConfigurationError):
        Configuration(base_path="https://api.plane.so", api_key="k", api_key_header=" ")


def test_access_token_ignores_the_header_setting() -> None:
    config = Configuration(base_path="https://api.plane.so", access_token="t", api_key_header="X-Other")
    headers = BaseResource(config, "/workspaces/")._headers()
    assert headers["Authorization"] == "Bearer t"
    assert "X-Other" not in headers
