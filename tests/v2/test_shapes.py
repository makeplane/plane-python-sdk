import responses

from plane.api.v2 import V2Namespace
from plane.config import Configuration

WS = "https://api.example.com/api/v2/workspaces/acme"


@responses.activate
def test_grouping_node_consumes_no_id(config: Configuration) -> None:
    responses.get(
        f"{WS}/pages/", json={"data": [], "pagination": {"style": "offset"}, "total_count": 0}
    )

    V2Namespace(config).workspaces.wiki.pages.list("acme")

    assert responses.calls[0].request.url.startswith(f"{WS}/pages/")


@responses.activate
def test_singleton_has_no_pk(config: Configuration) -> None:
    responses.get(f"{WS}/features/", json={"id": "f1", "is_project_grouping_enabled": True})

    features = V2Namespace(config).workspaces.features.retrieve("acme")

    assert features.is_project_grouping_enabled is True


@responses.activate
def test_bridge_uses_its_override_template(config: Configuration) -> None:
    responses.post(f"{WS}/releases/r1/labels/", json={"added": ["l1"]})

    added = V2Namespace(config).workspaces.releases.labels.add("acme", "r1", ["l1"])

    assert added == ["l1"]
    assert responses.calls[0].request.url.endswith("/releases/r1/labels/")


@responses.activate
def test_catalog_list_uses_the_primary_template(config: Configuration) -> None:
    responses.get(
        f"{WS}/releases/labels/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.releases.labels.list("acme")

    assert responses.calls[0].request.url.startswith(f"{WS}/releases/labels/")
