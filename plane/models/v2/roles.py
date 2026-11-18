"""Role models for api_v2: the read row plus the custom-role write bodies."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

RoleNamespace = Literal["instance", "workspace", "project"]
RoleStatus = Literal["active", "inactive"]
CustomRoleNamespace = Literal["workspace", "project"]


class Role(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    level: int | None = None
    namespace: RoleNamespace | None = None
    status: RoleStatus | None = None
    is_system: bool | None = None
    sort_order: int | None = None
    based_on_id: str | None = None
    permission_scheme_ids: list[str] | None = None
    permissions: list[str] | None = None
    updated_at: datetime | None = None


class CreateRole(BaseModel):
    """POST body -- a custom role. `based_on_slug` copies that role's schemes."""

    model_config = ConfigDict(extra="ignore")

    name: str
    namespace: CustomRoleNamespace
    description: str | None = None
    permission_scheme_ids: list[str] | None = None
    based_on_slug: str | None = None
    level: int | None = None
    sort_order: int | None = None
    status: RoleStatus | None = None


class UpdateRole(BaseModel):
    """PATCH body. Setting `status="inactive"` on a role with members needs `reassign_to`,
    the role that takes them over. A system role accepts `sort_order` only (403 otherwise)."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description: str | None = None
    permission_scheme_ids: list[str] | None = None
    level: int | None = None
    sort_order: int | None = None
    status: RoleStatus | None = None
    reassign_to: str | None = None
