"""Navigable rows for the two families migrated in this plan: `Release` (children
`labels`, `tags`, `comments`, `links`, `changelog`, `work_items`) and `Initiative`
(children `labels`, `projects`, `work_items`).

`Releases` is already wired onto `Workspaces` (for the sake of `.labels`/`.tags`, now
joined by its own CRUD and the rest of the family); `Initiatives` is not wired onto
the tree yet -- that is later follow-on work -- so it is constructed directly through
`V2Transport`, the same way every other offline resource test in this package is."""

from __future__ import annotations

import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.initiatives import Initiatives
from plane.api.v2.releases import Releases
from plane.config import Configuration


@responses.activate
def test_fetched_release_reaches_its_comments(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/releases/r1/", json={"id": "r1", "name": "v1.0"})
    responses.get(
        f"{base}/releases/r1/comments/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    release = Releases(V2Transport(config)).retrieve("acme", "r1")
    release.comments.list()

    assert release.name == "v1.0"
    assert responses.calls[1].request.url == f"{base}/releases/r1/comments/"


@responses.activate
def test_fetched_release_reaches_its_links(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/releases/r1/", json={"id": "r1"})
    responses.get(
        f"{base}/releases/r1/links/", json={"data": [], "pagination": {"style": "offset"}}
    )

    release = Releases(V2Transport(config)).retrieve("acme", "r1")
    release.links.list()

    assert responses.calls[1].request.url == f"{base}/releases/r1/links/"


@responses.activate
def test_fetched_release_reaches_its_changelog(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/releases/r1/", json={"id": "r1"})
    responses.get(f"{base}/releases/r1/changelog/", json={"id": "chg-1"})

    release = Releases(V2Transport(config)).retrieve("acme", "r1")
    changelog = release.changelog.retrieve()

    assert changelog.id == "chg-1"
    assert responses.calls[1].request.url == f"{base}/releases/r1/changelog/"


@responses.activate
def test_fetched_release_reaches_its_work_items(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/releases/r1/", json={"id": "r1"})
    responses.post(f"{base}/releases/r1/work-items/", json={"added": ["w1"], "removed": []})

    release = Releases(V2Transport(config)).retrieve("acme", "r1")
    added = release.work_items.add(["w1"])

    assert added == ["w1"]
    assert responses.calls[1].request.url == f"{base}/releases/r1/work-items/"


@responses.activate
def test_fetched_release_reaches_its_labels_bridge(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/releases/r1/", json={"id": "r1"})
    responses.post(f"{base}/releases/r1/labels/", json={"added": ["lbl-1"], "removed": []})

    release = Releases(V2Transport(config)).retrieve("acme", "r1")
    added = release.labels.add(["lbl-1"])

    assert added == ["lbl-1"]
    assert responses.calls[1].request.url == f"{base}/releases/r1/labels/"


@responses.activate
def test_listed_and_iterated_releases_are_both_navigable(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(
        f"{base}/releases/",
        json={"data": [{"id": "r1", "name": "v1.0"}], "pagination": {"style": "offset"}},
    )
    responses.get(
        f"{base}/releases/r1/links/", json={"data": [], "pagination": {"style": "offset"}}
    )

    page = Releases(V2Transport(config)).list("acme")
    page.data[0].links.list()

    assert responses.calls[1].request.url == f"{base}/releases/r1/links/"


@responses.activate
def test_iterated_release_reaches_its_comments(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(
        f"{base}/releases/",
        json={"data": [{"id": "r1"}], "pagination": {"style": "offset"}},
    )
    responses.get(
        f"{base}/releases/r1/comments/", json={"data": [], "pagination": {"style": "offset"}}
    )

    rows = list(Releases(V2Transport(config)).iterate("acme"))
    rows[0].comments.list()

    assert responses.calls[1].request.url == f"{base}/releases/r1/comments/"


@responses.activate
def test_fetched_initiative_reaches_its_projects(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/initiatives/in1/", json={"id": "in1", "name": "Q3 push"})
    responses.post(f"{base}/initiatives/in1/projects/", json={"added": ["p1"], "removed": []})

    initiative = Initiatives(V2Transport(config)).retrieve("acme", "in1")
    added = initiative.projects.add(["p1"])

    assert initiative.name == "Q3 push"
    assert added == ["p1"]
    assert responses.calls[1].request.url == f"{base}/initiatives/in1/projects/"


@responses.activate
def test_fetched_initiative_reaches_its_work_items(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/initiatives/in1/", json={"id": "in1"})
    responses.post(f"{base}/initiatives/in1/work-items/", json={"added": ["w1"], "removed": []})

    initiative = Initiatives(V2Transport(config)).retrieve("acme", "in1")
    added = initiative.work_items.add(["w1"])

    assert added == ["w1"]
    assert responses.calls[1].request.url == f"{base}/initiatives/in1/work-items/"


@responses.activate
def test_fetched_initiative_reaches_its_labels_bridge(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/initiatives/in1/", json={"id": "in1"})
    responses.post(f"{base}/initiatives/in1/labels/", json={"added": ["lbl-1"], "removed": []})

    initiative = Initiatives(V2Transport(config)).retrieve("acme", "in1")
    added = initiative.labels.add(["lbl-1"])

    assert added == ["lbl-1"]
    assert responses.calls[1].request.url == f"{base}/initiatives/in1/labels/"


@responses.activate
def test_listed_and_iterated_initiatives_are_both_navigable(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(
        f"{base}/initiatives/",
        json={"data": [{"id": "in1", "name": "Q3 push"}], "pagination": {"style": "offset"}},
    )
    responses.post(f"{base}/initiatives/in1/projects/", json={"added": ["p1"], "removed": []})

    page = Initiatives(V2Transport(config)).list("acme")
    page.data[0].projects.add(["p1"])

    assert responses.calls[1].request.url == f"{base}/initiatives/in1/projects/"
