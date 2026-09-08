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

    def list(self, slug: str, project: str, work_item: str) -> WorkItemRelationList:
        """Every related work item id, grouped by relation-definition direction."""
        payload = self.transport.request(
            "GET", self._collection_url(slug=slug, project_id=project, work_item_id=work_item)
        )
        return self.model.model_validate(payload)

    def create(
        self, slug: str, project: str, work_item: str, data: WorkItemRelationCreate
    ) -> WorkItemRelationList:
        return self._create(data, slug=slug, project_id=project, work_item_id=work_item)

    def delete(self, slug: str, project: str, work_item: str, related_work_item: str) -> None:
        """Delete by the *related* work item's id, not a relation-row id -- the API
        has no separate id for a relation; the pair `(work_item, related_work_item)`
        identifies which one to remove."""
        return self._delete(
            pk=related_work_item, slug=slug, project_id=project, work_item_id=work_item
        )
