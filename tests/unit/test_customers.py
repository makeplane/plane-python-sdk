"""Unit tests for Customers API resource (smoke tests with real HTTP requests)."""

import pytest

from plane.client import PlaneClient
from plane.models.customers import CreateCustomer, UpdateCustomer


class TestCustomersAPI:
    """Test Customers API resource."""

    def test_list_customers(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing customers."""
        response = client.customers.list(workspace_slug)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_customers_with_params(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing customers with query parameters."""
        response = client.customers.list(workspace_slug, params={"limit": 10})
        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) <= 10


class TestCustomersAPICRUD:
    """Test Customers API CRUD operations."""

    @pytest.fixture
    def customer_data(self) -> CreateCustomer:
        """Create test customer data."""
        import time
        return CreateCustomer(
            name=f"Test Customer {int(time.time())}",
            email=f"test{int(time.time())}@example.com",
        )

    @pytest.fixture
    def customer(self, client: PlaneClient, workspace_slug: str, customer_data: CreateCustomer):
        """Create a test customer and yield it, then delete it."""
        customer = client.customers.create(workspace_slug, customer_data)
        yield customer
        try:
            client.customers.delete(workspace_slug, customer.id)
        except Exception:
            pass

    def test_create_customer(
        self, client: PlaneClient, workspace_slug: str, customer_data: CreateCustomer
    ) -> None:
        """Test creating a customer."""
        customer = client.customers.create(workspace_slug, customer_data)
        assert customer is not None
        assert customer.id is not None
        assert customer.name == customer_data.name
        
        # Cleanup
        try:
            client.customers.delete(workspace_slug, customer.id)
        except Exception:
            pass

    def test_retrieve_customer(self, client: PlaneClient, workspace_slug: str, customer) -> None:
        """Test retrieving a customer."""
        retrieved = client.customers.retrieve(workspace_slug, customer.id)
        assert retrieved is not None
        assert retrieved.id == customer.id
        assert retrieved.name == customer.name

    def test_update_customer(self, client: PlaneClient, workspace_slug: str, customer) -> None:
        """Test updating a customer."""
        update_data = UpdateCustomer(name="Updated Customer Name")
        updated = client.customers.update(workspace_slug, customer.id, update_data)
        assert updated is not None
        assert updated.id == customer.id
        assert updated.name == "Updated Customer Name"

