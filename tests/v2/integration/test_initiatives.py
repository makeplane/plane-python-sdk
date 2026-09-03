"""Live coverage for `client.v2.workspace(slug).initiatives`, plus its
workspace-level `labels` sub-resource and child-management actions; skips
(never fails) when required env vars are absent."""

from __future__ import annotations

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.initiatives import Initiatives
from plane.client import PlaneClient
from plane.models.v2.initiatives import (
    CreateInitiative,
    CreateInitiativeLabel,
    UpdateInitiative,
    UpdateInitiativeLabel,
)
from plane.models.v2.work_items import CreateWorkItem

from .helpers import unique_name


@pytest.fixture(scope="module")
def initiatives(client: PlaneClient, workspace_slug: str) -> Initiatives:
    return client.v2.workspace(workspace_slug).initiatives


class TestInitiatives:
    def test_crud(self, initiatives: Initiatives) -> None:
        created = initiatives.create(CreateInitiative(name=unique_name("initiative")))
        try:
            fetched = initiatives.retrieve(created.id, expand=["lead"])
            assert fetched.id == created.id

            page = initiatives.list()
            assert any(i.id == created.id for i in page.data)

            updated = initiatives.update(created.id, UpdateInitiative(state="ACTIVE"))
            assert updated.state == "ACTIVE"

            assert initiatives.find_by_name(created.name).id == created.id
        finally:
            initiatives.delete(created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            initiatives.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_labels_projects_and_work_items_add(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        initiatives: Initiatives,
    ) -> None:
        initiative = initiatives.create(CreateInitiative(name=unique_name("initiative-manage")))
        label = initiatives.labels.create(
            CreateInitiativeLabel(name=unique_name("initiative-label"))
        )
        work_items = client.v2.workspace(workspace_slug).project(project_id).work_items
        work_item = work_items.create(CreateWorkItem(name=unique_name("wi-initiative-link")))
        try:
            labels_result = initiatives.labels.add(initiative.id, [label.id])
            assert label.id in labels_result

            projects_result = initiatives.projects.add(initiative.id, [project_id])
            assert project_id in projects_result

            work_items_result = initiatives.work_items.add(initiative.id, [work_item.id])
            assert work_item.id in work_items_result

            refreshed = initiatives.retrieve(initiative.id)
            assert refreshed.label_ids and label.id in refreshed.label_ids
            assert refreshed.project_ids and project_id in refreshed.project_ids
        finally:
            work_items.delete(work_item.id)
            initiatives.labels.delete(label.id)
            initiatives.delete(initiative.id)

    def test_labels_crud_is_workspace_level_not_nested_under_an_initiative(
        self, initiatives: Initiatives
    ) -> None:
        created = initiatives.labels.create(
            CreateInitiativeLabel(name=unique_name("initiative-label"))
        )
        try:
            fetched = initiatives.labels.retrieve(created.id)
            assert fetched.id == created.id

            updated = initiatives.labels.update(created.id, UpdateInitiativeLabel(color="#123456"))
            assert updated.color == "#123456"

            assert initiatives.labels.find_by_name(created.name).id == created.id
        finally:
            initiatives.labels.delete(created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            initiatives.labels.retrieve(created.id)
        assert exc_info.value.status == 404
