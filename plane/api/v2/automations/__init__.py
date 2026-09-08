"""Automations (api_v2). Project- and workspace-scoped families have their own
path templates/operationIds, hence separate `ProjectAutomations`/`WorkspaceAutomations`
classes -- project-scoped methods open with `slug, project` (their own `automation`
pk on top), workspace-scoped ones open with just `slug`. `set_status` (204, no body)
is the only way to enable/disable one, and is a custom action on both. A fetched row
comes back `Loaded` (`LoadedProjectAutomation`/`LoadedWorkspaceAutomation`), reaching
`.edges`, `.nodes` and `.activities` without repeating ids."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.automations import (
    Automation,
    CreateAutomation,
    SetAutomationStatus,
    UpdateAutomation,
)
from .._generated.constants import (
    ProjectAutomationsCreateField,
    ProjectAutomationsListField,
    ProjectAutomationsListFilters,
    ProjectAutomationsListOrderBy,
    ProjectAutomationsPartialUpdateField,
    ProjectAutomationsRetrieveField,
    WorkspaceAutomationsCreateField,
    WorkspaceAutomationsListField,
    WorkspaceAutomationsListFilters,
    WorkspaceAutomationsListOrderBy,
    WorkspaceAutomationsPartialUpdateField,
    WorkspaceAutomationsRetrieveField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.automation import LoadedProjectAutomation, LoadedWorkspaceAutomation
from .activities import ProjectAutomationActivities, WorkspaceAutomationActivities
from .edges import ProjectAutomationEdges, WorkspaceAutomationEdges
from .nodes import ProjectAutomationNodes, WorkspaceAutomationNodes

__all__ = [
    "ProjectAutomationActivities",
    "ProjectAutomationEdges",
    "ProjectAutomationNodes",
    "ProjectAutomations",
    "WorkspaceAutomationActivities",
    "WorkspaceAutomationEdges",
    "WorkspaceAutomationNodes",
    "WorkspaceAutomations",
]


class ProjectAutomations(
    V2Resource[Automation, CreateAutomation, UpdateAutomation],
    LoadsNavigableRows[LoadedProjectAutomation],
):
    path = "/workspaces/{slug}/projects/{project_id}/automations/"
    model = Automation
    loaded_model = LoadedProjectAutomation
    loaded_names = ("slug", "project", "automation")
    operations = {
        "list": "project_automations_list",
        "retrieve": "project_automations_retrieve",
        "create": "project_automations_create",
        "update": "project_automations_partial_update",
        "delete": "project_automations_destroy",
        "status": "project_automations_status",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.edges = ProjectAutomationEdges(transport)
        self.nodes = ProjectAutomationNodes(transport)
        self.activities = ProjectAutomationActivities(transport)

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectAutomationsListField] | None = None,
        order_by: ProjectAutomationsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[ProjectAutomationsListFilters],
    ) -> Page[LoadedProjectAutomation]:
        """One page of automations in this project.

        `**filters` covers `is_enabled`, `is_global`, `name`, `scope`, `status`, `search`."""
        page = self._list(
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
        )
        return self._load_page(page, slug, project, fields=fields)

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectAutomationsListField] | None = None,
        order_by: ProjectAutomationsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[ProjectAutomationsListFilters],
    ) -> Iterator[LoadedProjectAutomation]:
        """Every automation in this project, following pages automatically."""
        rows = self._iter(
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
        )
        return (self._load(row, slug, project, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        project: str,
        automation: str,
        *,
        fields: Sequence[ProjectAutomationsRetrieveField] | None = None,
    ) -> LoadedProjectAutomation:
        row = self._retrieve(
            pk=automation, params={"fields": fields}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def find_by_name(self, slug: str, project: str, name: str) -> LoadedProjectAutomation:
        """The one automation with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug, project_id=project)
        return self._load(row, slug, project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateAutomation,
        *,
        fields: Sequence[ProjectAutomationsCreateField] | None = None,
    ) -> LoadedProjectAutomation:
        row = self._create(data, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def update(
        self,
        slug: str,
        project: str,
        automation: str,
        data: UpdateAutomation,
        *,
        fields: Sequence[ProjectAutomationsPartialUpdateField] | None = None,
    ) -> LoadedProjectAutomation:
        row = self._update(
            data, pk=automation, params={"fields": fields}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def delete(self, slug: str, project: str, automation: str) -> None:
        return self._delete(pk=automation, slug=slug, project_id=project)

    def set_status(self, slug: str, project: str, automation: str, *, is_enabled: bool) -> None:
        """Enable/disable a project automation (and move it out of draft). 204, no
        row returned -- a custom action through the kernel's `_void_action`, not a
        hand-built URL."""
        data = SetAutomationStatus(is_enabled=is_enabled)
        return self._void_action("status", pk=automation, data=data, slug=slug, project_id=project)


class WorkspaceAutomations(
    V2Resource[Automation, CreateAutomation, UpdateAutomation],
    LoadsNavigableRows[LoadedWorkspaceAutomation],
):
    path = "/workspaces/{slug}/automations/"
    model = Automation
    loaded_model = LoadedWorkspaceAutomation
    loaded_names = ("slug", "automation")
    operations = {
        "list": "workspace_automations_list",
        "retrieve": "workspace_automations_retrieve",
        "create": "workspace_automations_create",
        "update": "workspace_automations_partial_update",
        "delete": "workspace_automations_destroy",
        "status": "workspace_automations_status",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.edges = WorkspaceAutomationEdges(transport)
        self.nodes = WorkspaceAutomationNodes(transport)
        self.activities = WorkspaceAutomationActivities(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceAutomationsListField] | None = None,
        order_by: WorkspaceAutomationsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkspaceAutomationsListFilters],
    ) -> Page[LoadedWorkspaceAutomation]:
        """One page of workspace-level (global, not-project-tied) automations."""
        page = self._list(
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
        )
        return self._load_page(page, slug, fields=fields)

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceAutomationsListField] | None = None,
        order_by: WorkspaceAutomationsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkspaceAutomationsListFilters],
    ) -> Iterator[LoadedWorkspaceAutomation]:
        """Every workspace-level automation, following pages automatically."""
        rows = self._iter(
            params={
                "fields": fields,
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
        automation: str,
        *,
        fields: Sequence[WorkspaceAutomationsRetrieveField] | None = None,
    ) -> LoadedWorkspaceAutomation:
        row = self._retrieve(pk=automation, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def find_by_name(self, slug: str, name: str) -> LoadedWorkspaceAutomation:
        """The one automation with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug)
        return self._load(row, slug)

    def create(
        self,
        slug: str,
        data: CreateAutomation,
        *,
        fields: Sequence[WorkspaceAutomationsCreateField] | None = None,
    ) -> LoadedWorkspaceAutomation:
        row = self._create(data, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def update(
        self,
        slug: str,
        automation: str,
        data: UpdateAutomation,
        *,
        fields: Sequence[WorkspaceAutomationsPartialUpdateField] | None = None,
    ) -> LoadedWorkspaceAutomation:
        row = self._update(data, pk=automation, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def delete(self, slug: str, automation: str) -> None:
        return self._delete(pk=automation, slug=slug)

    def set_status(self, slug: str, automation: str, *, is_enabled: bool) -> None:
        """Enable/disable a workspace automation (and move it out of draft). 204, no
        row returned -- a custom action through the kernel's `_void_action`, not a
        hand-built URL."""
        data = SetAutomationStatus(is_enabled=is_enabled)
        return self._void_action("status", pk=automation, data=data, slug=slug)
