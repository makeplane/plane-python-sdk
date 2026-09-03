"""Customer work-item membership bridge (api_v2)."""

from __future__ import annotations

import builtins
from collections.abc import Sequence

from ....models.v2.customers import CustomerWorkItemManageRequest, CustomerWorkItemManageResponse
from .._kernel.resource import V2Resource


class CustomerWorkItems(
    V2Resource[
        CustomerWorkItemManageResponse, CustomerWorkItemManageRequest, CustomerWorkItemManageRequest
    ]
):
    """Membership bridge between a customer and work items: `add` links work
    items to the customer, `remove` unlinks them. Both POST to
    `.../customers/{customer_id}/work-items/` and return the ids actually
    changed."""

    path = "/workspaces/{slug}/customers/{customer_id}/work-items/"
    model = CustomerWorkItemManageResponse
    operations = {
        "bridge": "customers_work_items",
    }

    def add(self, customer_id: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Link 1..100 work items to this customer; returns the ids actually
        added (already-linked ones are omitted)."""
        return self._bridge(key="add", ids=work_item_ids, customer_id=customer_id)

    def remove(self, customer_id: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Unlink 1..100 work items from this customer; returns the ids
        actually removed."""
        return self._bridge(key="remove", ids=work_item_ids, customer_id=customer_id)
