from typing import Any

from ...models.workflows import CreateWorkflow, UpdateWorkflow, Workflow
from ..base_resource import BaseResource
from .states import WorkflowStates
from .transitions import WorkflowTransitions


class Workflows(BaseResource):
    """API client for managing project workflows."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        self.states = WorkflowStates(config)
        self.transitions = WorkflowTransitions(config)

    def list(self, workspace_slug: str, project_id: str) -> list[Workflow]:
        """List all workflows for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project

        Returns:
            List of workflows
        """
        data = self._get(f"{workspace_slug}/projects/{project_id}/workflows/")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [Workflow.model_validate(item) for item in items]

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        data: CreateWorkflow,
    ) -> Workflow:
        """Create a new workflow for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Workflow data

        Returns:
            The created workflow
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/workflows/",
            data.model_dump(exclude_none=True),
        )
        return Workflow.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
        data: UpdateWorkflow,
    ) -> Workflow:
        """Update a workflow by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
            data: Updated workflow data

        Returns:
            The updated workflow
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/",
            data.model_dump(exclude_none=True),
        )
        return Workflow.model_validate(response)
