from collections.abc import Mapping
from typing import Any

from plane.api.base_resource import BaseResource
from plane.models.customers import (
    CreateCustomerRequest,
    CustomerRequest,
    PaginatedCustomerRequestResponse,
    UpdateCustomerRequest,
)


class CustomerRequests(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        customer_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[CustomerRequest]:
        """List customer requests.

        Returns one page of requests — 1000 by default, or `per_page` when it is
        given. Use `list_paginated()` to page beyond that, or to read the cursors
        and total count.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            params: Optional query parameters, e.g. `query` to search by name,
                `per_page` to size the page
        """
        return self.list_paginated(workspace_slug, customer_id, params=params).results

    def list_paginated(
        self,
        workspace_slug: str,
        customer_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedCustomerRequestResponse:
        """List customer requests, keeping the pagination envelope.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            params: Optional query parameters, e.g. `query` to search by name,
                `per_page` to size the page, `cursor` to walk pages
        """
        response = self._get(f"{workspace_slug}/customers/{customer_id}/requests", params=params)
        return PaginatedCustomerRequestResponse.model_validate(response)

    def retrieve(self, workspace_slug: str, customer_id: str, request_id: str) -> CustomerRequest:
        """Retrieve a customer request by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            request_id: UUID of the customer request
        """
        response = self._get(f"{workspace_slug}/customers/{customer_id}/requests/{request_id}")
        return CustomerRequest.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        customer_id: str,
        data: CreateCustomerRequest | CustomerRequest,
    ) -> CustomerRequest:
        """Create a new customer request.

        `data.work_item_ids` links work items to the customer as the request is
        created. The returned request does not echo them back; read them with
        `client.customers.work_items.list()`.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            data: Customer request data. Prefer `CreateCustomerRequest`;
                `CustomerRequest` is still accepted for callers written against
                earlier versions.
        """
        response = self._post(
            f"{workspace_slug}/customers/{customer_id}/requests",
            data.model_dump(exclude_none=True),
        )
        return CustomerRequest.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        customer_id: str,
        request_id: str,
        data: UpdateCustomerRequest,
    ) -> CustomerRequest:
        """Update a customer request by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            request_id: UUID of the customer request
            data: Updated request data
        """
        response = self._patch(
            f"{workspace_slug}/customers/{customer_id}/requests/{request_id}",
            data.model_dump(exclude_none=True),
        )
        return CustomerRequest.model_validate(response)

    def delete(self, workspace_slug: str, customer_id: str, request_id: str) -> None:
        """Delete a customer request by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            request_id: UUID of the customer request
        """
        return self._delete(f"{workspace_slug}/customers/{customer_id}/requests/{request_id}")
