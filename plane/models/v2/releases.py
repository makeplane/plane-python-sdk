"""Release models for api_v2 (workspace-scoped); label/tag catalogs are distinct from the per-
release association (`ReleaseChildManageRequest`)."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

ReleaseStatus = Literal["unreleased", "released", "cancelled"]


class Release(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    status: ReleaseStatus | None = None
    description_html: str | None = None
    description_id: str | None = None
    release_date: date | None = None
    target_date: date | None = None
    is_latest: bool | None = None
    is_prerelease: bool | None = None
    lead_id: str | None = None
    tag_id: str | None = None
    label_ids: list[str] | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateRelease(BaseModel):
    """POST body. `name` is the only field the API requires."""

    model_config = ConfigDict(extra="ignore")

    name: str
    status: ReleaseStatus | None = None
    description_html: str | None = None
    description_json: object | None = None
    release_date: date | None = None
    target_date: date | None = None
    is_latest: bool | None = None
    is_prerelease: bool | None = None
    lead_id: str | None = None
    tag_id: str | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateRelease(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    status: ReleaseStatus | None = None
    description_html: str | None = None
    description_json: object | None = None
    release_date: date | None = None
    target_date: date | None = None
    is_latest: bool | None = None
    is_prerelease: bool | None = None
    lead_id: str | None = None
    tag_id: str | None = None
    external_id: str | None = None
    external_source: str | None = None


# -- Labels (workspace-level catalog) --------------------------------------------


class ReleaseLabel(BaseModel):
    """A workspace-level release-label catalog entry -- not the per-release
    association (see `ReleaseLabels.add`/`.remove`)."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    color: str | None = None
    sort_order: int | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateReleaseLabel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    color: str | None = None
    sort_order: int | None = None


class UpdateReleaseLabel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    color: str | None = None
    sort_order: int | None = None


# -- Tags (workspace-level catalog) ----------------------------------------------


class ReleaseTag(BaseModel):
    """A workspace-level release-tag catalog entry; detail routes accept either its UUID or a
    `version:<value>`-prefixed lookup."""

    model_config = ConfigDict(extra="allow")

    id: str
    version: str | None = None
    description: str | None = None
    git_tag: str | None = None
    commit_hash: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateReleaseTag(BaseModel):
    model_config = ConfigDict(extra="ignore")

    version: str
    description: str | None = None
    git_tag: str | None = None
    commit_hash: str | None = None


class UpdateReleaseTag(BaseModel):
    model_config = ConfigDict(extra="ignore")

    version: str | None = None
    description: str | None = None
    git_tag: str | None = None
    commit_hash: str | None = None


# -- Comments (nested under a release) -------------------------------------------


class ReleaseComment(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    release_id: str | None = None
    comment_id: str | None = None
    comment_html: str | None = None
    is_resolved: bool | None = None
    is_hidden: bool | None = None
    parent_id: str | None = None
    edited_at: datetime | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateReleaseComment(BaseModel):
    model_config = ConfigDict(extra="ignore")

    comment_html: str
    is_resolved: bool | None = None
    parent_id: str | None = None


class UpdateReleaseComment(BaseModel):
    model_config = ConfigDict(extra="ignore")

    comment_html: str | None = None
    is_resolved: bool | None = None
    parent_id: str | None = None


# -- Links (nested under a release) ----------------------------------------------


class ReleaseLink(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    release_id: str | None = None
    title: str | None = None
    url: str | None = None
    metadata: dict[str, object] | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateReleaseLink(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str
    url: str
    metadata: dict[str, object] | None = None


class UpdateReleaseLink(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str | None = None
    url: str | None = None
    metadata: dict[str, object] | None = None


# -- Changelog (singleton nested under a release) --------------------------------


class ReleaseChangelog(BaseModel):
    """One changelog per release, created implicitly with the release. There is
    no create/delete -- only `Releases.changelog.retrieve`/`.update`."""

    model_config = ConfigDict(extra="allow")

    id: str
    release_id: str | None = None
    changelog_id: str | None = None
    description_html: str | None = None
    description_json: object | None = None


class UpdateReleaseChangelog(BaseModel):
    model_config = ConfigDict(extra="ignore")

    description_html: str | None = None
    description_json: object | None = None


# -- Child membership bridges (labels / work items) --------------------------------


class ReleaseChildManageRequest(BaseModel):
    """Body of the `.work_items`/`ReleaseLabels` bridges (`add`/`remove`): ids
    to attach and/or detach on the release in one call."""

    model_config = ConfigDict(extra="ignore")

    add: list[str] | None = None
    remove: list[str] | None = None


class ReleaseChildManageResult(BaseModel):
    """The ids actually added/removed by a `.work_items`/`ReleaseLabels`
    bridge call."""

    model_config = ConfigDict(extra="allow")

    added: list[str] = []
    removed: list[str] = []
