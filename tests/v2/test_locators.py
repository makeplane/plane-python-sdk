"""`Workspace`/`Project` locator tests; a resource is authored bound (not wrapped), so only
construction and bound-method behavior need covering."""

from __future__ import annotations

from typing import Any

import pytest
import responses

from plane.api.v2 import V2Namespace
from plane.api.v2.project import Project
from plane.api.v2.workspace import Workspace
from plane.config import Configuration


class _RequestSpy:
    """Replaces `V2Transport.request` to record calls without making any."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def __call__(self, method: str, path: str, **kwargs: Any) -> None:
        self.calls.append((method, path))
        raise AssertionError(f"unexpected HTTP call: {method} {path}")


def test_workspace_locator_makes_no_http_calls(config: Configuration) -> None:
    v2 = V2Namespace(config)
    spy = _RequestSpy()
    v2.transport.request = spy  # type: ignore[method-assign]

    workspace = v2.workspace("acme")

    assert isinstance(workspace, Workspace)
    assert spy.calls == []


def test_project_locator_makes_no_http_calls(config: Configuration) -> None:
    v2 = V2Namespace(config)
    spy = _RequestSpy()
    v2.transport.request = spy  # type: ignore[method-assign]

    project = v2.workspace("acme").project("ENG")

    assert isinstance(project, Project)
    assert spy.calls == []


def test_workspace_wiki_locator_makes_no_http_calls(config: Configuration) -> None:
    v2 = V2Namespace(config)
    spy = _RequestSpy()
    v2.transport.request = spy  # type: ignore[method-assign]

    wiki = v2.workspace("acme").wiki

    assert wiki.pages is not None
    assert wiki.collections is not None
    assert spy.calls == []


def test_workspace_holds_transport_and_slug(config: Configuration) -> None:
    v2 = V2Namespace(config)
    workspace = v2.workspace("acme")
    assert workspace.transport is v2.transport
    assert workspace.slug == "acme"


def test_project_holds_slug_and_project_id(config: Configuration) -> None:
    v2 = V2Namespace(config)
    project = v2.workspace("acme").project("ENG")
    assert project.slug == "acme"
    assert project.project_id == "ENG"


def test_project_exposes_states_labels_and_work_items(config: Configuration) -> None:
    """`work_items` is now a plain attribute on `Project` like every resource; only its methods
    still take the old flat positional arguments."""
    project = V2Namespace(config).workspace("acme").project("ENG")

    assert hasattr(project, "states")
    assert hasattr(project, "labels")
    assert hasattr(project, "work_items")


@responses.activate
def test_chained_states_hits_the_expected_url(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = V2Namespace(config).workspace("acme").project("ENG").states.list()

    assert page.data[0].id == "1"


@responses.activate
def test_chained_labels_pass_filters(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    V2Namespace(config).workspace("acme").project("ENG").labels.list(name="bug")

    assert "name=bug" in responses.calls[0].request.url


@responses.activate
def test_scope_builders_make_no_requests_with_responses_active(config: Configuration) -> None:
    # No responses registered: constructing a scope must not touch the network. With
    # @responses.activate active, any real outbound request errors immediately instead
    # of hanging until the timeout, so a regression here fails fast.
    V2Namespace(config).workspace("acme").project("ENG")


def test_project_accepts_a_project_key_or_a_project_id(config: Configuration) -> None:
    """`project` accepts either form -- there is no server round trip at this
    point to resolve one to the other, so both are just stored verbatim."""
    workspace = V2Namespace(config).workspace("acme")

    by_key = workspace.project("ENG")
    by_id = workspace.project("11111111-1111-1111-1111-111111111111")

    assert by_key.project_id == "ENG"
    assert by_id.project_id == "11111111-1111-1111-1111-111111111111"


def test_v2_namespace_no_longer_exposes_flat_resources(config: Configuration) -> None:
    """The flat form is removed entirely -- every project/workspace-scoped
    resource is reached only through `workspace(slug)`/`.project(project)`."""
    v2 = V2Namespace(config)

    assert not hasattr(v2, "states")
    assert not hasattr(v2, "labels")
    assert not hasattr(v2, "work_items")
    assert not hasattr(v2, "resources")


@pytest.mark.parametrize(
    "attr", ["transport", "users", "user_assets"]
)
def test_v2_namespace_keeps_only_the_non_workspace_scoped_attributes(
    config: Configuration, attr: str
) -> None:
    v2 = V2Namespace(config)
    assert hasattr(v2, attr)
