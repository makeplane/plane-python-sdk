"""Artifact models for api_v2 -- `create`/`retrieve`/`publish`/`update` each return a differently-
shaped envelope; every read field but `id` is optional."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

DataMode = Literal["snapshot", "live"]


class Artifact(BaseModel):
    """Returned by `create`."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    current_version: int | None = None
    is_published: bool | None = None
    anchor: str | None = None
    data_mode: DataMode | None = None


class ArtifactDetail(BaseModel):
    """Returned by `retrieve`."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = None
    data_mode: DataMode | None = None
    current_version: int | None = None
    html: str | None = None


class ArtifactPublish(BaseModel):
    """Returned by `publish`. No `id` -- this row has none."""

    model_config = ConfigDict(extra="allow")

    anchor: str | None = None
    is_active: bool | None = None


class ArtifactUpdated(BaseModel):
    """Returned by `update`."""

    model_config = ConfigDict(extra="allow")

    id: str
    current_version: int | None = None
    data_mode: DataMode | None = None


class CreateArtifact(BaseModel):
    """POST body for `create`. `html` and `name` are required by the API."""

    model_config = ConfigDict(extra="ignore")

    name: str
    html: str
    description: str | None = None
    prompt: str | None = None
    project: str | None = None
    data_mode: DataMode | None = None


class UpdateArtifactUpdate(BaseModel):
    """PATCH body for `update` -- appends a new HTML version; golden marks `html` optional but the
    live view 400s without it."""

    model_config = ConfigDict(extra="ignore")

    html: str | None = None
    prompt: str | None = None
