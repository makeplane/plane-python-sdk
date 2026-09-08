"""Intake work items (api_v2) -- project-scoped triage queue. Model is
`IntakeWorkItem`, never `IntakeIssue`. PATCH folds v1's separate status endpoint:
set `status`/`snoozed_till`/`duplicate_to_id` in the same call as any other field."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.intakes import CreateIntakeWorkItem, IntakeWorkItem, UpdateIntakeWorkItem
from ._generated.constants import (
    IntakesCreateField,
    IntakesListField,
    IntakesListFilters,
    IntakesListOrderBy,
    IntakesPartialUpdateField,
    IntakesRetrieveField,
)
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


class Intakes(V2Resource[IntakeWorkItem, CreateIntakeWorkItem, UpdateIntakeWorkItem]):
    path = "/workspaces/{slug}/projects/{project_id}/intake-issues/"
    model = IntakeWorkItem
    operations = {
        "list": "intakes_list",
        "retrieve": "intakes_retrieve",
        "create": "intakes_create",
        "update": "intakes_partial_update",
        "delete": "intakes_destroy",
    }

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[IntakesListField] | None = None,
        order_by: IntakesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[IntakesListFilters],
    ) -> Page[IntakeWorkItem]:
        """One page of intake work items in this project. `**filters` covers the
        golden's query filters directly, e.g. `status=1`, `status__in=[-2, 0]`,
        `work_item_id=...`."""
        return self._list(
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

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[IntakesListField] | None = None,
        order_by: IntakesListOrderBy | None = None,
        **filters: Unpack[IntakesListFilters],
    ) -> Iterator[IntakeWorkItem]:
        """Every intake work item in this project, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        intake: str,
        *,
        fields: Sequence[IntakesRetrieveField] | None = None,
    ) -> IntakeWorkItem:
        return self._retrieve(pk=intake, params={"fields": fields}, slug=slug, project_id=project)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateIntakeWorkItem,
        *,
        fields: Sequence[IntakesCreateField] | None = None,
    ) -> IntakeWorkItem:
        return self._create(data, params={"fields": fields}, slug=slug, project_id=project)

    def update(
        self,
        slug: str,
        project: str,
        intake: str,
        data: UpdateIntakeWorkItem,
        *,
        fields: Sequence[IntakesPartialUpdateField] | None = None,
    ) -> IntakeWorkItem:
        return self._update(
            data, pk=intake, params={"fields": fields}, slug=slug, project_id=project
        )

    def delete(self, slug: str, project: str, intake: str) -> None:
        return self._delete(pk=intake, slug=slug, project_id=project)
