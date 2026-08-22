"""Saved views (api_v2). `ProjectViews`/`WorkspaceViews` are project- and
workspace-scoped filters/layouts -- different path templates, same read/write shape."""

from __future__ import annotations

from .project import ProjectViews
from .workspace import WorkspaceViews

__all__ = ["ProjectViews", "WorkspaceViews"]
