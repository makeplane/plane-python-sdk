"""Live coverage for `client.v2.users`: currently just `users.me()`. Not
workspace-scoped, so no chain conversion needed; offline coverage lives
in `tests/v2/test_users_resource.py`."""

from __future__ import annotations

import pytest

from plane.api.v2.users import Users
from plane.client import PlaneClient


@pytest.fixture
def users(client: PlaneClient) -> Users:
    return client.v2.users


class TestUsersMe:
    def test_me_returns_the_authenticated_principal(self, users: Users) -> None:
        who = users.me()
        assert who.id
        assert who.principal_kind in {"oauth", "api_key", "other"}
