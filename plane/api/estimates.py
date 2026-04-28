from __future__ import annotations

from typing import Any

from ..models.estimates import (
    CreateEstimate,
    CreateEstimatePoint,
    Estimate,
    EstimatePoint,
    UpdateEstimate,
    UpdateEstimatePoint,
)
from .base_resource import BaseResource


class Estimates(BaseResource):
    """Resource for managing project estimates and estimate points."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    # ── Estimate CRUD ────────────────────────────────────────────

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        data: CreateEstimate,
    ) -> Estimate:
        """Create a new estimate for a project.

        After creation the estimate is automatically linked to the project
        so that it appears as an active (non-archived) estimate in the UI.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
            data: Estimate creation data.
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/estimates",
            data.model_dump(exclude_none=True),
        )
        estimate = Estimate.model_validate(response)

        # Link the estimate to the project so it shows as active
        if estimate.id:
            self._patch(
                f"{workspace_slug}/projects/{project_id}",
                {"estimate": estimate.id},
            )

        return estimate

    def retrieve(
        self,
        workspace_slug: str,
        project_id: str,
    ) -> Estimate:
        """Retrieve the estimate configured for a project.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/estimates",
        )
        return Estimate.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        data: UpdateEstimate,
    ) -> Estimate:
        """Update the estimate for a project.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
            data: Fields to update.
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/estimates",
            data.model_dump(exclude_none=True),
        )
        return Estimate.model_validate(response)

    def delete(
        self,
        workspace_slug: str,
        project_id: str,
    ) -> None:
        """Delete the estimate for a project.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/estimates",
        )

    # ── Estimate Points ──────────────────────────────────────────

    def list_points(
        self,
        workspace_slug: str,
        project_id: str,
        estimate_id: str,
    ) -> list[EstimatePoint]:
        """List all estimate points for a project estimate.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
            estimate_id: UUID of the estimate.
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}"
            f"/estimates/{estimate_id}/estimate-points",
        )
        return [EstimatePoint.model_validate(item) for item in response]

    def create_points(
        self,
        workspace_slug: str,
        project_id: str,
        estimate_id: str,
        data: list[CreateEstimatePoint],
    ) -> list[EstimatePoint]:
        """Create estimate points for a project estimate.

        The API accepts a JSON array directly as the request body.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
            estimate_id: UUID of the estimate.
            data: List of estimate point creation data.
        """
        payload = [item.model_dump(exclude_none=True) for item in data]
        response = self._post(
            f"{workspace_slug}/projects/{project_id}"
            f"/estimates/{estimate_id}/estimate-points",
            payload,
        )
        return [EstimatePoint.model_validate(item) for item in response]

    def update_point(
        self,
        workspace_slug: str,
        project_id: str,
        estimate_id: str,
        estimate_point_id: str,
        data: UpdateEstimatePoint,
    ) -> EstimatePoint:
        """Update a single estimate point.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
            estimate_id: UUID of the estimate.
            estimate_point_id: UUID of the estimate point.
            data: Fields to update.
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}"
            f"/estimates/{estimate_id}/estimate-points/{estimate_point_id}",
            data.model_dump(exclude_none=True),
        )
        return EstimatePoint.model_validate(response)

    def delete_point(
        self,
        workspace_slug: str,
        project_id: str,
        estimate_id: str,
        estimate_point_id: str,
    ) -> None:
        """Delete a single estimate point.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
            estimate_id: UUID of the estimate.
            estimate_point_id: UUID of the estimate point.
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}"
            f"/estimates/{estimate_id}/estimate-points/{estimate_point_id}",
        )
