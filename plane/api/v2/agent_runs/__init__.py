"""Agent runs (api_v2) -- `/workspaces/{slug}/runs/`: the work an agent (an installed
app's bot) does in a workspace, usually in answer to a work item comment. A run's
append-only log is its `.activities`; the activities on every run at once are
`client.v2.workspaces.agent_run_activities`.

Who sees what:
- a bot token sees only its own runs: another agent's run is absent from a list and
  answers 404 by id;
- a person sees a run only if they can see its work item; a run with no work item (a
  scheduled native-agent run, say) is visible to every workspace admin and member;
- guests can't use agent runs at all.

Who may write: a person starts a run on a comment (`create`), replies with a `prompt`
activity and asks a run to `stop`; only the run's agent may `update` it (settling it as
`completed`) or post its output activities.

Polling: `list(..., paginate="cursor")` walks oldest change first (`updated_at`), and a
sync read -- a cursor walk or an `updated_at__gte=` poll -- holds back rows changed in the
last 3 seconds, so a run updated mid-walk is read again rather than skipped. Dedupe by
`id`. Webhooks for agent runs carry the same payload as v1, whichever API version made
the change.

A fetched row comes back as a `LoadedAgentRun`, which reaches `run.activities.list()`
without repeating `slug`/`run`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.agent_runs import AgentRun, CreateAgentRun, UpdateAgentRun
from .._generated.constants import (
    RunsCreateField,
    RunsListField,
    RunsListFilters,
    RunsListOrderBy,
    RunsPartialUpdateField,
    RunsRetrieveField,
    RunsStopField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.agent_run import LoadedAgentRun
from .activities import AgentRunActivities, WorkspaceAgentRunActivities

__all__ = ["AgentRunActivities", "AgentRuns", "WorkspaceAgentRunActivities"]


class AgentRuns(
    V2Resource[AgentRun, CreateAgentRun, UpdateAgentRun], LoadsNavigableRows[LoadedAgentRun]
):
    """There is no `delete`: a run is settled, not removed."""

    path = "/workspaces/{slug}/runs/"
    model = AgentRun
    loaded_model = LoadedAgentRun
    loaded_names = ("slug", "run")
    operations = {
        "list": "runs_list",
        "retrieve": "runs_retrieve",
        "create": "runs_create",
        "update": "runs_partial_update",
        "stop": "runs_stop",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.activities = AgentRunActivities(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[RunsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: RunsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[RunsListFilters],
    ) -> Page[LoadedAgentRun]:
        """One page of the runs the caller can see, oldest change first (`updated_at`).

        Filter with `agent_user_id`, `status` / `status__in`, `type`, `trigger_type`,
        `work_item_id`, `project_id` or `updated_at__gte`. `expand` takes `agent_user`,
        `creator`, `work_item`, `comment` and `source_comment`. With `paginate="cursor"`
        or `updated_at__gte`, rows changed in the last 3 seconds are held back until a
        later read -- dedupe by `id`."""
        page = self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
        )
        return self._load_page(page, slug, fields=fields)

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[RunsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: RunsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[RunsListFilters],
    ) -> Iterator[LoadedAgentRun]:
        """Every run the caller can see, following pages automatically."""
        rows = self._iter(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )
        return (self._load(row, slug, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        run: str,
        *,
        fields: Sequence[RunsRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedAgentRun:
        """A run by id. One the caller can't see answers 404, never 403."""
        row = self._retrieve(pk=run, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def create(
        self,
        slug: str,
        data: CreateAgentRun,
        *,
        fields: Sequence[RunsCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedAgentRun:
        """Start a run of the agent `data.agent_slug` on the top-level comment
        `data.comment_id`. A person must be able to comment on that comment's work item;
        a bot token may start only its own runs."""
        row = self._create(data, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def update(
        self,
        slug: str,
        run: str,
        data: UpdateAgentRun,
        *,
        fields: Sequence[RunsPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedAgentRun:
        """The run's agent reports its title, summary and usage, and settles the run with
        `status="completed"`. Bot tokens only: a person gets 403 and ends a run with
        `stop` instead."""
        row = self._update(data, pk=run, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def stop(
        self,
        slug: str,
        run: str,
        *,
        fields: Sequence[RunsStopField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedAgentRun:
        """Ask the run to stop -- the web app's Stop button. Records a `prompt` activity
        with `signal="stop"` and moves the run to `stopping`; the agent's next response
        settles it as `stopped`. People only: a bot token gets 403 (an agent ends its own
        run with `update(status="completed")` or an `error` activity). 409 if the run
        has already ended or is already stopping."""
        row = self._action("stop", pk=run, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)
