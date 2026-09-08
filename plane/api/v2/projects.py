"""Projects (api_v2). `project` accepts a UUID or its bare identifier (e.g.
`"ENG"`) everywhere -- no separate lookup needed. Adds `archive`/`unarchive`/
`summary`/`role_distribution`; no `bulk_delete` (delete cascades everything in it).

A fetched row (`retrieve`/`create`, and every row in a `list` page) comes back as
a `LoadedProject`: it carries the row's data and can reach `.states`/`.labels`
without the caller repeating `slug`/`project`.

The whole project band hangs off this class: `states`, `labels`, `work_items`,
`cycles`, `milestones`, `modules`, `estimates`, `intakes`, `members`, `views`,
`features`, `permissions`, `work_item_templates`, `worklogs` and `pages`. Every one
is migrated to the flat shape -- `tests/v2/test_tree.py`'s
`PROJECT_TREE_ATTACHMENTS` table proves each is the right class at the right URL,
and fails if a later plan attaches one without a row."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from typing_extensions import Unpack

from ...models.v2.common import BulkWriteResponse
from ...models.v2.project_role_distribution import ProjectRoleDistribution
from ...models.v2.projects import CreateProject, Project, ProjectSummary, UpdateProject
from ._generated.constants import (
    ProjectsCreateField,
    ProjectsListField,
    ProjectsListFilters,
    ProjectsListOrderBy,
    ProjectsPartialUpdateField,
    ProjectsRetrieveField,
    ProjectsUpsertField,
)
from ._kernel.loaded import LoadsNavigableRows
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport
from ._loaded.project import LoadedProject
from .cycles import Cycles
from .estimates import Estimates
from .features import ProjectFeatures
from .intakes import Intakes
from .labels import Labels
from .members import ProjectMembers
from .milestones import Milestones
from .modules import Modules
from .pages import ProjectPages
from .permissions import ProjectPermissions
from .states import States
from .views.project import ProjectViews
from .work_item_templates.project import ProjectWorkItemTemplates
from .work_items import WorkItems
from .worklogs import ProjectWorklogs


class Projects(
    V2Resource[Project, CreateProject, UpdateProject], LoadsNavigableRows[LoadedProject]
):
    path = "/workspaces/{slug}/projects/"
    extra_paths = {
        "role_distribution": "/workspaces/{slug}/project-role-distribution/",
    }
    model = Project
    loaded_model = LoadedProject
    loaded_names = ("slug", "project")
    operations = {
        "list": "projects_list",
        "retrieve": "projects_retrieve",
        "create": "projects_create",
        "update": "projects_partial_update",
        "upsert": "projects_upsert",
        "delete": "projects_destroy",
        "bulk_create": "projects_bulk_create",
        "bulk_update": "projects_bulk_update",
        "archive": "projects_archive",
        "unarchive": "projects_unarchive",
        "summary": "projects_summary",
        "role_distribution": "project_role_distribution",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.states = States(transport)
        self.labels = Labels(transport)
        self.work_items = WorkItems(transport)
        self.cycles = Cycles(transport)
        self.milestones = Milestones(transport)
        self.modules = Modules(transport)
        self.estimates = Estimates(transport)
        self.intakes = Intakes(transport)
        self.members = ProjectMembers(transport)
        self.views = ProjectViews(transport)
        self.features = ProjectFeatures(transport)
        self.permissions = ProjectPermissions(transport)
        self.work_item_templates = ProjectWorkItemTemplates(transport)
        self.worklogs = ProjectWorklogs(transport)
        self.pages = ProjectPages(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[ProjectsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ProjectsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[ProjectsListFilters],
    ) -> Page[LoadedProject]:
        """One page of projects in the workspace."""
        page = self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
        )
        return self._load_page(page, slug, fields=fields)

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[ProjectsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ProjectsListOrderBy | None = None,
        **filters: Unpack[ProjectsListFilters],
    ) -> Iterator[LoadedProject]:
        """Every project in the workspace, following pages automatically."""
        rows = self._iter(
            params={"fields": fields, "expand": expand, "order_by": order_by, **filters},
            slug=slug,
        )
        return (self._load(row, slug, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectsRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedProject:
        """Fetch a project. `project` accepts a UUID or its bare identifier
        (e.g. `"ENG"`) -- api_v2's flagship readable-identifier resource: no
        separate lookup is needed to go from a known key to a UUID."""
        row = self._retrieve(pk=project, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def find_by_name(self, slug: str, name: str) -> LoadedProject:
        """The one project with this name; raises if none or several match.

        Returns the same loaded row `retrieve` does -- a lookup that hands back a
        plain model would silently drop `.states`/`.labels`/`.work_items`."""
        row = self._find_one(filters={"name": name}, slug=slug)
        return self._load(row, slug)

    def create(
        self,
        slug: str,
        data: CreateProject,
        *,
        fields: Sequence[ProjectsCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedProject:
        row = self._create(data, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def update(
        self,
        slug: str,
        project: str,
        data: UpdateProject,
        *,
        fields: Sequence[ProjectsPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedProject:
        """`project` accepts a UUID or its bare identifier (e.g. `"ENG"`)."""
        row = self._update(data, pk=project, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def delete(self, slug: str, project: str) -> None:
        """`project` accepts a UUID or its bare identifier (e.g. `"ENG"`).
        Deleting a project cascades its work items, cycles, modules, pages and
        members."""
        return self._delete(pk=project, slug=slug)

    def upsert(
        self,
        slug: str,
        data: CreateProject,
        *,
        fields: Sequence[ProjectsUpsertField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedProject:
        """Reconciles on (external_source, external_id) when both are set."""
        row = self._upsert(data, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def bulk_create(
        self,
        slug: str,
        items: builtins.list[CreateProject],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_create(items, all_or_none=all_or_none, slug=slug)

    def bulk_update(
        self,
        slug: str,
        items: builtins.list[Mapping[str, object]],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`. No `bulk_delete`
        exists for projects -- use `delete` per project."""
        return self._bulk_update(items, all_or_none=all_or_none, slug=slug)

    # -- Custom actions -----------------------------------------------------------
    # None go through `_action`: response shapes/bodies don't match `self.model`.

    def archive(self, slug: str, project: str) -> None:
        """Archive a project. 204, no response body."""
        return self._void_action("archive", pk=project, slug=slug)

    def unarchive(self, slug: str, project: str) -> None:
        """Restore an archived project. 204, no response body."""
        return self._void_action("unarchive", pk=project, slug=slug)

    def summary(
        self,
        slug: str,
        project: str,
        *,
        counts: Sequence[str] | None = None,
    ) -> ProjectSummary:
        """Project identity plus resource counts (v1 summary parity).

        `counts` narrows the response to specific count keys; omit for all of them."""
        payload = self.transport.request(
            "GET",
            f"{self._detail_url(project, slug=slug)}summary/",
            params=self._query({"counts": counts}, action="summary"),
        )
        return ProjectSummary.model_validate(payload)

    def role_distribution(self, slug: str) -> ProjectRoleDistribution:
        """Workspace-wide counts of members per project role. A single read-only
        report, not a paginated collection -- one object per workspace, no `id`."""
        payload = self.transport.request("GET", self.url_for("role_distribution", slug=slug))
        return ProjectRoleDistribution.model_validate(payload)

    # -- Navigation -----------------------------------------------------------------

    def _row_id(self, row: Project) -> Any:
        """Children address a project by its readable identifier where the server
        returned one -- `.../projects/ENG/states/`, not the UUID."""
        return row.identifier or row.id
