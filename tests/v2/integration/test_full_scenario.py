"""One end-to-end scenario, readable top to bottom: project -> work item types + properties ->
states/labels -> cycle + module -> work items (readable fields, membership, comment, transition,
lookup by key) -> wiki collection + pages -> cleanup. Set PLANE_E2E_KEEP=1 to keep the rows."""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any

import pytest

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

KEEP = os.environ.get("PLANE_E2E_KEEP") == "1"


def test_full_scenario(client: PlaneClient, workspace_slug: str) -> None:
    ws = client.v2.workspace(workspace_slug)
    tag = uuid.uuid4().hex[:5].upper()
    cleanup: list[Any] = []  # (label, callable) pairs, run in reverse order

    try:
        # ---- 1. Project -------------------------------------------------------------
        project = ws.projects.create(
            CreateProject(name=f"E2E Scenario {tag}", identifier=f"E{tag}")
        )
        cleanup.append(("project", lambda: ws.projects.delete(project.id)))
        proj = ws.project(project.identifier or project.id)  # address by key from here on

        # ---- 2. Work item types + a custom property (mode-aware) ---------------------
        workspace_mode = bool(ws.features.retrieve().is_work_item_types_enabled)
        try:
            if workspace_mode:
                bug_type = ws.work_item_types.create(CreateWorkItemType(name=f"Bug {tag}"))
                cleanup.append(("type", lambda: ws.work_item_types.delete(bug_type.id)))
                proj.work_item_types.import_types([bug_type.id])
                severity = ws.work_item_properties.create(
                    CreateWorkItemProperty(display_name=f"Severity {tag}", property_type="TEXT")
                )
                cleanup.append(("property", lambda: ws.work_item_properties.delete(severity.id)))
                ws.work_item_types.properties.link(bug_type.id, [severity.id])
                cleanup.append(
                    (
                        "unlink",
                        lambda: ws.work_item_types.properties.unlink(bug_type.id, severity.id),
                    )
                )
            else:
                proj.work_item_types.enable()
                bug_type = proj.work_item_types.create(CreateWorkItemType(name=f"Bug {tag}"))
                cleanup.append(("type", lambda: proj.work_item_types.delete(bug_type.id)))
                severity = proj.work_item_properties.create(
                    CreateWorkItemProperty(display_name=f"Severity {tag}", property_type="TEXT")
                )
                cleanup.append(("property", lambda: proj.work_item_properties.delete(severity.id)))
                proj.work_item_types.properties.link(bug_type.id, [severity.id])
                cleanup.append(
                    (
                        "unlink",
                        lambda: proj.work_item_types.properties.unlink(bug_type.id, severity.id),
                    )
                )
        except PlaneAPIError as exc:
            if exc.status == 402:
                pytest.skip("work item types are not enabled on this workspace's plan")
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
        assert item.custom_fields and item.custom_fields[severity_key]["value"] == "high"  # type: ignore[index]
        assert item.identifier  # e.g. "E1A2B-1"

        subtask = proj.work_items.create(
            CreateWorkItem(name="Add regression test", parent=item.identifier)
        )
        cleanup.append(("sub-task", lambda: proj.work_items.delete(subtask.id)))
        assert subtask.parent_id == item.id

        proj.cycles.work_items.add(sprint.id, [item.id, subtask.id])
        proj.modules.work_items.add(auth.id, [item.id])
        in_sprint = {row.id for row in proj.work_items.list(cycle_id=sprint.id).data}
        assert in_sprint >= {item.id, subtask.id}

        proj.work_items.comments.create(
            item.id, CreateWorkItemComment(comment_html="<p>Repro attached.</p>")
        )
        assert len(proj.work_items.comments.list(item.id).data) == 1

        moved = proj.work_items.update(item.id, UpdateWorkItem(state="In Progress"))
        assert moved.state_id == in_progress.id

        by_key = ws.work_items.retrieve_by_identifier(item.identifier)  # no project needed
        assert by_key.id == item.id
        assert by_key.cycle_id == sprint.id
        assert auth.id in (by_key.module_ids or [])

        # ---- 6. Wiki: a collection, a page inside it, and a project page --------------
        handbook = ws.wiki.collections.create(CreateCollection(name=f"Handbook {tag}"))
        cleanup.append(("collection", lambda: ws.wiki.collections.delete(handbook.id)))
        runbook = ws.wiki.pages.create(CreatePage(name="Login runbook", collection_id=handbook.id))
        cleanup.append(("wiki page", lambda: _archive_then_delete(ws.wiki.pages, runbook.id)))
        assert runbook.collection_id == handbook.id
        in_handbook = ws.wiki.pages.list(collection_id=handbook.id).data
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


def _archive_then_delete(pages: Any, page_id: str) -> None:
    """v2 refuses to delete a live page: archive first (PATCH `archived_at`), then delete."""
    pages.update(page_id, UpdatePage(archived_at=datetime.now(timezone.utc)))
    pages.delete(page_id)
