"""Effective-permissions model for api_v2 -- the calling principal's own grants for
a workspace or a project. Read-only, no `id` (this row has none)."""

from pydantic import BaseModel, ConfigDict


class EffectivePermissions(BaseModel):
    model_config = ConfigDict(extra="allow")

    relation: str | None = None
    permission_grants: list[str] | None = None
