"""Permission models for api_v2: the caller's effective grants (no `id`), and the
catalogue of keys a custom permission scheme may grant."""

from pydantic import BaseModel, ConfigDict


class EffectivePermissions(BaseModel):
    model_config = ConfigDict(extra="allow")

    relation: str | None = None
    permission_grants: list[str] | None = None


class PermissionKey(BaseModel):
    """One grantable key. Saving it also stores `requires` (prerequisites) and `includes`
    (keys folded in with the same condition)."""

    model_config = ConfigDict(extra="allow")

    permission: str
    requires: list[str] = []
    includes: list[str] = []


class PermissionResource(BaseModel):
    model_config = ConfigDict(extra="allow")

    resource_type: str
    permissions: list[PermissionKey] = []


class PermissionCatalogue(BaseModel):
    """The permission catalogue for one namespace, grouped by resource type."""

    model_config = ConfigDict(extra="allow")

    resources: list[PermissionResource]
