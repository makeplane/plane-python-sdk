"""Automation activities (api_v2). Read-only -- generated as a side effect of
automation writes/runs, never written directly. Project- and workspace-scoped
families mirror `ProjectAutomations`/`WorkspaceAutomations`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.automations import AutomationActivity
from .._kernel.pagination import Page
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
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[AutomationActivity]:
        """One page of activity entries on a project automation.

        `**filters` covers `verb`, `field`, `created_at__gt`, etc."""
        return self._list(automation_id=automation_id, params={"fields": fields, **filters})

    def iterate(
        self,
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[AutomationActivity]:
        """Every activity entry on a project automation, following pages automatically."""
        return self._iter(automation_id=automation_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        automation_id: str,
        activity_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> AutomationActivity:
        return self._retrieve(
            pk=activity_id, automation_id=automation_id, params={"fields": fields}
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
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[AutomationActivity]:
        """One page of activity entries on a workspace automation."""
        return self._list(automation_id=automation_id, params={"fields": fields, **filters})

    def iterate(
        self,
        automation_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[AutomationActivity]:
        """Every activity entry on a workspace automation, following pages automatically."""
        return self._iter(automation_id=automation_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        automation_id: str,
        activity_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> AutomationActivity:
        return self._retrieve(
            pk=activity_id, automation_id=automation_id, params={"fields": fields}
        )
