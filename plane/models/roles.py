from pydantic import BaseModel, ConfigDict

from .pagination import PaginatedResponse


class Role(BaseModel):
    """Workspace or project role definition.

    The API returns additional fields (``id``, ``permissions``, ``level``,
    ``member_count``, ...); only the three below are modeled and the rest are
    ignored. ``slug`` is the stable identifier to use in code, but it is **not**
    globally unique — e.g. ``admin``/``guest`` exist in both namespaces — so key
    roles by ``(namespace, slug)`` when indexing them.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = None
    slug: str | None = None
    namespace: str | None = None


class PaginatedRoleResponse(PaginatedResponse):
    """Paginated response for workspace/project role definitions."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Role]
