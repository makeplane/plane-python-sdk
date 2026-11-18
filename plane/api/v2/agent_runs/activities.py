"""Agent run activities (api_v2) -- a run's append-only log, and the one feed of the
activities on every run the caller can see.

Both list oldest first (`created_at`) and page by cursor on `(created_at, id)`. There is
no update or delete: an activity, once written, stays."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.agent_runs import AgentRunActivity, CreateAgentRunActivity
from .._generated.constants import (
    RunActivitiesCreateField,
    RunActivitiesListField,
    RunActivitiesListFilters,
    RunActivitiesListOrderBy,
    RunActivitiesRetrieveField,
    WorkspaceRunActivitiesListField,
    WorkspaceRunActivitiesListFilters,
    WorkspaceRunActivitiesListOrderBy,
)
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource

__all__ = ["AgentRunActivities", "WorkspaceAgentRunActivities"]


# No patch DTO exists for activities -- the third type parameter is filled with the
# write model as an unused placeholder: the kernel has no append-only resource shape.
class AgentRunActivities(
    V2Resource[AgentRunActivity, CreateAgentRunActivity, CreateAgentRunActivity]
):
    """`/workspaces/{slug}/runs/{run_id}/activities/` -- one run's log.

    Reach it off a fetched run (`run.activities.list()`) or on the flat path
    (`client.v2.workspaces.agent_runs.activities.list(slug, run)`). A run the caller
    can't see answers 404 on every method here."""

    path = "/workspaces/{slug}/runs/{run_id}/activities/"
    model = AgentRunActivity
    operations = {
        "list": "run_activities_list",
        "retrieve": "run_activities_retrieve",
        "create": "run_activities_create",
    }

    def list(
        self,
        slug: str,
        run: str,
        *,
        fields: Sequence[RunActivitiesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: RunActivitiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[RunActivitiesListFilters],
    ) -> Page[AgentRunActivity]:
        """One page of the run's activities, oldest first. Filter with `type` /
        `type__in`, `signal`, `ephemeral`, `actor_id`, `comment_id` or `created_at__gte`;
        `expand=["actor"]` inlines who wrote each one."""
        return self._list(
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
            run_id=run,
        )

    def iterate(
        self,
        slug: str,
        run: str,
        *,
        fields: Sequence[RunActivitiesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: RunActivitiesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[RunActivitiesListFilters],
    ) -> Iterator[AgentRunActivity]:
        """Every activity on the run, following pages automatically."""
        return self._iter(
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
            run_id=run,
        )

    def retrieve(
        self,
        slug: str,
        run: str,
        activity: str,
        *,
        fields: Sequence[RunActivitiesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> AgentRunActivity:
        return self._retrieve(
            pk=activity, params={"fields": fields, "expand": expand}, slug=slug, run_id=run
        )

    def create(
        self,
        slug: str,
        run: str,
        data: CreateAgentRunActivity,
        *,
        fields: Sequence[RunActivitiesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> AgentRunActivity:
        """Append to the run's log. The run's agent (a bot token) posts its output --
        `thought`, `action`, `response`, `elicitation` or `error`; a person may only post
        a `prompt` (`content={"type": "prompt", "body": ...}`), which the server mirrors
        into the work item's thread as a reply and answers with that reply's
        `comment_id`. A person must be able to comment on the run's work item."""
        return self._create(
            data, params={"fields": fields, "expand": expand}, slug=slug, run_id=run
        )


# Read-only -- the type parameters are filled with the read model itself as an unused
# placeholder: the kernel has no read-only resource shape.
class WorkspaceAgentRunActivities(V2Resource[AgentRunActivity, AgentRunActivity, AgentRunActivity]):
    """`/workspaces/{slug}/runs/activities/` -- one feed of the activities on every run
    the caller can see (for a bot token, every activity on its own runs), so an agent
    keeps a single cursor instead of polling run by run.

    Workspace-scoped, so it hangs off the workspace
    (`client.v2.workspaces.agent_run_activities`), not off a run."""

    path = "/workspaces/{slug}/runs/activities/"
    model = AgentRunActivity
    operations = {"list": "workspace_run_activities_list"}

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceRunActivitiesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkspaceRunActivitiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkspaceRunActivitiesListFilters],
    ) -> Page[AgentRunActivity]:
        """One page of the feed, oldest first. Filter with `agent_run_id`, `type` /
        `type__in`, `signal`, `ephemeral`, `actor_id`, `comment_id` or `created_at__gte`.

        A sync read -- a cursor walk or a `created_at__gte=` poll -- holds back
        activities written in the last 3 seconds until a later read, so dedupe by
        `id`."""
        return self._list(
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

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceRunActivitiesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkspaceRunActivitiesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkspaceRunActivitiesListFilters],
    ) -> Iterator[AgentRunActivity]:
        """The whole feed, following pages automatically."""
        return self._iter(
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
