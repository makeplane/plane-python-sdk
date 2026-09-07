"""Work item dependencies (api_v2). Same non-paginated, dict-shaped `list`/`create`
as `WorkItemRelations`, but the six directions are fixed by the API, not a
per-workspace label set."""

from __future__ import annotations

from ....models.v2.work_items import WorkItemDependencyCreate, WorkItemDependencyList
from .._kernel.resource import V2Resource


class WorkItemDependencies(
    V2Resource[WorkItemDependencyList, WorkItemDependencyCreate, WorkItemDependencyCreate]
):
    path = "/workspaces/{slug}/projects/{project_id}/work-items/{work_item_id}/dependencies/"
    model = WorkItemDependencyList
    operations = {
        "list": "work_item_dependencies_list",
        "create": "work_item_dependencies_create",
        "delete": "work_item_dependencies_destroy",
    }

    def list(self, work_item_id: str) -> WorkItemDependencyList:
        """Every related work item id, grouped by dependency direction."""
        payload = self.transport.request(
            "GET", self._collection_url(work_item_id=work_item_id)
        )
        return self.model.model_validate(payload)

    def create(
        self, work_item_id: str, data: WorkItemDependencyCreate
    ) -> WorkItemDependencyList:
        return self._create(data, work_item_id=work_item_id)

    def delete(self, work_item_id: str, related_work_item_id: str) -> None:
        """Delete by the *related* work item's id -- see `WorkItemRelations.delete`."""
        return self._delete(pk=related_work_item_id, work_item_id=work_item_id)
