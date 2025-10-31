from .enums import (
    AccessEnum,
    EntityTypeEnum,
    GroupEnum,
    IntakeWorkItemStatusEnum,
    ModuleStatusEnum,
    NetworkEnum,
    PageCreateAPIAccessEnum,
    PriorityEnum,
    PropertyTypeEnum,
    RelationTypeEnum,
    TimezoneEnum,
    TypeMimeEnum,
    WorkItemRelationTypeEnum,
)
from .query_params import (
    BaseQueryParams,
    PaginatedQueryParams,
    RetrieveQueryParams,
    WorkItemQueryParams,
)

__all__ = [
    # enums
    "AccessEnum",
    "EntityTypeEnum",
    "GroupEnum",
    "WorkItemRelationTypeEnum",
    "ModuleStatusEnum",
    "PageCreateAPIAccessEnum",
    "PriorityEnum",
    "PropertyTypeEnum",
    "RelationTypeEnum",
    "TimezoneEnum",
    "TypeMimeEnum",
    "NetworkEnum",
    "IntakeWorkItemStatusEnum",
    # query params
    "BaseQueryParams",
    "PaginatedQueryParams",
    "RetrieveQueryParams",
    "WorkItemQueryParams",
]


# Rebuild models with forward references after all imports
def _rebuild_forward_references() -> None:
    """Rebuild Pydantic models to resolve forward references after circular imports."""
    # Import both modules - now they won't have circular import issues
    # because we're using TYPE_CHECKING and string forward references
    from .modules import ModuleLite, ModuleWorkItem, PaginatedModuleWorkItemResponse
    from .work_items import WorkItemExpand, WorkItem

    # Rebuild models that have forward references to each other
    WorkItemExpand.model_rebuild()  # Has forward ref to ModuleLite
    ModuleWorkItem.model_rebuild()  # Has forward ref to WorkItemExpand
    PaginatedModuleWorkItemResponse.model_rebuild()  # Contains ModuleWorkItem


# Call rebuild when models package is imported
_rebuild_forward_references()
