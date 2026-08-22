"""Offline coverage for `Users`: `users.me()` is the one route with no workspace/project in its
path; asserts a 401 surfaces as `PlaneAPIError`."""

from __future__ import annotations

import pytest
import responses

from plane.api.v2._kernel.errors import PlaneAPIError
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.users import Users
from plane.config import Configuration

BASE = "https://api.example.com/api/v2"


@pytest.fixture
def users(config: Configuration) -> Users:
    return Users(V2Transport(config))


@responses.activate
def test_users_me(users: Users) -> None:
    responses.get(
        f"{BASE}/users/me/",
        json={
            "id": "u1",
            "display_name": "Ada",
            "email": "ada@example.com",
            "principal_kind": "api_key",
            "scopes": ["read", "write"],
        },
    )

    who = users.me()

    assert who.principal_kind == "api_key"
    assert who.scopes == ["read", "write"]
    # No slug/project in the path at all.
    assert responses.calls[0].request.url is not None
    assert responses.calls[0].request.url.startswith(f"{BASE}/users/me/")


@responses.activate
def test_users_me_surfaces_401(users: Users) -> None:
    """A 401 from the transport raises `PlaneAPIError`, not something silently
    swallowed -- negative assertion, proven capable of failing below."""
    responses.get(
        f"{BASE}/users/me/",
        json={"type": "unauthorized", "code": "unauthorized", "detail": "no token"},
        status=401,
    )

    with pytest.raises(PlaneAPIError):
        users.me()
