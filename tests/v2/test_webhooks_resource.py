"""Offline coverage for `Webhooks`: CRUD plus `regenerate`, both `create` and
`regenerate` going through `_custom_action` since they return the richer
`WebhookCreateResult` envelope."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.webhooks import Webhooks
from plane.config import Configuration
from plane.models.v2.webhooks import CreateWebhook, UpdateWebhook

BASE = "https://api.example.com/api/v2/workspaces/acme/webhooks"


@pytest.fixture
def webhooks(config: Configuration) -> Webhooks:
    return Webhooks(V2Transport(config))


@responses.activate
def test_list_webhooks(webhooks: Webhooks) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "w1", "url": "https://example.com/hook", "is_active": True}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = webhooks.list("acme")

    assert page.total_count == 1
    assert page.data[0].is_active is True
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_retrieve_webhook(webhooks: Webhooks) -> None:
    responses.get(f"{BASE}/w1/", json={"id": "w1", "url": "https://example.com/hook"})

    row = webhooks.retrieve("acme", "w1")

    assert row.id == "w1"
    assert responses.calls[0].request.url == f"{BASE}/w1/"


@responses.activate
def test_find_by_name(webhooks: Webhooks) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "w1", "name": "prod"}], "pagination": {"style": "offset"}},
    )

    assert webhooks.find_by_name("acme", "prod").id == "w1"


@responses.activate
def test_create_returns_the_secret_once(webhooks: Webhooks) -> None:
    """`WebhookCreateResult` carries `secret_key` -- the golden's own
    `webhooks_create` schema omits it, but the resource returns the richer
    shape (see the module docstring's contract-drift note)."""
    responses.post(
        f"{BASE}/",
        json={
            "id": "w1",
            "url": "https://example.com/hook",
            "is_active": True,
            "secret_key": "shh-secret",
        },
        status=201,
    )

    created = webhooks.create("acme", CreateWebhook(url="https://example.com/hook"))

    assert created.id == "w1"
    assert created.secret_key == "shh-secret"
    assert responses.calls[0].request.url == f"{BASE}/"
    body = json.loads(responses.calls[0].request.body)
    assert body == {"url": "https://example.com/hook"}


@responses.activate
def test_create_fields_reach_the_query_string(webhooks: Webhooks) -> None:
    responses.post(
        f"{BASE}/",
        json={"id": "w1", "url": "https://example.com/hook", "secret_key": "shh-secret"},
        status=201,
    )

    webhooks.create("acme", CreateWebhook(url="https://example.com/hook"), fields=["id", "name"])

    assert "fields=id%2Cname" in responses.calls[0].request.url


def test_create_rejects_unknown_field_before_the_request(webhooks: Webhooks) -> None:
    with pytest.raises(ValueError, match="Unknown field"):
        webhooks.create(
            "acme",
            CreateWebhook(url="https://example.com/hook"),
            fields=["bogus"],  # type: ignore[list-item]
        )


@responses.activate
def test_update_uses_patch(webhooks: Webhooks) -> None:
    responses.patch(f"{BASE}/w1/", json={"id": "w1", "is_active": False})

    updated = webhooks.update("acme", "w1", UpdateWebhook(is_active=False))

    assert updated.is_active is False
    assert responses.calls[0].request.url == f"{BASE}/w1/"


@responses.activate
def test_delete_returns_none(webhooks: Webhooks) -> None:
    responses.delete(f"{BASE}/w1/", status=204)

    assert webhooks.delete("acme", "w1") is None
    assert responses.calls[0].request.url == f"{BASE}/w1/"


@responses.activate
def test_regenerate_posts_to_regenerate_sub_path_and_returns_a_new_secret(
    webhooks: Webhooks,
) -> None:
    responses.post(
        f"{BASE}/w1/regenerate/",
        json={"id": "w1", "secret_key": "new-secret"},
    )

    result = webhooks.regenerate("acme", "w1")

    assert result.id == "w1"
    assert result.secret_key == "new-secret"
    assert responses.calls[0].request.url == f"{BASE}/w1/regenerate/"
