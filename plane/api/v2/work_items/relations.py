"""Work item relations (api_v2). `list`/`create` return a single dict-shaped
object, not a paginated collection -- directions are a per-workspace-defined
dynamic label set (see `work_item_relation_definitions`)."""

from __future__ import annotations

from ....models.v2.work_items import WorkItemRelationCreate, WorkItemRelationList
from .._kernel.resource import V2Resource


class WorkItemRelations(
    V2Resource[WorkItemRelationList, WorkItemRelationCreate, WorkItemRelationCreate]
):
    path = "/workspaces/{slug}/projects/{project_id}/work-items/{work_item_id}/relations/"
    model = WorkItemRelationList
    operations = {
        "list": "work_item_relations_list",
        "create": "work_item_relations_create",
        "delete": "work_item_relations_destroy",
    }

    def list(self, work_item_id: str) -> WorkItemRelationList:
        """Every related work item id, grouped by relation-definition direction."""
        payload = self.transport.request("GET", self._collection_url(work_item_id=work_item_id))
        return self.model.model_validate(payload)

    def create(self, work_item_id: str, data: WorkItemRelationCreate) -> WorkItemRelationList:
        return self._create(data, work_item_id=work_item_id)

    def delete(self, work_item_id: str, related_work_item_id: str) -> None:
        """Delete by the *related* work item's id, not a relation-row id -- the API
        has no separate id for a relation; the pair `(work_item_id,
        related_work_item_id)` identifies which one to remove."""
        return self._delete(pk=related_work_item_id, work_item_id=work_item_id)
