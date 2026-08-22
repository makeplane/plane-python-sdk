import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.invitations import Invitations
from plane.config import Configuration
from plane.models.v2.invitations import BulkCreateWorkspaceInvites, CreateWorkspaceInvite

BASE = "https://api.example.com/api/v2/workspaces/acme/invitations"


@pytest.fixture
def invitations(config: Configuration) -> Invitations:
    return Invitations(V2Transport(config), slug="acme")


@responses.activate
def test_list_invitations(invitations: Invitations) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "email": "a@example.com", "accepted": False}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = invitations.list()

    assert page.total_count == 1
    assert page.data[0].accepted is False


@responses.activate
def test_sparse_response_leaves_absent_fields_none(invitations: Invitations) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = invitations.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].email is None


@responses.activate
def test_create_and_retrieve(invitations: Invitations) -> None:
    responses.post(f"{BASE}/", json={"id": "1", "email": "a@example.com"}, status=201)
    responses.get(f"{BASE}/1/", json={"id": "1", "email": "a@example.com", "accepted": False})

    created = invitations.create(CreateWorkspaceInvite(email="a@example.com"))
    fetched = invitations.retrieve(created.id)

    assert fetched.email == "a@example.com"


@responses.activate
def test_delete(invitations: Invitations) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert invitations.delete("1") is None


@responses.activate
def test_bulk_parses_the_live_list_response(invitations: Invitations) -> None:
    """The live view returns `many=True` on this 201 (a real list), not the golden's single
    `WorkspaceInvite` -- asserts the resource handles the list shape."""
    responses.post(
        f"{BASE}/bulk/",
        json=[
            {"id": "1", "email": "a@example.com"},
            {"id": "2", "email": "b@example.com"},
        ],
        status=201,
    )

    result = invitations.bulk(BulkCreateWorkspaceInvites(emails=["a@example.com", "b@example.com"]))

    assert [row.id for row in result] == ["1", "2"]


@responses.activate
def test_bulk_also_tolerates_a_single_object_payload(invitations: Invitations) -> None:
    """If the server ever matches the golden's documented single-object shape
    instead, the SDK should not crash -- it normalizes to a one-item list."""
    responses.post(f"{BASE}/bulk/", json={"id": "1", "email": "a@example.com"}, status=201)

    result = invitations.bulk(BulkCreateWorkspaceInvites(emails=["a@example.com"]))

    assert [row.id for row in result] == ["1"]
