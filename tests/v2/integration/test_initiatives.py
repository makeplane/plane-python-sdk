"""Live coverage for `client.v2.workspaces.initiatives`, plus its workspace-level
`labels` catalog and its three per-initiative membership bridges.

Both ways in, and the split is the resource's own shape rather than a preference.
`InitiativeLabels` is *two* things behind one class: a workspace-level label catalog
at `path`, and a per-initiative membership bridge at `extra_paths["add"]/["remove"]`.
The catalog half has no initiative to hang off, so it is reached down the flat path
with the slug passed explicitly; the bridge half is reached off a loaded initiative
(`initiative.labels.add([...])`), which is where the initiative id comes from."""

from __future__ import annotations

import pytest

from plane.api.v2 import LoadedWorkspace, PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.initiatives import (
    CreateInitiative,
    CreateInitiativeLabel,
    UpdateInitiative,
    UpdateInitiativeLabel,
)
from plane.models.v2.work_items import CreateWorkItem

from .helpers import unique_name


class TestInitiatives:
    def test_crud(self, workspace: LoadedWorkspace) -> None:
        created = workspace.initiatives.create(CreateInitiative(name=unique_name("initiative")))
        try:
            fetched = workspace.initiatives.retrieve(created.id, expand=["lead"])
            assert fetched.id == created.id

            page = workspace.initiatives.list()
            assert any(i.id == created.id for i in page.data)

            updated = workspace.initiatives.update(created.id, UpdateInitiative(state="ACTIVE"))
            assert updated.state == "ACTIVE"

            name = created.name
            assert name is not None
            assert workspace.initiatives.find_by_name(name).id == created.id
        finally:
            workspace.initiatives.delete(created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            workspace.initiatives.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_labels_projects_and_work_items_add(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        workspace: LoadedWorkspace,
    ) -> None:
        labels = client.v2.workspaces.initiatives.labels
        initiative = workspace.initiatives.create(
            CreateInitiative(name=unique_name("initiative-manage"))
        )
        label = labels.create(
            workspace_slug, CreateInitiativeLabel(name=unique_name("initiative-label"))
        )
        work_items = client.v2.workspaces.projects.work_items
        work_item = work_items.create(
            workspace_slug, project_id, CreateWorkItem(name=unique_name("wi-initiative-link"))
        )
        try:
            # The bridge half, off the loaded initiative: no id repeated.
            labels_result = initiative.labels.add([label.id])
            assert label.id in labels_result

            projects_result = initiative.projects.add([project_id])
            assert project_id in projects_result

            work_items_result = initiative.work_items.add([work_item.id])
            assert work_item.id in work_items_result

            refreshed = workspace.initiatives.retrieve(initiative.id)
            assert refreshed.label_ids and label.id in refreshed.label_ids
            assert refreshed.project_ids and project_id in refreshed.project_ids
        finally:
            work_items.delete(workspace_slug, project_id, work_item.id)
            labels.delete(workspace_slug, label.id)
            workspace.initiatives.delete(initiative.id)

    def test_labels_crud_is_workspace_level_not_nested_under_an_initiative(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """The catalog half, and the reason this file is not purely loaded-row: the
        URL is `/workspaces/{slug}/initiatives/labels/`, with no initiative in it, so
        there is no row for these calls to hang off. A loaded initiative reaches only
        the `add`/`remove` bridge."""
        labels = client.v2.workspaces.initiatives.labels
        created = labels.create(
            workspace_slug, CreateInitiativeLabel(name=unique_name("initiative-label"))
        )
        try:
            fetched = labels.retrieve(workspace_slug, created.id)
            assert fetched.id == created.id

            updated = labels.update(
                workspace_slug, created.id, UpdateInitiativeLabel(color="#123456")
            )
            assert updated.color == "#123456"

            name = created.name
            assert name is not None
            assert labels.find_by_name(workspace_slug, name).id == created.id
        finally:
            labels.delete(workspace_slug, created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            labels.retrieve(workspace_slug, created.id)
        assert exc_info.value.status == 404
