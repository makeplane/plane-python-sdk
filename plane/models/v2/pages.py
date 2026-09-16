"""Page models for api_v2; `Page` backs both project-scoped and workspace-scoped (wiki) pages via
`ProjectPages`/`WikiPages`."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

PageAccess = Literal[0, 1]  # 0 = Public, 1 = Private


class Page(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    access: PageAccess | None = None
    archived_at: datetime | None = None
    collection_id: str | None = None
    color: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_global: bool | None = None
    is_locked: bool | None = None
    logo_props: dict[str, object] | None = None
    name: str | None = None
    owned_by_id: str | None = None
    parent_id: str | None = None
    sort_order: float | None = None
    view_props: dict[str, object] | None = None


class CreatePage(BaseModel):
    """POST body. `name` is the only field the API requires."""

    model_config = ConfigDict(extra="ignore")

    name: str
    access: PageAccess | None = None
    archived_at: datetime | None = None
    collection_id: str | None = None
    """Adds the page to a collection on create; omitting `collection_id` auto-assigns the public
    default collection, so private pages need an explicit private one."""
    color: str | None = None
    description_html: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_locked: bool | None = None
    logo_props: dict[str, object] | None = None
    parent_id: str | None = None
    sort_order: float | None = None
    view_props: dict[str, object] | None = None


class UpdatePage(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    access: PageAccess | None = None
    archived_at: datetime | None = None
    collection_id: str | None = None
    color: str | None = None
    description_html: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_locked: bool | None = None
    logo_props: dict[str, object] | None = None
    parent_id: str | None = None
    sort_order: float | None = None
    view_props: dict[str, object] | None = None
