import pytest
import responses
from responses import matchers

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.roles import Roles
from plane.config import Configuration

BASE = "https://api.example.com/api/v2/workspaces/acme/roles"


@pytest.fixture
def roles(config: Configuration) -> Roles:
    return Roles(V2Transport(config), slug="acme")


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

    page = roles.list()

    assert page.total_count == 1
    assert page.data[0].namespace == "workspace"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(roles: Roles) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = roles.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None


@responses.activate
def test_retrieve(roles: Roles) -> None:
    responses.get(f"{BASE}/1/", json={"id": "1", "name": "Admin"})

    role = roles.retrieve("1")

    assert role.name == "Admin"


@responses.activate
def test_find_by_name(roles: Roles) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Admin"}], "pagination": {"style": "offset"}},
    )

    assert roles.find_by_name("Admin").id == "1"


@responses.activate
def test_find_by_name_raises_on_no_match(roles: Roles) -> None:
    from plane.api.v2._kernel.errors import NoMatchFound

    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    with pytest.raises(NoMatchFound, match="name='Nope'"):
        roles.find_by_name("Nope")


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

    assert roles.find_by_slug("admin").id == "1"


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

    assert roles.find_by_slug("admin", namespace="workspace").id == "1"
