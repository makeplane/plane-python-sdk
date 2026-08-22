"""Projects (api_v2). `project` accepts a UUID or its bare identifier (e.g.
`"ENG"`) everywhere -- no separate lookup needed. Adds `archive`/`unarchive`/
`summary`/`role_distribution`; no `bulk_delete` (delete cascades everything in it)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any
from urllib.parse import quote

from ...models.v2.common import BulkWriteResponse
from ...models.v2.project_role_distribution import ProjectRoleDistribution
from ...models.v2.projects import CreateProject, Project, ProjectSummary, UpdateProject
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


class Projects(V2Resource[Project, CreateProject, UpdateProject]):
    path = "/workspaces/{slug}/projects/"
    model = Project
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

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Project]:
        """One page of projects in the workspace.

        `**filters` covers `name`, `identifier`, `network`, `priority`, `is_archived`."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Project]:
        """Every project in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        project: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Project:
        """Fetch a project. `project` accepts a UUID or its bare identifier
        (e.g. `"ENG"`) -- api_v2's flagship readable-identifier resource: no
        separate lookup is needed to go from a known key to a UUID."""
        return self._retrieve(pk=project, params={"fields": fields, "expand": expand})

    def find_by_name(self, name: str) -> Project:
        """The one project with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateProject) -> Project:
        return self._create(data)

    def update(self, project: str, data: UpdateProject) -> Project:
        """`project` accepts a UUID or its bare identifier (e.g. `"ENG"`)."""
        return self._update(data, pk=project)

    def delete(self, project: str) -> None:
        """`project` accepts a UUID or its bare identifier (e.g. `"ENG"`).
        Deleting a project cascades its work items, cycles, modules, pages and
        members."""
        return self._delete(pk=project)

    def upsert(self, data: CreateProject) -> Project:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data)

    def bulk_create(
        self,
        items: builtins.list[CreateProject],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_create(items, all_or_none=all_or_none)

    def bulk_update(
        self,
        items: builtins.list[Mapping[str, Any]],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`. No `bulk_delete`
        exists for projects -- use `delete` per project."""
        return self._bulk_update(items, all_or_none=all_or_none)

    # -- Custom actions -----------------------------------------------------------
    # None go through `_action`: response shapes/bodies don't match `self.model`.

    def archive(self, project: str) -> None:
        """Archive a project. 204, no response body."""
        self.transport.request("POST", f"{self._detail_url(project)}archive/")
        return None

    def unarchive(self, project: str) -> None:
        """Restore an archived project. 204, no response body."""
        self.transport.request("POST", f"{self._detail_url(project)}unarchive/")
        return None

    def summary(self, project: str, *, counts: Sequence[str] | None = None) -> ProjectSummary:
        """Project identity plus resource counts (v1 summary parity).

        `counts` narrows the response to specific count keys; omit for all of them."""
        params: dict[str, Any] = {}
        if counts is not None:
            params["counts"] = ",".join(counts) if not isinstance(counts, str) else counts
        payload = self.transport.request(
            "GET", f"{self._detail_url(project)}summary/", params=params or None
        )
        return ProjectSummary.model_validate(payload)

    def role_distribution(self) -> ProjectRoleDistribution:
        """Workspace-wide counts of members per project role. A single read-only
        report, not a paginated collection -- one object per workspace, no `id`."""
        payload = self.transport.request("GET", self._role_distribution_url())
        return ProjectRoleDistribution.model_validate(payload)

    def _role_distribution_url(self) -> str:
        # A sibling path of this resource's own collection URL, not a sub-path of it.
        slug = self._scope["slug"]
        return f"/workspaces/{quote(str(slug), safe='')}/project-role-distribution/"
