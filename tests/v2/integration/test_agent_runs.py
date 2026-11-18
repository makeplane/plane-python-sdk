"""Live coverage for agent runs: `client.v2.workspaces.agent_runs`, a run's `activities`,
the workspace-wide `agent_run_activities` feed, and the run fields on work item comments.

A person (the suite's api-key `client`) starts a run on a comment, prompts it and stops
it; the agent itself (`agent_client`, the app bot's access token) reports on its own run.
Both principals matter: the API splits the writes between them and refuses the wrong one.
Needs `AGENT_SLUG` (and `AGENT_BOT_TOKEN` for the agent's half); without them those tests
skip as a declared capability gap.

Runs are reached off the loaded `workspace` row and a fetched run's own `activities`, so
the slug and run id are written once; the comment checks use the loaded work item."""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedAgentRun, LoadedProject, LoadedWorkspace, PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.agent_runs import CreateAgentRun, CreateAgentRunActivity, UpdateAgentRun
from plane.models.v2.work_items import CreateWorkItem, CreateWorkItemComment

from .helpers import unique_name

SYNC_HOLD_BACK_SECONDS = 3.5
"""A sync read (a cursor walk or a `*__gte` poll) holds back rows stamped in the last 3
seconds; waiting a little longer makes a just-written row visible to one."""


@pytest.fixture
def work_item(project: LoadedProject) -> Iterator[Any]:
    created = project.work_items.create(CreateWorkItem(name=unique_name("wi-agent-run")))
    yield created
    try:
        project.work_items.delete(created.id)
    except Exception:
        pass


@pytest.fixture
def thread(work_item: Any) -> Any:
    """The top-level comment a run is started on -- it becomes the run's thread root."""
    return work_item.comments.create(
        CreateWorkItemComment(comment_html="<p>Write a poem about this work item</p>")
    )


@pytest.fixture
def run(workspace: LoadedWorkspace, agent_slug: str, thread: Any) -> LoadedAgentRun:
    """A run the person started. Runs can't be deleted -- the work item's cleanup is the
    only teardown there is."""
    return workspace.agent_runs.create(
        CreateAgentRun(agent_slug=agent_slug, comment_id=thread.id, title=unique_name("run"))
    )


class TestRunsAsAPerson:
    def test_create_takes_the_comments_work_item(
        self, run: LoadedAgentRun, thread: Any, work_item: Any
    ) -> None:
        assert run.comment_id == thread.id
        assert run.source_comment_id == thread.id
        assert run.work_item_id == work_item.id
        assert run.status in {"created", "in_progress"}
        assert run.type == "comment_thread"

    def test_retrieve_expands_the_thread_comment_and_work_item(
        self, workspace: LoadedWorkspace, run: LoadedAgentRun, thread: Any, work_item: Any
    ) -> None:
        fetched = workspace.agent_runs.retrieve(run.id, expand=["comment", "work_item"])

        body = fetched.model_dump()
        assert body["comment"]["id"] == thread.id
        assert body["work_item"]["id"] == work_item.id

    def test_list_filters_by_work_item_and_status(
        self, workspace: LoadedWorkspace, run: LoadedAgentRun, work_item: Any
    ) -> None:
        page = workspace.agent_runs.list(
            work_item_id=work_item.id, status__in=["created", "in_progress", "awaiting"]
        )
        assert [row.id for row in page.data] == [run.id]

        none = workspace.agent_runs.list(work_item_id=work_item.id, status="completed")
        assert none.data == []

    def test_a_cursor_walk_reaches_the_run_once_the_hold_back_passes(
        self, workspace: LoadedWorkspace, run: LoadedAgentRun, work_item: Any
    ) -> None:
        time.sleep(SYNC_HOLD_BACK_SECONDS)

        rows = list(
            workspace.agent_runs.iterate(work_item_id=work_item.id, paginate="cursor", per_page=1)
        )

        assert [row.id for row in rows] == [run.id]
        assert rows[0].activities._ids[-1] == run.id

    def test_a_person_cannot_update_a_run(
        self, workspace: LoadedWorkspace, run: LoadedAgentRun
    ) -> None:
        with pytest.raises(PlaneAPIError) as caught:
            workspace.agent_runs.update(run.id, UpdateAgentRun(summary="forged"))
        assert caught.value.status == 403

    def test_stop_moves_the_run_to_stopping_and_only_once(
        self, workspace: LoadedWorkspace, run: LoadedAgentRun
    ) -> None:
        stopped = workspace.agent_runs.stop(run.id)
        assert stopped.status == "stopping"

        with pytest.raises(PlaneAPIError) as caught:
            workspace.agent_runs.stop(run.id)
        assert caught.value.status == 409

        signals = [row.signal for row in stopped.activities.iterate(type="prompt")]
        assert "stop" in signals

    def test_an_unknown_run_is_a_404(self, workspace: LoadedWorkspace) -> None:
        with pytest.raises(PlaneAPIError) as caught:
            workspace.agent_runs.retrieve("00000000-0000-4000-8000-000000000000")
        assert caught.value.status == 404


class TestActivitiesAsAPerson:
    def test_a_prompt_is_logged_and_mirrored_into_the_thread(
        self, workspace: LoadedWorkspace, run: LoadedAgentRun, work_item: Any
    ) -> None:
        prompt = run.activities.create(
            CreateAgentRunActivity(
                type="prompt",
                content={"type": "prompt", "body": "<p>Make it rhyme</p>"},
                content_metadata={"client_ref": "sdk-it"},
            )
        )

        assert prompt.type == "prompt"
        assert prompt.agent_run_id == run.id
        assert prompt.content_metadata == {"client_ref": "sdk-it"}
        assert prompt.comment_id is not None, "a person's prompt is mirrored as a thread reply"

        fetched = run.activities.retrieve(prompt.id, expand=["actor"])
        assert fetched.content == {"type": "prompt", "body": "<p>Make it rhyme</p>"}

        logged = {row.id for row in run.activities.iterate(type="prompt")}
        assert prompt.id in logged

        reply = work_item.comments.retrieve(prompt.comment_id)
        assert "Make it rhyme" in (reply.comment_html or "")

    def test_the_workspace_feed_carries_the_runs_activity(
        self, workspace: LoadedWorkspace, run: LoadedAgentRun
    ) -> None:
        prompt = run.activities.create(
            CreateAgentRunActivity(type="prompt", content={"type": "prompt", "body": "<p>Go</p>"})
        )

        page = workspace.agent_run_activities.list(agent_run_id=run.id, type="prompt")
        assert prompt.id in {row.id for row in page.data}

        assert prompt.created_at is not None
        time.sleep(SYNC_HOLD_BACK_SECONDS)
        polled = workspace.agent_run_activities.iterate(
            agent_run_id=run.id, created_at__gte=prompt.created_at.isoformat(), paginate="cursor"
        )
        assert prompt.id in {row.id for row in polled}

    def test_a_person_cannot_post_the_agents_output(self, run: LoadedAgentRun) -> None:
        with pytest.raises(PlaneAPIError) as caught:
            run.activities.create(
                CreateAgentRunActivity(
                    type="response", content={"type": "response", "body": "forged"}
                )
            )
        assert caught.value.status == 400


class TestCommentsCarryTheRun:
    def test_the_thread_comment_names_its_run(
        self, run: LoadedAgentRun, thread: Any, work_item: Any
    ) -> None:
        fetched = work_item.comments.retrieve(thread.id, expand=["agent_run"])

        assert fetched.agent_run_id == run.id
        assert fetched.agent_run is not None
        assert fetched.agent_run.id == run.id
        assert fetched.agent_run.agent_user_id == run.agent_user_id

    def test_comments_filter_by_agent_run_id(
        self, run: LoadedAgentRun, thread: Any, work_item: Any
    ) -> None:
        work_item.comments.create(CreateWorkItemComment(comment_html="<p>unrelated</p>"))

        page = work_item.comments.list(agent_run_id=run.id, fields=["id", "agent_run_id"])

        assert [(row.id, row.agent_run_id) for row in page.data] == [(thread.id, run.id)]


class TestRunsAsTheAgent:
    def test_the_agent_reports_and_completes_its_run(
        self, agent_client: PlaneClient, workspace_slug: str, run: LoadedAgentRun
    ) -> None:
        agent_runs = agent_client.v2.workspaces.agent_runs
        mine = agent_runs.retrieve(workspace_slug, run.id)

        thought = mine.activities.create(
            CreateAgentRunActivity(
                type="thought", content={"type": "thought", "body": "Reading the work item"}
            )
        )
        assert thought.type == "thought"

        done = agent_runs.update(
            workspace_slug,
            run.id,
            UpdateAgentRun(status="completed", summary="Wrote the poem.", token_usage={"in": 7}),
        )
        assert done.status == "completed"
        assert done.summary == "Wrote the poem."
        assert done.ended_at is not None

    def test_the_agent_lists_its_own_runs(
        self, agent_client: PlaneClient, workspace_slug: str, run: LoadedAgentRun
    ) -> None:
        assert run.agent_user_id is not None and run.work_item_id is not None
        page = agent_client.v2.workspaces.agent_runs.list(
            workspace_slug, agent_user_id=run.agent_user_id, work_item_id=run.work_item_id
        )
        assert [row.id for row in page.data] == [run.id]

    def test_the_agent_cannot_stop_its_run(
        self, agent_client: PlaneClient, workspace_slug: str, run: LoadedAgentRun
    ) -> None:
        with pytest.raises(PlaneAPIError) as caught:
            agent_client.v2.workspaces.agent_runs.stop(workspace_slug, run.id)
        assert caught.value.status == 403
