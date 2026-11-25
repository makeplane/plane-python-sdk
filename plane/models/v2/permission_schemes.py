"""Permission scheme models for api_v2."""

from __future__ import annotations

import builtins
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

Namespace = Literal["instance", "workspace", "project"]
SchemeNamespace = Literal["workspace", "project"]


class PermissionScheme(BaseModel):
    """A system or custom permission scheme; every field but `id` optional."""

    model_config = ConfigDict(extra="allow")

    id: str
    description: str | None = None
    is_system: bool | None = None
    name: str | None = None
    namespace: Namespace | None = None
    permissions: builtins.list[str] | None = None
    slug: str | None = None
    sort_order: int | None = None
    updated_at: datetime | None = None


class CreatePermissionScheme(BaseModel):
    """POST body. `permissions` are keys from `permissions.resources()`; the server adds
    each key's prerequisites and folded keys on save."""

    model_config = ConfigDict(extra="ignore")

    name: str
    namespace: SchemeNamespace
    permissions: builtins.list[str] | None = None
    description: str | None = None
    sort_order: int | None = None


class UpdatePermissionScheme(BaseModel):
    """PATCH body -- custom schemes only; `namespace` is fixed at create."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    permissions: builtins.list[str] | None = None
    description: str | None = None
    sort_order: int | None = None


class PermissionSchemeImpact(BaseModel):
    """Who a change to the scheme reaches: the workspace's roles composing it, the people
    holding those roles, and the projects those people can reach."""

    model_config = ConfigDict(extra="allow")

    roles: int
    users: int
    projects: int
