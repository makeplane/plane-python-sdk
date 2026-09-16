"""Milestone work-item link-management models; `milestones_work_items` is a single POST action, not
part of milestone CRUD."""

from __future__ import annotations

import builtins

from pydantic import BaseModel, ConfigDict, Field


class MilestoneWorkItemManageRequest(BaseModel):
    """POST body for `.../milestones/{id}/work-items/`: `add` links the listed
    work item ids to this milestone, `remove` unlinks them. Both are optional and
    may be used together in one call."""

    model_config = ConfigDict(extra="ignore")

    add: builtins.list[str] = Field(default_factory=list)
    remove: builtins.list[str] = Field(default_factory=list)


class MilestoneWorkItemManageResponse(BaseModel):
    """The work item ids actually added/removed -- idempotent no-ops (e.g. adding
    a work item already linked) are omitted from both lists."""

    model_config = ConfigDict(extra="allow")

    added: builtins.list[str]
    removed: builtins.list[str]
