"""Automation activities (api_v2). Read-only -- generated as a side effect of
automation writes/runs, never written directly. Project- and workspace-scoped
families mirror `ProjectAutomations`/`WorkspaceAutomations`: project-scoped
methods open with `slug, project, automation` (depth 3); workspace-scoped ones
open with `slug, automation` (depth 2). The golden declares no `expand` for
either family."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.automations import AutomationActivity
from .._generated.constants import (
    ProjectAutomationActivitiesListField,
    ProjectAutomationActivitiesListFilters,
    ProjectAutomationActivitiesListOrderBy,
    ProjectAutomationActivitiesRetrieveField,
    WorkspaceAutomationActivitiesListField,
    WorkspaceAutomationActivitiesListFilters,
    WorkspaceAutomationActivitiesListOrderBy,
    WorkspaceAutomationActivitiesRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource


class ProjectAutomationActivities(
    V2Resource[AutomationActivity, AutomationActivity, AutomationActivity]
):
    path = "/workspaces/{slug}/projects/{project_id}/automations/{automation_id}/activities/"
    model = AutomationActivity
    operations = {
        "list": "project_automation_activities_list",
        "retrieve": "project_automation_activities_retrieve",
    }

    def list(
        self,
        slug: str,
        project: str,
        automation: str,
        *,
        fields: Sequence[ProjectAutomationActivitiesListField] | None = None,
        order_by: ProjectAutomationActivitiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[ProjectAutomationActivitiesListFilters],
    ) -> Page[AutomationActivity]:
        """One page of activity entries on a project automation.

        `**filters` covers `field`, `verb`, `created_at__gt`."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
            project_id=project,
            automation_id=automation,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        automation: str,
        *,
        fields: Sequence[ProjectAutomationActivitiesListField] | None = None,
        order_by: ProjectAutomationActivitiesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[ProjectAutomationActivitiesListFilters],
    ) -> Iterator[AutomationActivity]:
        """Every activity entry on a project automation, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
            project_id=project,
            automation_id=automation,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        automation: str,
        activity: str,
        *,
        fields: Sequence[ProjectAutomationActivitiesRetrieveField] | None = None,
    ) -> AutomationActivity:
        return self._retrieve(
            pk=activity,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            automation_id=automation,
        )


class WorkspaceAutomationActivities(
    V2Resource[AutomationActivity, AutomationActivity, AutomationActivity]
):
    path = "/workspaces/{slug}/automations/{automation_id}/activities/"
    model = AutomationActivity
    operations = {
        "list": "workspace_automation_activities_list",
        "retrieve": "workspace_automation_activities_retrieve",
    }

    def list(
        self,
        slug: str,
        automation: str,
        *,
        fields: Sequence[WorkspaceAutomationActivitiesListField] | None = None,
        order_by: WorkspaceAutomationActivitiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkspaceAutomationActivitiesListFilters],
    ) -> Page[AutomationActivity]:
        """One page of activity entries on a workspace automation."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
            automation_id=automation,
        )

    def iterate(
        self,
        slug: str,
        automation: str,
        *,
        fields: Sequence[WorkspaceAutomationActivitiesListField] | None = None,
        order_by: WorkspaceAutomationActivitiesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkspaceAutomationActivitiesListFilters],
    ) -> Iterator[AutomationActivity]:
        """Every activity entry on a workspace automation, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
            automation_id=automation,
        )

    def retrieve(
        self,
        slug: str,
        automation: str,
        activity: str,
        *,
        fields: Sequence[WorkspaceAutomationActivitiesRetrieveField] | None = None,
    ) -> AutomationActivity:
        return self._retrieve(
            pk=activity, params={"fields": fields}, slug=slug, automation_id=automation
        )
