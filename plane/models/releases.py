"""Models for releases."""

from typing import Any

from pydantic import BaseModel, ConfigDict

from .pagination import PaginatedResponse


class Release(BaseModel):
    """Release response model.

    `description` is returned as a nested object ({description_html, description_json,
    ...}), not a plain string. Write it with `description_html` / `description_json`
    on create/update.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    description: Any | None = None
    status: str | None = None
    target_date: str | None = None
    release_date: str | None = None
    lead: str | None = None
    tag: str | None = None
    is_latest: bool | None = None
    is_prerelease: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    workspace: str | None = None

    # Deprecated: never populated by the API. Kept so existing callers do not break.
    start_date: str | None = None
    logo_props: Any | None = None


class CreateRelease(BaseModel):
    """Request model for creating a release.

    Set the body with `description_html` / `description_json`. `status` is one of
    "unreleased" (default), "released", "cancelled".
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description_html: str | None = None
    description_json: Any | None = None
    status: str | None = None
    target_date: str | None = None
    release_date: str | None = None
    lead: str | None = None
    tag: str | None = None
    is_prerelease: bool | None = None
    external_source: str | None = None
    external_id: str | None = None

    # Deprecated: ignored by the API. Kept for backward compatibility.
    description: str | None = None
    start_date: str | None = None
    logo_props: Any | None = None


class UpdateRelease(BaseModel):
    """Request model for updating a release."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description_html: str | None = None
    description_json: Any | None = None
    status: str | None = None
    target_date: str | None = None
    release_date: str | None = None
    lead: str | None = None
    tag: str | None = None
    is_prerelease: bool | None = None
    external_source: str | None = None
    external_id: str | None = None

    # Deprecated: ignored by the API. Kept for backward compatibility.
    description: str | None = None
    start_date: str | None = None
    logo_props: Any | None = None


class ReleaseTag(BaseModel):
    """Release tag response model.

    A tag is a version marker (version + optional git metadata), not a label.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    version: str | None = None
    description: str | None = None
    commit_hash: str | None = None
    git_tag: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    workspace: str | None = None

    # Deprecated: a tag has no name/color/sort_order. Kept so old readers do not break.
    name: str | None = None
    color: str | None = None
    sort_order: float | None = None


class CreateReleaseTag(BaseModel):
    """Request model for creating a release tag.

    `version` is required by the API and must be unique in the workspace. `name`
    and `color` are ignored (a tag is not a label) and kept only for backward
    compatibility.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    version: str | None = None
    description: str | None = None
    commit_hash: str | None = None
    git_tag: str | None = None

    # Deprecated: ignored by the API. Kept for backward compatibility.
    name: str | None = None
    color: str | None = None


class UpdateReleaseTag(BaseModel):
    """Request model for updating a release tag."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    version: str | None = None
    description: str | None = None
    commit_hash: str | None = None
    git_tag: str | None = None


class ReleaseLabel(BaseModel):
    """Release label response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    color: str | None = None
    sort_order: float | None = None
    workspace: str | None = None


class CreateReleaseLabel(BaseModel):
    """Request model for creating a release label."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    color: str | None = None
    sort_order: int | None = None


class UpdateReleaseLabel(BaseModel):
    """Request model for updating a release label."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    color: str | None = None
    sort_order: int | None = None


class AddReleaseItemLabel(BaseModel):
    """Request model for adding labels to a release."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    label_ids: list[str]


class ReleaseWorkItem(BaseModel):
    """A work item linked to a release, as returned by the list endpoint."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str | None = None
    project_id: str | None = None


class AddReleaseWorkItems(BaseModel):
    """Request model for linking work items to a release."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    work_item_ids: list[str]


class ReleaseComment(BaseModel):
    """Release comment response model.

    `comment` is a nested object ({description_html, ...}). Write it with
    `comment_html`.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    comment: Any | None = None
    is_hidden: bool | None = None
    is_resolved: bool | None = None
    parent: str | None = None
    edited_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    workspace: str | None = None
    release: str | None = None


class CreateReleaseComment(BaseModel):
    """Request model for creating a release comment."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    comment_html: str
    parent: str | None = None


class UpdateReleaseComment(BaseModel):
    """Request model for updating a release comment."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    comment_html: str | None = None
    is_resolved: bool | None = None


class ReleaseLink(BaseModel):
    """Release link response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    title: str | None = None
    url: str | None = None
    metadata: Any | None = None
    created_at: str | None = None
    updated_at: str | None = None
    workspace: str | None = None
    release: str | None = None


class CreateReleaseLink(BaseModel):
    """Request model for creating a release link."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    url: str
    title: str | None = None
    metadata: Any | None = None


class UpdateReleaseLink(BaseModel):
    """Request model for updating a release link."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    title: str | None = None
    url: str | None = None
    metadata: Any | None = None


class PaginatedReleaseResponse(PaginatedResponse):
    """Paginated response for the releases list endpoint."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Release]


class PaginatedReleaseTagResponse(PaginatedResponse):
    """Paginated response for the release tags list endpoint."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[ReleaseTag]


class PaginatedReleaseLabelResponse(PaginatedResponse):
    """Paginated response for the release labels list endpoint."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[ReleaseLabel]


class PaginatedReleaseWorkItemResponse(PaginatedResponse):
    """Paginated response for the release work-items list endpoint."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[ReleaseWorkItem]


class PaginatedReleaseCommentResponse(PaginatedResponse):
    """Paginated response for the release comments list endpoint."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[ReleaseComment]


class PaginatedReleaseLinkResponse(PaginatedResponse):
    """Paginated response for the release links list endpoint."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[ReleaseLink]
