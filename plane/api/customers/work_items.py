from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from plane.api.base_resource import BaseResource
from plane.models.customers import (
    CustomerWorkItem,
    LinkCustomerWorkItems,
    LinkCustomerWorkItemsResponse,
)


class CustomerWorkItems(BaseResource):
    """API resource for the work items linked to a customer.

    Links may hang off the customer alone, or off one of its requests when a
    `customer_request_id` is supplied.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        customer_id: str,
        customer_request_id: str | None = None,
        search: str | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> list[CustomerWorkItem]:
        """List the work items linked to a customer.

        This endpoint is not paginated and returns every linked work item.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            customer_request_id: Only return work items linked via this request
            search: Match on work item name, sequence ID or project identifier
            params: Additional query parameters
        """
        query: dict[str, Any] = dict(params or {})
        if customer_request_id:
            query["customer_request_id"] = customer_request_id
        if search:
            query["search"] = search

        response = self._get(
            f"{workspace_slug}/customers/{customer_id}/issues", params=query or None
        )
        return [CustomerWorkItem.model_validate(item) for item in response]

    def link(
        self,
        workspace_slug: str,
        customer_id: str,
        data: LinkCustomerWorkItems,
        customer_request_id: str | None = None,
    ) -> LinkCustomerWorkItemsResponse:
        """Link one or more work items to a customer.

        The API rejects the whole call if any work item in `data.work_item_ids`
        does not exist. Re-linking an already linked work item is a no-op.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            data: The work items to link
            customer_request_id: Attach the links to this request of the customer
        """
        query = {"customer_request_id": customer_request_id} if customer_request_id else None
        response = self._post(
            f"{workspace_slug}/customers/{customer_id}/issues",
            data.model_dump(exclude_none=True, by_alias=True),
            params=query,
        )
        return LinkCustomerWorkItemsResponse.model_validate(response)

    def unlink(
        self,
        workspace_slug: str,
        customer_id: str,
        work_item_id: str,
        customer_request_id: str | None = None,
    ) -> None:
        """Unlink a work item from a customer.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            work_item_id: UUID of the work item to unlink
            customer_request_id: Only drop the link made via this request;
                without it every link between the customer and the work item goes

        Raises:
            HttpError: 404 if no such link exists
        """
        query = {"customer_request_id": customer_request_id} if customer_request_id else None
        return self._delete(
            f"{workspace_slug}/customers/{customer_id}/issues/{work_item_id}", params=query
        )
