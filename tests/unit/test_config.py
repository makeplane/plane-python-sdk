"""Unit tests for TLS verification config (Configuration.verify / PlaneClient(verify=...)).

These construct clients/config directly and never make network calls, so they
run without any PLANE_* environment variables.
"""

from plane.client import PlaneClient
from plane.client.oauth_client import OAuthClient
from plane.config import Configuration


def test_verify_defaults_to_true() -> None:
    config = Configuration(base_path="https://api.plane.so", api_key="test-key")
    assert config.verify is True


def test_verify_false_propagates_to_configuration() -> None:
    config = Configuration(base_path="https://api.plane.so", api_key="test-key", verify=False)
    assert config.verify is False


def test_verify_ca_bundle_path_propagates_verbatim() -> None:
    ca_path = "/etc/ssl/certs/internal-ca.pem"
    config = Configuration(base_path="https://api.plane.so", api_key="test-key", verify=ca_path)
    assert config.verify == ca_path


def test_plane_client_verify_defaults_to_true() -> None:
    client = PlaneClient(base_url="https://api.plane.so", api_key="test-key")
    assert client.config.verify is True
    assert client.projects.session.verify is True


def test_plane_client_verify_false_propagates_to_session() -> None:
    client = PlaneClient(base_url="https://api.plane.so", api_key="test-key", verify=False)
    assert client.config.verify is False
    assert client.projects.session.verify is False


def test_plane_client_verify_ca_bundle_propagates_to_all_resources() -> None:
    ca_path = "/etc/ssl/certs/internal-ca.pem"
    client = PlaneClient(base_url="https://api.plane.so", api_key="test-key", verify=ca_path)

    assert client.projects.session.verify == ca_path
    assert client.work_items.session.verify == ca_path
    # Sub-resources build their own BaseResource off the same Configuration.
    assert client.work_items.comments.session.verify == ca_path


def test_oauth_client_verify_defaults_to_true() -> None:
    oauth_client = OAuthClient(
        base_url="https://api.plane.so",
        client_id="client-id",
        client_secret="client-secret",
    )
    assert oauth_client.session.verify is True


def test_oauth_client_verify_false_propagates_to_session() -> None:
    oauth_client = OAuthClient(
        base_url="https://api.plane.so",
        client_id="client-id",
        client_secret="client-secret",
        verify=False,
    )
    assert oauth_client.session.verify is False
