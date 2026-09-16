"""Role models for api_v2. Read-only: list + retrieve only, no write surface."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

RoleNamespace = Literal["instance", "workspace", "project"]
RoleStatus = Literal["active", "inactive"]


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
