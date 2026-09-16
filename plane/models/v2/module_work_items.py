"""Module work-item link-management models; `modules_work_items_manage` is a single POST action,
not part of module CRUD."""

from __future__ import annotations

import builtins

from pydantic import BaseModel, ConfigDict, Field


class ModuleWorkItemManageRequest(BaseModel):
    """POST body for `.../modules/{id}/work-items/`: `add`/`remove` operate only on this module,
    each list capped at 100 ids."""

    model_config = ConfigDict(extra="ignore")

    add: builtins.list[str] = Field(default_factory=list, max_length=100)
    remove: builtins.list[str] = Field(default_factory=list, max_length=100)


class ModuleWorkItemManageResponse(BaseModel):
    """The work item ids actually added/removed -- idempotent no-ops (e.g. adding
    a work item already in the module) are omitted from both lists."""

    model_config = ConfigDict(extra="allow")

    added: builtins.list[str]
    removed: builtins.list[str]
