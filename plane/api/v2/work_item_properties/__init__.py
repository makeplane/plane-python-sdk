"""Work item properties (api_v2): custom field definitions on work items.
`WorkItemProperties` (project-scoped) and `WorkspaceWorkItemProperties`
(workspace-scoped) are independent resources -- own operationIds, own path -- each
with its own `.options`; the workspace one also has `.contexts`. A fetched row
comes back `Loaded` (`LoadedWorkItemProperty`/`LoadedWorkspaceWorkItemProperty`),
reaching its children (`.property_options`, and `.contexts` on the workspace
flavour) without repeating ids -- `property_options`, not `options`, because
`WorkItemProperty.options` is itself a real API field (inlined OPTION-type
choices for the property)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.work_item_properties import (
    CreateWorkItemProperty,
    UpdateWorkItemProperty,
    WorkItemProperty,
)
from .._generated.constants import (
    WorkItemPropertiesCreateField,
    WorkItemPropertiesListField,
    WorkItemPropertiesListFilters,
    WorkItemPropertiesListOrderBy,
    WorkItemPropertiesPartialUpdateField,
    WorkItemPropertiesRetrieveField,
    WorkspaceWorkItemPropertiesCreateField,
    WorkspaceWorkItemPropertiesListField,
    WorkspaceWorkItemPropertiesListFilters,
    WorkspaceWorkItemPropertiesListOrderBy,
    WorkspaceWorkItemPropertiesPartialUpdateField,
    WorkspaceWorkItemPropertiesRetrieveField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.work_item_property import LoadedWorkItemProperty, LoadedWorkspaceWorkItemProperty
from .contexts import WorkItemPropertyContexts
from .options import WorkItemPropertyOptions
from .workspace_options import WorkspaceWorkItemPropertyOptions

__all__ = [
    "WorkItemPropertyContexts",
    "WorkItemPropertyOptions",
    "WorkItemProperties",
    "WorkspaceWorkItemPropertyOptions",
    "WorkspaceWorkItemProperties",
]


class WorkItemProperties(
    V2Resource[WorkItemProperty, CreateWorkItemProperty, UpdateWorkItemProperty],
    LoadsNavigableRows[LoadedWorkItemProperty],
):
    """Project-scoped property definitions."""

    path = "/workspaces/{slug}/projects/{project_id}/work-item-properties/"
    model = WorkItemProperty
    loaded_model = LoadedWorkItemProperty
    loaded_names = ("slug", "project", "property")
    operations = {
        "list": "work_item_properties_list",
        "retrieve": "work_item_properties_retrieve",
        "create": "work_item_properties_create",
        "update": "work_item_properties_partial_update",
        "delete": "work_item_properties_destroy",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.options = WorkItemPropertyOptions(transport)

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[WorkItemPropertiesListField] | None = None,
        order_by: WorkItemPropertiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[WorkItemPropertiesListFilters],
    ) -> Page[LoadedWorkItemProperty]:
        """One page of this project's property definitions."""
        page = self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
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
        fields: Sequence[WorkItemPropertiesListField] | None = None,
        order_by: WorkItemPropertiesListOrderBy | None = None,
        **filters: Unpack[WorkItemPropertiesListFilters],
    ) -> Iterator[LoadedWorkItemProperty]:
        """Every property definition in this project, following pages automatically."""
        rows = self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
        )
        return (self._load(row, slug, project, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        project: str,
        property: str,
        *,
        fields: Sequence[WorkItemPropertiesRetrieveField] | None = None,
    ) -> LoadedWorkItemProperty:
        row = self._retrieve(pk=property, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def find_by_name(self, slug: str, project: str, name: str) -> LoadedWorkItemProperty:
        """The one property definition whose machine key matches `name`; raises if
        none or several match. `name` is the slugified key (e.g. `story_points`),
        not the label a user sees -- see `find_by_display_name` for that."""
        row = self._find_one(filters={"name": name}, slug=slug, project_id=project)
        return self._load(row, slug, project)

    def find_by_display_name(
        self, slug: str, project: str, display_name: str
    ) -> LoadedWorkItemProperty:
        """The one property definition whose UI label matches `display_name`
        (e.g. "Story Points"); raises if none or several match. This is what a
        user sees, not the machine key -- see `find_by_name` for that."""
        row = self._find_one(filters={"display_name": display_name}, slug=slug, project_id=project)
        return self._load(row, slug, project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateWorkItemProperty,
        *,
        fields: Sequence[WorkItemPropertiesCreateField] | None = None,
    ) -> LoadedWorkItemProperty:
        row = self._create(data, params={"fields": fields}, slug=slug, project_id=project)
        return self._load(row, slug, project, fields=fields)

    def update(
        self,
        slug: str,
        project: str,
        property: str,
        data: UpdateWorkItemProperty,
        *,
        fields: Sequence[WorkItemPropertiesPartialUpdateField] | None = None,
    ) -> LoadedWorkItemProperty:
        row = self._update(
            data, pk=property, params={"fields": fields}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def delete(self, slug: str, project: str, property: str) -> None:
        return self._delete(pk=property, slug=slug, project_id=project)


class WorkspaceWorkItemProperties(
    V2Resource[WorkItemProperty, CreateWorkItemProperty, UpdateWorkItemProperty],
    LoadsNavigableRows[LoadedWorkspaceWorkItemProperty],
):
    """Workspace-scoped property definitions -- not project-scoped, distinct from
    `WorkItemProperties` in the golden (own operationIds, own path)."""

    path = "/workspaces/{slug}/work-item-properties/"
    model = WorkItemProperty
    loaded_model = LoadedWorkspaceWorkItemProperty
    loaded_names = ("slug", "property")
    operations = {
        "list": "workspace_work_item_properties_list",
        "retrieve": "workspace_work_item_properties_retrieve",
        "create": "workspace_work_item_properties_create",
        "update": "workspace_work_item_properties_partial_update",
        "delete": "workspace_work_item_properties_destroy",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.contexts = WorkItemPropertyContexts(transport)
        self.options = WorkspaceWorkItemPropertyOptions(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceWorkItemPropertiesListField] | None = None,
        order_by: WorkspaceWorkItemPropertiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[WorkspaceWorkItemPropertiesListFilters],
    ) -> Page[LoadedWorkspaceWorkItemProperty]:
        """One page of this workspace's property definitions."""
        page = self._list(
            params={
                "fields": fields,
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
        fields: Sequence[WorkspaceWorkItemPropertiesListField] | None = None,
        order_by: WorkspaceWorkItemPropertiesListOrderBy | None = None,
        **filters: Unpack[WorkspaceWorkItemPropertiesListFilters],
    ) -> Iterator[LoadedWorkspaceWorkItemProperty]:
        """Every property definition in this workspace, following pages automatically."""
        rows = self._iter(params={"fields": fields, "order_by": order_by, **filters}, slug=slug)
        return (self._load(row, slug, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        property: str,
        *,
        fields: Sequence[WorkspaceWorkItemPropertiesRetrieveField] | None = None,
    ) -> LoadedWorkspaceWorkItemProperty:
        row = self._retrieve(pk=property, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def find_by_name(self, slug: str, name: str) -> LoadedWorkspaceWorkItemProperty:
        """The one property definition whose machine key matches `name`; raises if
        none or several match. `name` is the slugified key, not the label a user
        sees -- see `find_by_display_name` for that."""
        row = self._find_one(filters={"name": name}, slug=slug)
        return self._load(row, slug)

    def find_by_display_name(self, slug: str, display_name: str) -> LoadedWorkspaceWorkItemProperty:
        """The one property definition whose UI label matches `display_name`;
        raises if none or several match. This is what a user sees, not the
        machine key -- see `find_by_name` for that."""
        row = self._find_one(filters={"display_name": display_name}, slug=slug)
        return self._load(row, slug)

    def create(
        self,
        slug: str,
        data: CreateWorkItemProperty,
        *,
        fields: Sequence[WorkspaceWorkItemPropertiesCreateField] | None = None,
    ) -> LoadedWorkspaceWorkItemProperty:
        row = self._create(data, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def update(
        self,
        slug: str,
        property: str,
        data: UpdateWorkItemProperty,
        *,
        fields: Sequence[WorkspaceWorkItemPropertiesPartialUpdateField] | None = None,
    ) -> LoadedWorkspaceWorkItemProperty:
        row = self._update(data, pk=property, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def delete(self, slug: str, property: str) -> None:
        return self._delete(pk=property, slug=slug)
