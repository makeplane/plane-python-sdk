from collections.abc import Mapping
from typing import Any

from ..models.modules import (
    CreateModule,
    Module,
    PaginatedArchivedModuleResponse,
    PaginatedModuleResponse,
    PaginatedModuleWorkItemResponse,
    UpdateModule,
)
from .base_resource import BaseResource


class Modules(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, project_id: str, data: CreateModule) -> Module:
        """Create a new module.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Module data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/modules",
            data.model_dump(exclude_none=True),
        )
        return Module.model_validate(response)

    def retrieve(self, workspace_slug: str, project_id: str, module_id: str) -> Module:
        """Retrieve a module by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            module_id: UUID of the module
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/modules/{module_id}")
        return Module.model_validate(response)

    def update(
        self, workspace_slug: str, project_id: str, module_id: str, data: UpdateModule
    ) -> Module:
        """Update a module by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            module_id: UUID of the module
            data: Updated module data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/modules/{module_id}",
            data.model_dump(exclude_none=True),
        )
        return Module.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, module_id: str) -> None:
        """Delete a module by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            module_id: UUID of the module
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/modules/{module_id}")

    def list(
        self, workspace_slug: str, project_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedModuleResponse:
        """List modules with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/modules", params=params)
        return PaginatedModuleResponse.model_validate(response)

    def list_archived(
        self, workspace_slug: str, project_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedArchivedModuleResponse:
        """List archived modules with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/archived-modules", params=params
        )
        return PaginatedArchivedModuleResponse.model_validate(response)

    def add_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        module_id: str,
        issue_ids: [str],
    ) -> None:
        """Add work items to a module.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            module_id: UUID of the module
            issue_ids: List of issue IDs to add to the module
        """
        return self._post(
            f"{workspace_slug}/projects/{project_id}/modules/{module_id}/module-issues",
            {"issues": issue_ids},
        )

    def remove_work_item(
        self, workspace_slug: str, project_id: str, module_id: str, work_item_id: str
    ) -> None:
        """Remove a work item from a module.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            module_id: UUID of the module
            work_item_id: UUID of the work item
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/modules/{module_id}/module-issues/{work_item_id}"
        )

    def list_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        module_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedModuleWorkItemResponse:
        """List work items in a module.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            module_id: UUID of the module
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/modules/{module_id}/module-issues",
            params=params,
        )
        return PaginatedModuleWorkItemResponse.model_validate(response)

    def archive(self, workspace_slug: str, project_id: str, module_id: str) -> None:
        """Archive a module.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            module_id: UUID of the module

        Returns:
            None (HTTP 204 No Content)
        """
        self._post(f"{workspace_slug}/projects/{project_id}/modules/{module_id}/archive", {})

    def unarchive(self, workspace_slug: str, project_id: str, module_id: str) -> None:
        """Unarchive a module.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            module_id: UUID of the module

        Returns:
            None (HTTP 204 No Content)
        """
        self._delete(
            f"{workspace_slug}/projects/{project_id}/archived-modules/{module_id}/unarchive"
        )
