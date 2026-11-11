"""Offline coverage for `AgentRuns`, its `activities` child and the workspace-wide
`agent_run_activities` feed: every operation's URL, method, query and body, the DTO
rules the API enforces, and navigation from a fetched run and a fetched workspace."""

import json
from urllib.parse import parse_qs, urlparse

import pytest
import responses
from pydantic import ValidationError

from plane.api.v2 import LoadedAgentRun, PlaneAPIError, V2Namespace
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.agent_runs import AgentRuns, WorkspaceAgentRunActivities
from plane.config import Configuration
from plane.models.v2.agent_runs import (
    AgentRunActivity,
    CreateAgentRun,
    CreateAgentRunActivity,
    UpdateAgentRun,
)

ROOT = "https://api.example.com/api/v2/workspaces/acme"
RUNS = f"{ROOT}/runs"
RUN = {
    "id": "r1",
    "agent_user_id": "bot-1",
    "comment_id": "c1",
    "source_comment_id": "c1",
    "work_item_id": "w1",
    "project_id": "p1",
    "status": "in_progress",
    "type": "comment_thread",
    "title": "Write a poem",
    "token_usage": {},
    "started_at": "2026-11-10T09:00:00Z",
    "updated_at": "2026-11-10T09:00:05Z",
}
PROMPT = {
    "id": "a1",
    "agent_run_id": "r1",
    "type": "prompt",
    "content": {"type": "prompt", "body": "<p>Make it rhyme</p>"},
    "signal": "continue",
    "ephemeral": False,
    "comment_id": "c2",
}


@pytest.fixture
def runs(config: Configuration) -> AgentRuns:
    return AgentRuns(V2Transport(config))


@pytest.fixture
def feed(config: Configuration) -> WorkspaceAgentRunActivities:
    return WorkspaceAgentRunActivities(V2Transport(config))


def _query(call_index: int = 0) -> dict[str, list[str]]:
    return parse_qs(urlparse(responses.calls[call_index].request.url).query)


def _body(call_index: int = 0) -> object:
    body = responses.calls[call_index].request.body
    return json.loads(body) if body else None


# -- Runs ---------------------------------------------------------------------------


@responses.activate
def test_list_sends_filters_expand_and_the_cursor_envelope(runs: AgentRuns) -> None:
    responses.get(
        f"{RUNS}/",
        json={
            "data": [RUN],
            "pagination": {"style": "cursor"},
            "has_more": False,
            "next_cursor": None,
        },
    )

    page = runs.list(
        "acme",
        status__in=["in_progress", "awaiting"],
        work_item_id="w1",
        updated_at__gte="2026-11-10T09:00:00Z",
        expand=["agent_user", "work_item"],
        order_by="-updated_at",
        paginate="cursor",
        per_page=50,
    )

    assert _query() == {
        "status__in": ["in_progress,awaiting"],
        "work_item_id": ["w1"],
        "updated_at__gte": ["2026-11-10T09:00:00Z"],
        "expand": ["agent_user,work_item"],
        "order_by": ["-updated_at"],
        "paginate": ["cursor"],
        "per_page": ["50"],
    }
    row = page.data[0]
    assert isinstance(row, LoadedAgentRun)
    assert row.status == "in_progress"
    assert row.activities._ids == ("acme", "r1")


def test_list_rejects_options_the_golden_does_not_offer(runs: AgentRuns) -> None:
    with pytest.raises(ValueError, match="Unknown order_by"):
        runs.list("acme", order_by="title")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="Unknown expand"):
        runs.list("acme", expand=["actor"])
    with pytest.raises(ValueError, match="Unknown field"):
        runs.list("acme", fields=["name"])  # type: ignore[list-item]


@responses.activate
def test_iterate_follows_cursor_pages_and_threads_the_ids(runs: AgentRuns) -> None:
    responses.get(
        f"{RUNS}/",
        json={
            "data": [{**RUN, "id": "r1"}],
            "pagination": {"style": "cursor"},
            "has_more": True,
            "next_cursor": "cur-2",
        },
    )
    responses.get(
        f"{RUNS}/",
        json={
            "data": [{**RUN, "id": "r2"}],
            "pagination": {"style": "cursor"},
            "has_more": False,
            "next_cursor": None,
        },
    )

    rows = list(runs.iterate("acme", paginate="cursor", status="awaiting"))

    assert [row.id for row in rows] == ["r1", "r2"]
    assert rows[1].activities._ids == ("acme", "r2")
    assert _query(1) == {"paginate": ["cursor"], "status": ["awaiting"], "cursor": ["cur-2"]}


@responses.activate
def test_retrieve_passes_fields_and_expand(runs: AgentRuns) -> None:
    responses.get(
        f"{RUNS}/r1/",
        json={"id": "r1", "status": "completed", "comment": {"id": "c1", "comment_html": "<p/>"}},
    )

    row = runs.retrieve("acme", "r1", fields=["id", "status"], expand=["comment"])

    assert row.status == "completed"
    assert _query() == {"fields": ["id,status"], "expand": ["comment"]}


@responses.activate
def test_create_sends_only_the_fields_set(runs: AgentRuns) -> None:
    responses.post(f"{RUNS}/", json={**RUN, "status": "created"}, status=201)

    created = runs.create(
        "acme", CreateAgentRun(agent_slug="poem-agent", comment_id="c1", title="Write a poem")
    )

    assert created.status == "created"
    assert created.activities._ids == ("acme", "r1")
    assert _body() == {"agent_slug": "poem-agent", "comment_id": "c1", "title": "Write a poem"}


def test_create_needs_an_agent_slug_and_a_comment() -> None:
    with pytest.raises(ValidationError):
        CreateAgentRun(agent_slug="", comment_id="c1")
    with pytest.raises(ValidationError):
        CreateAgentRun(agent_slug="poem-agent")  # type: ignore[call-arg]


@responses.activate
def test_update_patches_the_agents_report(runs: AgentRuns) -> None:
    responses.patch(f"{RUNS}/r1/", json={**RUN, "status": "completed", "summary": "Done."})

    updated = runs.update(
        "acme",
        "r1",
        UpdateAgentRun(status="completed", summary="Done.", token_usage={"input": 12}),
    )

    assert updated.status == "completed"
    assert responses.calls[0].request.method == "PATCH"
    assert _body() == {"status": "completed", "summary": "Done.", "token_usage": {"input": 12}}


def test_update_only_settles_a_run_as_completed() -> None:
    with pytest.raises(ValidationError):
        UpdateAgentRun(status="stopped")  # type: ignore[arg-type]


@responses.activate
def test_stop_posts_with_no_body_and_answers_the_run(runs: AgentRuns) -> None:
    responses.post(f"{RUNS}/r1/stop/", json={**RUN, "status": "stopping"})

    stopped = runs.stop("acme", "r1", fields=["id", "status"])

    assert stopped.status == "stopping"
    assert responses.calls[0].request.body is None
    assert _query() == {"fields": ["id,status"]}
    assert stopped.activities._ids == ("acme", "r1")


@responses.activate
def test_stopping_an_ended_run_raises_the_409(runs: AgentRuns) -> None:
    responses.post(
        f"{RUNS}/r1/stop/",
        status=409,
        json={
            "type": "https://developers.plane.so/errors/conflict",
            "title": "Conflict",
            "status": 409,
            "code": "conflict",
            "detail": "This agent run has already ended.",
        },
        content_type="application/problem+json",
    )

    with pytest.raises(PlaneAPIError) as caught:
        runs.stop("acme", "r1")

    assert caught.value.status == 409
    assert caught.value.code == "conflict"


def test_runs_cannot_be_deleted(runs: AgentRuns) -> None:
    """The API has no DELETE for a run -- it is settled, not removed."""
    assert not hasattr(runs, "delete")


# -- Activities on one run ----------------------------------------------------------


@responses.activate
def test_a_fetched_run_lists_its_activities_with_no_ids_repeated(runs: AgentRuns) -> None:
    responses.get(f"{RUNS}/r1/", json=RUN)
    responses.get(
        f"{RUNS}/r1/activities/",
        json={"data": [PROMPT], "pagination": {"style": "offset"}, "total_count": 1},
    )

    run = runs.retrieve("acme", "r1")
    page = run.activities.list(type__in=["prompt", "response"], expand=["actor"])

    assert responses.calls[1].request.url.startswith(f"{RUNS}/r1/activities/?")
    assert _query(1) == {"type__in": ["prompt,response"], "expand": ["actor"]}
    activity = page.data[0]
    assert isinstance(activity, AgentRunActivity)
    assert activity.content == {"type": "prompt", "body": "<p>Make it rhyme</p>"}
    assert activity.comment_id == "c2"


@responses.activate
def test_activities_create_and_retrieve_on_the_flat_path(config: Configuration) -> None:
    activities = V2Namespace(config).workspaces.agent_runs.activities
    responses.post(f"{RUNS}/r1/activities/", json=PROMPT, status=201)
    responses.get(f"{RUNS}/r1/activities/a1/", json=PROMPT)

    created = activities.create(
        "acme",
        "r1",
        CreateAgentRunActivity(
            type="prompt",
            content={"type": "prompt", "body": "<p>Make it rhyme</p>"},
            content_metadata={"idempotency_key": "k-1"},
        ),
    )
    fetched = activities.retrieve("acme", "r1", "a1", fields=["id", "type"])

    assert created.id == fetched.id == "a1"
    assert _body() == {
        "type": "prompt",
        "content": {"type": "prompt", "body": "<p>Make it rhyme</p>"},
        "content_metadata": {"idempotency_key": "k-1"},
    }
    assert _query(1) == {"fields": ["id,type"]}


@responses.activate
def test_iterate_activities_follows_offset_pages(config: Configuration) -> None:
    activities = V2Namespace(config).workspaces.agent_runs.activities
    responses.get(
        f"{RUNS}/r1/activities/",
        json={"data": [PROMPT], "next": 1, "pagination": {"style": "offset"}},
    )
    responses.get(
        f"{RUNS}/r1/activities/",
        json={"data": [{**PROMPT, "id": "a2"}], "next": None, "pagination": {"style": "offset"}},
    )

    assert [row.id for row in activities.iterate("acme", "r1", per_page=1)] == ["a1", "a2"]


def test_an_activity_needs_a_known_type() -> None:
    with pytest.raises(ValidationError):
        CreateAgentRunActivity(type="comment", content={"body": "x"})  # type: ignore[arg-type]


# -- The workspace-wide activity feed -----------------------------------------------


@responses.activate
def test_feed_polls_with_the_sync_filters(feed: WorkspaceAgentRunActivities) -> None:
    responses.get(
        f"{RUNS}/activities/",
        json={"data": [PROMPT], "pagination": {"style": "cursor"}, "has_more": False},
    )

    page = feed.list(
        "acme",
        agent_run_id="r1",
        created_at__gte="2026-11-10T09:00:00Z",
        signal="stop",
        paginate="cursor",
    )

    assert page.data[0].agent_run_id == "r1"
    assert _query() == {
        "agent_run_id": ["r1"],
        "created_at__gte": ["2026-11-10T09:00:00Z"],
        "signal": ["stop"],
        "paginate": ["cursor"],
    }


@responses.activate
def test_feed_iterate_walks_the_cursor(feed: WorkspaceAgentRunActivities) -> None:
    responses.get(
        f"{RUNS}/activities/",
        json={
            "data": [PROMPT],
            "pagination": {"style": "cursor"},
            "has_more": True,
            "next_cursor": "c-2",
        },
    )
    responses.get(
        f"{RUNS}/activities/",
        json={"data": [{**PROMPT, "id": "a2"}], "pagination": {"style": "cursor"}},
    )

    assert [row.id for row in feed.iterate("acme", paginate="cursor")] == ["a1", "a2"]
    assert _query(1)["cursor"] == ["c-2"]


# -- Navigation from a fetched workspace --------------------------------------------


@responses.activate
def test_a_fetched_workspace_reaches_runs_and_the_feed(config: Configuration) -> None:
    responses.get(f"{ROOT}/", json={"id": "ws-1", "slug": "acme"})
    responses.get(f"{RUNS}/r1/", json=RUN)
    responses.get(f"{RUNS}/r1/activities/", json={"data": [], "pagination": {"style": "offset"}})
    responses.get(f"{RUNS}/activities/", json={"data": [], "pagination": {"style": "offset"}})

    workspace = V2Namespace(config).workspaces.retrieve("acme")
    run = workspace.agent_runs.retrieve("r1")
    run.activities.list()
    workspace.agent_run_activities.list()

    assert [call.request.url.split("?")[0] for call in responses.calls] == [
        f"{ROOT}/",
        f"{RUNS}/r1/",
        f"{RUNS}/r1/activities/",
        f"{RUNS}/activities/",
    ]
