import json

import pytest
import responses
from pydantic import BaseModel, ConfigDict

from plane.api.v2._kernel.resource import V2Resource
from plane.api.v2._kernel.transport import V2Transport
from plane.config import Configuration


class Row(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None


class WriteRow(BaseModel):
    name: str


class PatchRow(BaseModel):
    name: str | None = None


class Rows(V2Resource[Row, WriteRow, PatchRow]):
    path = "/workspaces/{slug}/projects/{project_id}/states/"
    model = Row
    operations = {
        "list": "states_list",
        "retrieve": "states_retrieve",
        "create": "states_create",
        "update": "states_partial_update",
    }


@pytest.fixture
def rows(config: Configuration) -> Rows:
    return Rows(V2Transport(config))


class WorkItemRows(V2Resource[Row, WriteRow, PatchRow]):
    """Uses real `work_items_list`/`work_items_retrieve` operationIds (whose `fields` enums
    genuinely differ) to test per-action `fields` validation."""

    path = "/workspaces/{slug}/projects/{project_id}/work-items/"
    model = Row
    operations = {
        "list": "work_items_list",
        "retrieve": "work_items_retrieve",
    }


@pytest.fixture
def work_item_rows(config: Configuration) -> WorkItemRows:
    return WorkItemRows(V2Transport(config))


@responses.activate
def test_list_returns_typed_rows(rows: Rows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [{"id": "1", "name": "Todo"}], "pagination": {"style": "offset"}},
    )

    page = rows._list(slug="acme", project_id="ENG")

    assert page.data[0].name == "Todo"


@responses.activate
def test_list_encodes_fields_and_filters(rows: Rows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    rows._list(slug="acme", project_id="ENG", params={"fields": ["id", "name"], "name": "Todo"})

    query = responses.calls[0].request.url
    assert "fields=id%2Cname" in query
    assert "name=Todo" in query


def test_unknown_field_is_rejected_before_the_request(rows: Rows) -> None:
    with pytest.raises(ValueError, match="nope"):
        rows._list(slug="acme", project_id="ENG", params={"fields": ["nope"]})


@responses.activate
def test_known_order_by_is_accepted(rows: Rows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    rows._list(slug="acme", project_id="ENG", params={"order_by": "-created_at"})

    assert "order_by=-created_at" in responses.calls[0].request.url


def test_unknown_order_by_is_rejected_before_the_request(rows: Rows) -> None:
    with pytest.raises(ValueError, match="nope"):
        rows._list(slug="acme", project_id="ENG", params={"order_by": "nope"})


@responses.activate
def test_order_by_list_is_validated_and_joined(rows: Rows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    rows._list(slug="acme", project_id="ENG", params={"order_by": ["created_at", "-id"]})

    assert "order_by=created_at%2C-id" in responses.calls[0].request.url


def test_order_by_list_with_an_unknown_entry_raises_value_error_not_type_error(
    rows: Rows,
) -> None:
    with pytest.raises(ValueError, match="nope"):
        rows._list(slug="acme", project_id="ENG", params={"order_by": ["created_at", "nope"]})


@responses.activate
def test_retrieve_appends_pk(rows: Rows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/abc/",
        json={"id": "abc", "name": "Todo"},
    )

    assert rows._retrieve(slug="acme", project_id="ENG", pk="abc").id == "abc"


@responses.activate
def test_update_uses_patch(rows: Rows) -> None:
    responses.patch(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/abc/",
        json={"id": "abc", "name": "Doing"},
    )

    assert (
        rows._update(PatchRow(name="Doing"), slug="acme", project_id="ENG", pk="abc").name
        == "Doing"
    )


@responses.activate
def test_delete_returns_none(rows: Rows) -> None:
    responses.delete(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/abc/", status=204
    )

    assert rows._delete(slug="acme", project_id="ENG", pk="abc") is None


def test_field_valid_for_retrieve_only_is_rejected_by_list(work_item_rows: WorkItemRows) -> None:
    """`custom_fields` is in the real `work_items_retrieve` enum but not `work_items_list`
    (verified against the generated golden). Validating `_list` against the `list`
    operation's own enum — not a single resource-wide enum — must still catch it."""
    with pytest.raises(ValueError, match="custom_fields"):
        work_item_rows._list(slug="acme", project_id="ENG", params={"fields": ["custom_fields"]})


@responses.activate
def test_field_valid_for_retrieve_only_is_accepted_by_retrieve(
    work_item_rows: WorkItemRows,
) -> None:
    """The converse of the above: the same field, illegal for `_list`, must be accepted
    by `_retrieve` because it validates against `work_items_retrieve`'s own enum."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/work-items/abc/",
        json={"id": "abc", "custom_fields": {}},
    )

    row = work_item_rows._retrieve(
        slug="acme", project_id="ENG", pk="abc", params={"fields": ["custom_fields"]}
    )

    assert row.id == "abc"


@responses.activate
def test_collection_url_percent_encodes_path_params(rows: Rows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/ac%20me/projects/ENG%2FX/states/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    rows._list(slug="ac me", project_id="ENG/X")

    query = responses.calls[0].request.url
    assert "ac%20me" in query
    assert "ENG%2FX" in query


@responses.activate
def test_detail_url_percent_encodes_pk(rows: Rows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/a%2Fb%20c/",
        json={"id": "a/b c", "name": "Todo"},
    )

    row = rows._retrieve(slug="acme", project_id="ENG", pk="a/b c")

    assert row.id == "a/b c"
    query = responses.calls[0].request.url
    assert "a%2Fb%20c" in query


class WorkItemExpandRows(V2Resource[Row, WriteRow, PatchRow]):
    """Points at the real `work_items_list` operation id, whose `expand` enum
    (`assignees, cycle, labels, modules, parent, state, type`) is exercised here
    against real golden data rather than an invented enum."""

    path = "/workspaces/{slug}/projects/{project_id}/work-items/"
    model = Row
    operations = {"list": "work_items_list"}


@pytest.fixture
def work_item_expand_rows(config: Configuration) -> WorkItemExpandRows:
    return WorkItemExpandRows(V2Transport(config))


@responses.activate
def test_valid_expand_passes_through(work_item_expand_rows: WorkItemExpandRows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/work-items/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    work_item_expand_rows._list(
        slug="acme", project_id="ENG", params={"expand": ["state", "labels"]}
    )

    query = responses.calls[0].request.url
    assert "expand=state%2Clabels" in query


def test_invalid_expand_is_rejected_before_the_request(
    work_item_expand_rows: WorkItemExpandRows,
) -> None:
    """No responses are registered (and @responses.activate is not applied): if
    validation failed to run, the real HTTP call this would otherwise attempt fails
    the test by erroring on the network, not by silently passing."""
    with pytest.raises(ValueError, match="bogus"):
        work_item_expand_rows._list(slug="acme", project_id="ENG", params={"expand": ["bogus"]})


def test_expand_as_comma_string_is_also_validated(
    work_item_expand_rows: WorkItemExpandRows,
) -> None:
    with pytest.raises(ValueError, match="bogus"):
        work_item_expand_rows._list(slug="acme", project_id="ENG", params={"expand": "state,bogus"})


class ArchivableRows(V2Resource[Row, WriteRow, PatchRow]):
    """Exercises `_action` against the real `work_items_archive` operation id."""

    path = "/workspaces/{slug}/projects/{project_id}/work-items/"
    model = Row
    operations = {"archive": "work_items_archive"}


@pytest.fixture
def archivable_rows(config: Configuration) -> ArchivableRows:
    return ArchivableRows(V2Transport(config))


@responses.activate
def test_action_posts_to_the_named_sub_path_and_returns_the_row(
    archivable_rows: ArchivableRows,
) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/work-items/abc/archive/",
        json={"id": "abc", "name": "Archived"},
    )

    row = archivable_rows._action("archive", pk="abc", slug="acme", project_id="ENG")

    assert row.id == "abc"
    assert row.name == "Archived"


@responses.activate
def test_action_validates_expand_against_its_own_operation_id(
    archivable_rows: ArchivableRows,
) -> None:
    with pytest.raises(ValueError, match="bogus"):
        archivable_rows._action(
            "archive", pk="abc", slug="acme", project_id="ENG", params={"expand": ["bogus"]}
        )


# -- Membership bridges (`_bridge`) -------------------------------------------------


class MemberRow(BaseModel):
    member_id: str
    access: int | None = None


class BridgeRows(V2Resource[Row, WriteRow, PatchRow]):
    """Catalog-style resource whose bridge URL differs from its own `path`."""

    path = "/workspaces/{slug}/releases/labels/"
    extra_paths = {
        "add": "/workspaces/{slug}/releases/{release_id}/labels/",
        "remove": "/workspaces/{slug}/releases/{release_id}/labels/",
    }
    model = Row
    operations = {"bridge": "releases_labels"}


@pytest.fixture
def bridge_rows(config: Configuration) -> BridgeRows:
    return BridgeRows(V2Transport(config))


@responses.activate
def test_bridge_add_posts_only_the_add_key_and_returns_added(bridge_rows: BridgeRows) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/releases/r1/labels/",
        json={"added": ["l1"], "removed": []},
    )

    added = bridge_rows._bridge(key="add", ids=["l1", "l2"], slug="acme", release_id="r1")

    assert added == ["l1"]
    assert json.loads(responses.calls[0].request.body) == {"add": ["l1", "l2"]}


@responses.activate
def test_bridge_remove_posts_only_the_remove_key_and_returns_removed(
    bridge_rows: BridgeRows,
) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/releases/r1/labels/",
        json={"added": [], "removed": ["l1"]},
    )

    removed = bridge_rows._bridge(key="remove", ids=["l1"], slug="acme", release_id="r1")

    assert removed == ["l1"]
    assert json.loads(responses.calls[0].request.body) == {"remove": ["l1"]}


@responses.activate
def test_bridge_returns_empty_list_when_the_result_key_is_absent(bridge_rows: BridgeRows) -> None:
    responses.post("https://api.example.com/api/v2/workspaces/acme/releases/r1/labels/", json={})

    assert bridge_rows._bridge(key="add", ids=["l1"], slug="acme", release_id="r1") == []


@responses.activate
def test_bridge_serializes_pydantic_entries_without_nones(bridge_rows: BridgeRows) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/releases/r1/labels/",
        json={"added": ["u1", "u2"]},
    )

    bridge_rows._bridge(
        key="add",
        ids=[MemberRow(member_id="u1", access=1), MemberRow(member_id="u2")],
        slug="acme",
        release_id="r1",
    )

    assert json.loads(responses.calls[0].request.body) == {
        "add": [{"member_id": "u1", "access": 1}, {"member_id": "u2"}]
    }


@responses.activate
def test_bridge_rejects_empty_and_over_cap_id_lists_before_any_request(
    bridge_rows: BridgeRows,
) -> None:
    with pytest.raises(ValueError, match="at least one"):
        bridge_rows._bridge(key="add", ids=[], release_id="r1")
    with pytest.raises(ValueError, match="At most 100"):
        bridge_rows._bridge(key="remove", ids=["x"] * 101, release_id="r1")
    assert len(responses.calls) == 0


def test_bridge_rejects_unknown_keys(bridge_rows: BridgeRows) -> None:
    with pytest.raises(ValueError, match="'add' or 'remove'"):
        bridge_rows._bridge(key="manage", ids=["x"], release_id="r1")
