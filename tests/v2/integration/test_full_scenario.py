"""One end-to-end scenario, readable top to bottom: project -> work item types + properties ->
states/labels -> cycle + module -> work items (readable fields, membership, comment, transition,
lookup by key) -> wiki collection + pages -> cleanup. Set PLANE_E2E_KEEP=1 to keep the rows."""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any

from plane.api.v2 import PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.collections import CreateCollection
from plane.models.v2.cycles import CreateCycle
from plane.models.v2.labels import CreateLabel
from plane.models.v2.modules import CreateModule
from plane.models.v2.pages import CreatePage, UpdatePage
from plane.models.v2.projects import CreateProject
from plane.models.v2.work_item_properties import CreateWorkItemProperty
from plane.models.v2.work_item_types import CreateWorkItemType
from plane.models.v2.work_items import CreateWorkItem, CreateWorkItemComment, UpdateWorkItem

from ._guard import skip_absent_capability

KEEP = os.environ.get("PLANE_E2E_KEEP") == "1"


def test_full_scenario(client: PlaneClient, workspace_slug: str) -> None:
    ws = client.v2.workspaces.retrieve(workspace_slug)
    tag = uuid.uuid4().hex[:5].upper()
    cleanup: list[Any] = []  # (label, callable) pairs, run in reverse order

    try:
        # ---- 1. Project -------------------------------------------------------------
        project = ws.projects.create(
            CreateProject(name=f"E2E Scenario {tag}", identifier=f"E{tag}")
        )
        cleanup.append(("project", lambda: ws.projects.delete(project.id)))
        # `Projects.create` already answers a loaded row, and `_row_id` is
        # `identifier`, so `project` *is* the by-key handle -- there is nothing left to
        # re-bind. That is the whole point of the loaded-row design, and this line
        # used to be the locator call that made it look otherwise.
        proj = project

        # ---- 2. Work item types + a custom property (mode-aware) ---------------------
        workspace_mode = bool(ws.features.retrieve().is_work_item_types_enabled)
        # `bug_type`/`severity` are loaded rows of *different* classes depending on the
        # branch (workspace- vs project-scoped work item types), so they are annotated
        # `Any`: the two are the same shape to this scenario, but not the same type.
        bug_type: Any
        severity: Any
        try:
            if workspace_mode:
                bug_type = ws.work_item_types.create(CreateWorkItemType(name=f"Bug {tag}"))
                cleanup.append(("type", lambda: ws.work_item_types.delete(bug_type.id)))
                proj.work_item_types.import_types([bug_type.id])
                severity = ws.work_item_properties.create(
                    CreateWorkItemProperty(display_name=f"Severity {tag}", property_type="TEXT")
                )
                cleanup.append(("property", lambda: ws.work_item_properties.delete(severity.id)))
                bug_type.properties.link([severity.id])
                cleanup.append(("unlink", lambda: bug_type.properties.unlink(severity.id)))
            else:
                proj.work_item_types.enable()
                bug_type = proj.work_item_types.create(CreateWorkItemType(name=f"Bug {tag}"))
                cleanup.append(("type", lambda: proj.work_item_types.delete(bug_type.id)))
                severity = proj.work_item_properties.create(
                    CreateWorkItemProperty(display_name=f"Severity {tag}", property_type="TEXT")
                )
                cleanup.append(("property", lambda: proj.work_item_properties.delete(severity.id)))
                bug_type.properties.link([severity.id])
                cleanup.append(("unlink", lambda: bug_type.properties.unlink(severity.id)))
        except PlaneAPIError as exc:
            if exc.status == 402:
                skip_absent_capability("work item types are not enabled on this workspace's plan")
            raise
        severity_key = severity.name
        assert severity_key
        assert any(row.id == bug_type.id for row in proj.work_item_types.list().data)

        # ---- 3. States and labels ---------------------------------------------------
        todo = proj.states.find_by_name("Todo")  # seeded with every new project
        in_progress = proj.states.find_by_name("In Progress")
        bug_label = proj.labels.create(CreateLabel(name="bug", color="#d73a4a"))
        cleanup.append(("label", lambda: proj.labels.delete(bug_label.id)))

        # ---- 4. Cycle and module ----------------------------------------------------
        sprint = proj.cycles.create(CreateCycle(name="Sprint 1"))
        cleanup.append(("cycle", lambda: proj.cycles.delete(sprint.id)))
        auth = proj.modules.create(CreateModule(name="Auth"))
        cleanup.append(("module", lambda: proj.modules.delete(auth.id)))

        # ---- 5. Work items: readable fields in, ids out ------------------------------
        item = proj.work_items.create(
            CreateWorkItem(
                name="Fix login bug",
                state="Todo",
                labels=["bug"],
                type=bug_type.name,
                custom_fields={severity_key: "high"},
            )
        )
        cleanup.append(("work item", lambda: proj.work_items.delete(item.id)))
        assert item.state_id == todo.id
        assert bug_label.id in (item.label_ids or [])
        assert item.type_id == bug_type.id
        assert item.custom_fields is not None
        severity_value = item.custom_fields[severity_key]
        assert isinstance(severity_value, dict)
        assert severity_value["value"] == "high"
        assert item.identifier  # e.g. "E1A2B-1"

        subtask = proj.work_items.create(
            CreateWorkItem(name="Add regression test", parent=item.identifier)
        )
        cleanup.append(("sub-task", lambda: proj.work_items.delete(subtask.id)))
        assert subtask.parent_id == item.id

        sprint.work_items.add([item.id, subtask.id])
        auth.work_items.add([item.id])
        in_sprint = {row.id for row in proj.work_items.list(cycle_id=sprint.id).data}
        assert in_sprint >= {item.id, subtask.id}

        item.comments.create(CreateWorkItemComment(comment_html="<p>Repro attached.</p>"))
        assert len(item.comments.list().data) == 1

        moved = proj.work_items.update(item.id, UpdateWorkItem(state="In Progress"))
        assert moved.state_id == in_progress.id

        by_key = ws.work_items.retrieve_by_identifier(item.identifier)  # no project needed
        assert by_key.id == item.id
        assert by_key.cycle_id == sprint.id
        assert auth.id in (by_key.module_ids or [])

        # ---- 6. Wiki: a collection, a page inside it, and a project page --------------
        # `wiki` is a grouping node, not a resource: it holds no `V2Resource` base and
        # consumes no path id, so a loaded workspace deliberately does not reach it and
        # its children each take `slug` themselves. Flat path, by design.
        collections = client.v2.workspaces.wiki.collections
        wiki_pages = client.v2.workspaces.wiki.pages
        handbook = collections.create(workspace_slug, CreateCollection(name=f"Handbook {tag}"))
        cleanup.append(("collection", lambda: collections.delete(workspace_slug, handbook.id)))
        runbook = wiki_pages.create(
            workspace_slug, CreatePage(name="Login runbook", collection_id=handbook.id)
        )
        cleanup.append(
            ("wiki page", lambda: _archive_then_delete(wiki_pages, workspace_slug, runbook.id))
        )
        assert runbook.collection_id == handbook.id
        in_handbook = wiki_pages.list(workspace_slug, collection_id=handbook.id).data
        assert any(row.id == runbook.id for row in in_handbook)

        notes = proj.pages.create(CreatePage(name="Sprint 1 notes"))
        cleanup.append(("project page", lambda: _archive_then_delete(proj.pages, notes.id)))
        assert any(row.id == notes.id for row in proj.pages.list().data)
    finally:
        # ---- 7. Cleanup, newest first; every failure is reported, none is swallowed -------
        failures: list[str] = []
        if not KEEP:
            for label, undo in reversed(cleanup):
                try:
                    undo()
                except Exception as exc:
                    failures.append(f"{label}: {exc}")
    assert not failures, "cleanup left rows behind:\n" + "\n".join(failures)


def _archive_then_delete(pages: Any, *ids: str) -> None:
    """v2 refuses to delete a live page: archive first (PATCH `archived_at`), then
    delete. `*ids` are whatever leading path ids the caller's handle still needs --
    none for a bound `proj.pages`, the workspace slug for the flat `wiki.pages`."""
    pages.update(*ids, UpdatePage(archived_at=datetime.now(timezone.utc)))
    pages.delete(*ids)
