"""Permission scheme models for api_v2."""

from __future__ import annotations

import builtins
from typing import Literal

from pydantic import BaseModel, ConfigDict

Namespace = Literal["instance", "workspace", "project"]


class PermissionScheme(BaseModel):
    """A system or custom permission scheme (v1 external parity); read-only, every field but `id`
    optional."""

    model_config = ConfigDict(extra="allow")

    id: str
    description: str | None = None
    is_system: bool | None = None
    name: str | None = None
    namespace: Namespace | None = None
    permissions: builtins.list[str] | None = None
    slug: str | None = None
    sort_order: int | None = None
