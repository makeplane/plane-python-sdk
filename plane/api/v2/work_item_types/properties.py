"""Custom properties linked to a work item type (api_v2), project- and
workspace-scoped. `link` POSTs to the *collection* URL with
`{"properties": [...]}`, returning the full set of linked property ids -- not a
`WorkItemProperty` row -- so it goes through the kernel's `_custom_action`, not
`_create`. `unlink` deletes a property's attachment by its own id; this also
deletes that property's values on every work item of the type. Both names come
from the web app's own wording and are kept deliberately."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from ....models.v2.work_item_types import (
    WorkItemProperty,
    WorkItemPropertyAttach,
    WorkItemPropertyAttachResult,
)
from .._generated.constants import (
    WorkItemTypePropertiesListField,
    WorkItemTypePropertiesListOrderBy,
    WorkItemTypePropertiesRetrieveField,
    WorkspaceWorkItemTypePropertiesListField,
    WorkspaceWorkItemTypePropertiesListOrderBy,
    WorkspaceWorkItemTypePropertiesRetrieveField,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkItemTypeProperties(
    V2Resource[WorkItemProperty, WorkItemPropertyAttach, WorkItemPropertyAttach]
):
    path = "/workspaces/{slug}/projects/{project_id}/work-item-types/{type_id}/properties/"
    model = WorkItemProperty
    operations = {
        "list": "work_item_type_properties_list",
        "retrieve": "work_item_type_properties_retrieve",
        "link": "work_item_type_properties_attach",
        "unlink": "work_item_type_properties_detach",
    }

    def list(
        self,
        slug: str,
        project: str,
        type: str,
        *,
        fields: Sequence[WorkItemTypePropertiesListField] | None = None,
        order_by: WorkItemTypePropertiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
    ) -> Page[WorkItemProperty]:
        """One page of custom properties linked to a work item type. The golden
        declares no query filters for this operation beyond `fields`/`order_by`."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
            },
            slug=slug,
            project_id=project,
            type_id=type,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        type: str,
        *,
        fields: Sequence[WorkItemTypePropertiesListField] | None = None,
        order_by: WorkItemTypePropertiesListOrderBy | None = None,
    ) -> Iterator[WorkItemProperty]:
        """Every custom property linked to a work item type, following pages
        automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by},
            slug=slug,
            project_id=project,
            type_id=type,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        type: str,
        property: str,
        *,
        fields: Sequence[WorkItemTypePropertiesRetrieveField] | None = None,
    ) -> WorkItemProperty:
        return self._retrieve(
            pk=property, params={"fields": fields}, slug=slug, project_id=project, type_id=type
        )

    def link(
        self, slug: str, project: str, type: str, property_ids: Sequence[str]
    ) -> WorkItemPropertyAttachResult:
        """Link existing property definitions to this work item type; returns the
        full set of linked property ids."""
        return self._custom_action(
            "link",
            model=WorkItemPropertyAttachResult,
            data=WorkItemPropertyAttach(properties=list(property_ids)),
            slug=slug,
            project_id=project,
            type_id=type,
        )

    def unlink(self, slug: str, project: str, type: str, property: str) -> None:
        """Unlink a property definition from this work item type. This deletes
        that property's values on every work item of the type."""
        return self._delete(pk=property, slug=slug, project_id=project, type_id=type)


class WorkspaceWorkItemTypeProperties(
    V2Resource[WorkItemProperty, WorkItemPropertyAttach, WorkItemPropertyAttach]
):
    path = "/workspaces/{slug}/work-item-types/{type_id}/properties/"
    model = WorkItemProperty
    operations = {
        "list": "workspace_work_item_type_properties_list",
        "retrieve": "workspace_work_item_type_properties_retrieve",
        "link": "workspace_work_item_type_properties_attach",
        "unlink": "workspace_work_item_type_properties_detach",
    }

    def list(
        self,
        slug: str,
        type: str,
        *,
        fields: Sequence[WorkspaceWorkItemTypePropertiesListField] | None = None,
        order_by: WorkspaceWorkItemTypePropertiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
    ) -> Page[WorkItemProperty]:
        """One page of custom properties linked to a workspace-level work item type."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
            },
            slug=slug,
            type_id=type,
        )

    def iterate(
        self,
        slug: str,
        type: str,
        *,
        fields: Sequence[WorkspaceWorkItemTypePropertiesListField] | None = None,
        order_by: WorkspaceWorkItemTypePropertiesListOrderBy | None = None,
    ) -> Iterator[WorkItemProperty]:
        """Every custom property linked to a workspace-level work item type,
        following pages automatically."""
        return self._iter(params={"fields": fields, "order_by": order_by}, slug=slug, type_id=type)

    def retrieve(
        self,
        slug: str,
        type: str,
        property: str,
        *,
        fields: Sequence[WorkspaceWorkItemTypePropertiesRetrieveField] | None = None,
    ) -> WorkItemProperty:
        return self._retrieve(pk=property, params={"fields": fields}, slug=slug, type_id=type)

    def link(
        self, slug: str, type: str, property_ids: Sequence[str]
    ) -> WorkItemPropertyAttachResult:
        """Link existing property definitions to this workspace-level work item
        type; returns the full set of linked property ids."""
        return self._custom_action(
            "link",
            model=WorkItemPropertyAttachResult,
            data=WorkItemPropertyAttach(properties=list(property_ids)),
            slug=slug,
            type_id=type,
        )

    def unlink(self, slug: str, type: str, property: str) -> None:
        """Unlink a property definition from this workspace-level work item type.
        This deletes that property's values on every work item of the type."""
        return self._delete(pk=property, slug=slug, type_id=type)
