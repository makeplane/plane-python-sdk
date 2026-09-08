"""Work item relation definitions (api_v2) -- the workspace-defined direction pairs
(e.g. `blocks`/`blocked_by`) that `work_items.relations` addresses by name.
`is_default` is system-managed; writes to a seeded default 400/403 server-side."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from ...models.v2.work_item_relation_definitions import (
    CreateWorkItemRelationDefinition,
    UpdateWorkItemRelationDefinition,
    WorkItemRelationDefinition,
)
from ._generated.constants import (
    WorkItemRelationDefinitionsCreateField,
    WorkItemRelationDefinitionsListField,
    WorkItemRelationDefinitionsPartialUpdateField,
    WorkItemRelationDefinitionsRetrieveField,
)
from ._kernel.errors import MultipleMatchesFound, NoMatchFound
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


class WorkItemRelationDefinitions(
    V2Resource[
        WorkItemRelationDefinition,
        CreateWorkItemRelationDefinition,
        UpdateWorkItemRelationDefinition,
    ]
):
    path = "/workspaces/{slug}/work-item-relation-definitions/"
    model = WorkItemRelationDefinition
    operations = {
        "list": "work_item_relation_definitions_list",
        "retrieve": "work_item_relation_definitions_retrieve",
        "create": "work_item_relation_definitions_create",
        "update": "work_item_relation_definitions_partial_update",
        "delete": "work_item_relation_definitions_destroy",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[WorkItemRelationDefinitionsListField] | None = None,
        per_page: int | None = None,
        offset: int | None = None,
    ) -> Page[WorkItemRelationDefinition]:
        """One page of relation definitions. The golden offers no query filters
        or `order_by` on this operation."""
        return self._list(
            params={"fields": fields, "per_page": per_page, "offset": offset},
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[WorkItemRelationDefinitionsListField] | None = None,
    ) -> Iterator[WorkItemRelationDefinition]:
        """Every relation definition, following pages automatically."""
        return self._iter(params={"fields": fields}, slug=slug)

    def retrieve(
        self,
        slug: str,
        definition_id: str,
        *,
        fields: Sequence[WorkItemRelationDefinitionsRetrieveField] | None = None,
    ) -> WorkItemRelationDefinition:
        return self._retrieve(pk=definition_id, params={"fields": fields}, slug=slug)

    def find_by_name(self, slug: str, name: str) -> WorkItemRelationDefinition:
        """The one relation definition with this name; raises if none or several
        match. Filters client-side: no `?name=` filter exists; row count is
        always small, so a full scan is cheap."""
        matches = [row for row in self.iterate(slug) if row.name == name]
        if not matches:
            raise NoMatchFound(f"No WorkItemRelationDefinitions matched name={name!r}.")
        if len(matches) > 1:
            raise MultipleMatchesFound(
                f"Multiple rows matched name={name!r}; "
                f"use the id instead, or list to see every match."
            )
        return matches[0]

    def create(
        self,
        slug: str,
        data: CreateWorkItemRelationDefinition,
        *,
        fields: Sequence[WorkItemRelationDefinitionsCreateField] | None = None,
    ) -> WorkItemRelationDefinition:
        return self._create(data, params={"fields": fields}, slug=slug)

    def update(
        self,
        slug: str,
        definition_id: str,
        data: UpdateWorkItemRelationDefinition,
        *,
        fields: Sequence[WorkItemRelationDefinitionsPartialUpdateField] | None = None,
    ) -> WorkItemRelationDefinition:
        return self._update(data, pk=definition_id, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, definition_id: str) -> None:
        return self._delete(pk=definition_id, slug=slug)
