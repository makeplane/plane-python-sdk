from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..models.projects import (
    CreateProject,
    PaginatedProjectLiteResponse,
    PaginatedProjectMemberResponse,
    PaginatedProjectResponse,
    Project,
    ProjectFeature,
    ProjectMember,
    ProjectWorklogSummary,
    UpdateProject,
)
from ..models.query_params import (
    MemberListQueryParams,
    MemberQueryParams,
    PaginatedQueryParams,
    ProjectLiteListQueryParams,
)
from .base_resource import BaseResource


class Projects(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, data: CreateProject) -> Project:
        """Create a new project.

        Args:
            workspace_slug: The workspace slug identifier
            data: Project data
        """
        response = self._post(f"{workspace_slug}/projects", data.model_dump(exclude_none=True))
        return Project.model_validate(response)

    def retrieve(self, workspace_slug: str, project_id: str) -> Project:
        """Retrieve a project by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}")
        return Project.model_validate(response)

    def update(self, workspace_slug: str, project_id: str, data: UpdateProject) -> Project:
        """Update a project by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Updated project data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}", data.model_dump(exclude_none=True)
        )
        return Project.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str) -> None:
        """Delete a project by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}")

    def list(
        self, workspace_slug: str, params: PaginatedQueryParams | None = None
    ) -> PaginatedProjectResponse:
        """List projects with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(f"{workspace_slug}/projects", params=query_params)
        return PaginatedProjectResponse.model_validate(response)

    def list_lite(
        self, workspace_slug: str, params: ProjectLiteListQueryParams | None = None
    ) -> PaginatedProjectLiteResponse:
        """List projects as a paginated "lite" response.

        Calls the read-only ``/projects-lite/`` endpoint, which returns a
        field-trimmed shape (id, identifier, name, cover_image, icon_prop,
        emoji, description, cover_image_url, archived_at) suitable for pickers
        and reference lookups. Supports ordering, cursor pagination, and an
        ``include_archived`` toggle -- there are no field filters. ``per_page``
        defaults to and caps at 1000.

        .. note::
            Archived projects are now **excluded** by default. Pass
            ``ProjectLiteListQueryParams(include_archived=True)`` to restore the
            previous behavior of listing archived projects too.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional ordering + cursor pagination query parameters,
                plus the ``include_archived`` toggle
        """
        response = self._get(
            f"{workspace_slug}/projects-lite",
            params=params.to_query_params() if params else None,
        )
        return PaginatedProjectLiteResponse.model_validate(response)

    def get_worklog_summary(self, workspace_slug: str, project_id: str) -> [ProjectWorklogSummary]:
        """Get work log summary for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/total-worklogs")
        return [ProjectWorklogSummary.model_validate(item) for item in response]

    def get_members(
        self,
        workspace_slug: str,
        project_id: str,
        params: MemberQueryParams | Mapping[str, Any] | None = None,
    ) -> list[ProjectMember]:
        """Get all members of a project with optional filtering (unpaginated).

        Calls the filterable ``/projects/{id}/project-members/`` endpoint.
        Returns a list of ProjectMember objects that include role (int) and
        role_slug (str) fields in addition to basic identity fields.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters. Accepts a ``MemberQueryParams``
                instance for typed filtering (first_name, last_name, email,
                display_name, role_slug, is_active, is_bot), or a raw mapping.
        """
        if isinstance(params, MemberQueryParams):
            params = params.to_query_params()
        elif params is not None:
            # Lowercase bools so the typed filter backend accepts them
            # (requests would otherwise encode True as "True" -> HTTP 400).
            params = {k: (str(v).lower() if isinstance(v, bool) else v) for k, v in params.items()}
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/project-members", params=params
        )
        return [ProjectMember.model_validate(item) for item in response or []]

    def get_members_lite(
        self,
        workspace_slug: str,
        project_id: str,
        params: MemberListQueryParams | None = None,
    ) -> PaginatedProjectMemberResponse:
        """List project members as a paginated "lite" response.

        Unlike :meth:`get_members` (which returns a bare list), this returns a
        cursor-paginated envelope. To page through every member, follow
        ``response.next_cursor`` while ``response.next_page_results`` is True.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional filter + pagination query parameters (the
                :meth:`get_members` filters plus ``cursor`` and ``per_page``)
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/project-members-lite",
            params=params.to_query_params() if params else None,
        )
        return PaginatedProjectMemberResponse.model_validate(response)

    def get_features(self, workspace_slug: str, project_id: str) -> ProjectFeature:
        """Get features of a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/features")
        return ProjectFeature.model_validate(response)

    def update_features(
        self, workspace_slug: str, project_id: str, data: ProjectFeature
    ) -> ProjectFeature:
        """Update features of a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Updated project features
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/features", data.model_dump(exclude_none=True)
        )
        return ProjectFeature.model_validate(response)

    def archive(self, workspace_slug: str, project_id: str) -> None:
        """Archive a project.

        Move a project to archived status, hiding it from active project lists.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project

        Returns:
            None (HTTP 204 No Content)
        """
        self._post(f"{workspace_slug}/projects/{project_id}/archive", {})

    def unarchive(self, workspace_slug: str, project_id: str) -> None:
        """Unarchive a project.

        Restore an archived project to active status, making it available
        in regular workflows.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project

        Returns:
            None (HTTP 204 No Content)
        """
        self._delete(f"{workspace_slug}/projects/{project_id}/archive")
