"""`Webhooks` against a real server, reached as `client.v2.workspace(slug).webhooks`.
Pins the open contract question in `plane.models.v2.webhooks`: whether `create()`
really returns `secret_key` despite the golden documenting a bare `Webhook`."""

from __future__ import annotations

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.webhooks import Webhooks
from plane.client import PlaneClient
from plane.models.v2.webhooks import CreateWebhook, UpdateWebhook

from .helpers import unique_name


@pytest.fixture
def webhooks(client: PlaneClient, workspace_slug: str) -> Webhooks:
    return client.v2.workspace(workspace_slug).webhooks


def _unique_url() -> str:
    return f"https://example.com/hooks/{unique_name('wh')}"


class TestCRUD:
    def test_create_returns_a_secret_key_once(self, webhooks: Webhooks) -> None:
        created = webhooks.create(CreateWebhook(url=_unique_url()))
        try:
            assert created.id
            assert created.secret_key
        finally:
            webhooks.delete(created.id)

    def test_retrieve_does_not_carry_a_secret(self, webhooks: Webhooks) -> None:
        created = webhooks.create(CreateWebhook(url=_unique_url()))
        try:
            fetched = webhooks.retrieve(created.id)
            assert fetched.id == created.id
            assert "secret_key" not in (fetched.model_extra or {})
        finally:
            webhooks.delete(created.id)

    def test_patch_updates_only_the_given_fields(self, webhooks: Webhooks) -> None:
        created = webhooks.create(CreateWebhook(url=_unique_url()))
        try:
            updated = webhooks.update(created.id, UpdateWebhook(is_active=False))
            assert updated.id == created.id
            assert updated.is_active is False
        finally:
            webhooks.delete(created.id)

    def test_delete_then_retrieve_404s(self, webhooks: Webhooks) -> None:
        created = webhooks.create(CreateWebhook(url=_unique_url()))
        webhooks.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            webhooks.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_find_by_name(self, webhooks: Webhooks) -> None:
        name = unique_name("webhook")
        created = webhooks.create(CreateWebhook(url=_unique_url(), name=name))
        try:
            assert webhooks.find_by_name(name).id == created.id
        finally:
            webhooks.delete(created.id)


class TestRegenerate:
    def test_regenerate_mints_a_different_secret(self, webhooks: Webhooks) -> None:
        created = webhooks.create(CreateWebhook(url=_unique_url()))
        try:
            regenerated = webhooks.regenerate(created.id)
            assert regenerated.id == created.id
            assert regenerated.secret_key
            assert regenerated.secret_key != created.secret_key
        finally:
            webhooks.delete(created.id)
