import pytest
import responses
from responses import matchers

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.roles import Roles
from plane.config import Configuration

BASE = "https://api.example.com/api/v2/workspaces/acme/roles"


@pytest.fixture
def roles(config: Configuration) -> Roles:
    return Roles(V2Transport(config))


@responses.activate
def test_list_takes_the_workspace_slug(roles: Roles) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/roles/",
        json={
            "data": [{"id": "r1", "name": "Admin"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = roles.list("acme")

    assert page.data[0].name == "Admin"
    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/roles/"
    )


@responses.activate
def test_list_roles(roles: Roles) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "Admin", "namespace": "workspace", "level": 20}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = roles.list("acme")

    assert page.total_count == 1
    assert page.data[0].namespace == "workspace"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_sparse_response_leaves_absent_fields_none(roles: Roles) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = roles.list("acme", fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None
    assert "fields=id" in responses.calls[0].request.url


@responses.activate
def test_list_per_page_and_offset_reach_the_query_string(roles: Roles) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    roles.list("acme", per_page=50, offset=100)

    request_url = responses.calls[0].request.url
    assert "per_page=50" in request_url
    assert "offset=100" in request_url


@responses.activate
def test_list_role_slug_filter_reaches_the_golden_slug_query_param(roles: Roles) -> None:
    """`role_slug` is the way to reach the golden's own `?slug=` role filter from
    `list()`, since the leading path id already claims the keyword `slug` for the
    workspace."""
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "slug": "admin"}], "pagination": {"style": "offset"}},
    )

    roles.list("acme", role_slug="admin")

    assert "slug=admin" in responses.calls[0].request.url


@responses.activate
def test_list_namespace_is_system_and_search_reach_the_query_string(roles: Roles) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    roles.list("acme", namespace="workspace", is_system=True, search="admin")

    request_url = responses.calls[0].request.url
    assert "namespace=workspace" in request_url
    assert "is_system=True" in request_url
    assert "search=admin" in request_url


@responses.activate
def test_iterate_takes_the_workspace_slug(roles: Roles) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "Admin"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    rows = list(roles.iterate("acme"))

    assert rows[0].id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_retrieve(roles: Roles) -> None:
    responses.get(f"{BASE}/1/", json={"id": "1", "name": "Admin"})

    role = roles.retrieve("acme", "1")

    assert role.name == "Admin"
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_find_by_name(roles: Roles) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Admin"}], "pagination": {"style": "offset"}},
    )

    found = roles.find_by_name("acme", "Admin")

    assert found.id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_find_by_name_raises_on_no_match(roles: Roles) -> None:
    from plane.api.v2._kernel.errors import NoMatchFound

    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    with pytest.raises(NoMatchFound, match="name='Nope'"):
        roles.find_by_name("acme", "Nope")


@responses.activate
def test_find_by_slug(roles: Roles) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "Admin", "slug": "admin"}],
            "pagination": {"style": "offset"},
        },
        match=[matchers.query_param_matcher({"slug": "admin", "per_page": "2", "count": "False"})],
    )

    found = roles.find_by_slug("acme", "admin")

    assert found.id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_find_by_slug_with_namespace(roles: Roles) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "Admin", "slug": "admin", "namespace": "workspace"}],
            "pagination": {"style": "offset"},
        },
        match=[
            matchers.query_param_matcher(
                {
                    "slug": "admin",
                    "namespace": "workspace",
                    "per_page": "2",
                    "count": "False",
                }
            )
        ],
    )

    found = roles.find_by_slug("acme", "admin", namespace="workspace")

    assert found.id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")
