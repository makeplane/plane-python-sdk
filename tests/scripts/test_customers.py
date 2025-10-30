#!/usr/bin/env python3
"""
Comprehensive test script for testing Customers SDK functionality end-to-end.

This script demonstrates:
1. Creating customer properties (email, phone, industry, company_size, etc.)
2. Creating multiple customers with details
3. Creating customer requests
4. Updating customers and properties
5. Listing and retrieving customers and requests

Usage:
    python test_customers.py

Requirements:
    - Set BASE_URL environment variable (e.g., https://api.plane.so)
    - Set either API_KEY or ACCESS_TOKEN environment variable
    - Set WORKSPACE_SLUG environment variable
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from plane.client import PlaneClient  # noqa: E402
from plane.models.customers import (  # noqa: E402
    CreateCustomer,
    CreateCustomerProperty,
    CustomerRequest,
    UpdateCustomer,
    UpdateCustomerProperty,
    UpdateCustomerRequest,
)
from plane.models.enums import PropertyType  # noqa: E402
from plane.models.work_item_property_configurations import (  # noqa: E402
    DateAttributeSettings,
    TextAttributeSettings,
)


def print_step(step_num: int, message: str) -> None:
    """Print a formatted step message."""
    print(f"\n{'=' * 70}")
    print(f"Step {step_num}: {message}")
    print("=" * 70)


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"✗ {message}", file=sys.stderr)


def main() -> None:
    """Main test function."""
    # Get configuration from environment
    base_url = os.getenv("BASE_URL")
    api_key = os.getenv("API_KEY")
    access_token = os.getenv("ACCESS_TOKEN")
    workspace_slug = os.getenv("WORKSPACE_SLUG")

    # Validate required environment variables
    if not base_url:
        print_error("BASE_URL environment variable is required")
        sys.exit(1)

    if not api_key and not access_token:
        print_error("Either API_KEY or ACCESS_TOKEN environment variable is required")
        sys.exit(1)

    if not workspace_slug:
        print_error("WORKSPACE_SLUG environment variable is required")
        sys.exit(1)

    print("Starting Comprehensive Customer SDK Test")
    print(f"Base URL: {base_url}")
    print(f"Workspace: {workspace_slug}")
    print(f"Authentication: {'API Key' if api_key else 'Access Token'}")

    try:
        # Initialize the client
        print_step(1, "Initializing Plane Client")
        client = PlaneClient(
            base_url=base_url,
            api_key=api_key,
            access_token=access_token,
        )
        print_success("Client initialized successfully")

        # Create customer properties first
        print_step(2, "Creating customer properties")
        properties = {}

        # Property definitions
        # Let's delete the below properties if existing and create new ones.
        # Need to first get the properties and then delete them.
        properties_response = client.customers.properties.list(workspace_slug)
        print(f"Properties: {properties_response}")
        for prop in properties_response.results:
            client.customers.properties.delete(workspace_slug, prop.id)

        property_definitions = [
            {
                "name": "email",
                "display_name": "Email Address",
                "description": "Customer email address",
                "type": PropertyType.TEXT.value,
                "settings": TextAttributeSettings(display_format="single-line"),
                "is_required": False,
            },
            {
                "name": "phone",
                "display_name": "Phone Number",
                "description": "Customer phone number",
                "type": PropertyType.TEXT.value,
                "settings": TextAttributeSettings(display_format="single-line"),
                "is_required": False,
            },
            {
                "name": "industry",
                "display_name": "Industry",
                "description": "Industry sector",
                "type": PropertyType.TEXT.value,
                "settings": TextAttributeSettings(display_format="single-line"),
                "is_required": False,
            },
            {
                "name": "company_size",
                "display_name": "Company Size",
                "description": "Number of employees",
                "type": PropertyType.DECIMAL.value,
                "settings": None,
                "is_required": False,
            },
            {
                "name": "contract_value",
                "display_name": "Contract Value",
                "description": "Annual contract value in USD",
                "type": PropertyType.DECIMAL.value,
                "settings": None,
                "is_required": False,
            },
            {
                "name": "is_enterprise",
                "display_name": "Enterprise Customer",
                "description": "Is this an enterprise customer?",
                "type": PropertyType.BOOLEAN.value,
                "settings": None,
                "is_required": False,
            },
            {
                "name": "onboarding_date",
                "display_name": "Onboarding Date",
                "description": "Date when customer was onboarded",
                "type": PropertyType.DATETIME.value,
                "settings": DateAttributeSettings(display_format="MMM dd, yyyy"),
                "is_required": False,
            },
        ]

        for prop_def in property_definitions:
            prop_data = CreateCustomerProperty(
                name=prop_def["name"],
                display_name=prop_def["display_name"],
                description=prop_def["description"],
                property_type=prop_def["type"],
                is_required=prop_def["is_required"],
                is_active=True,
                settings=prop_def["settings"],
            )
            prop = client.customers.properties.create(workspace_slug, prop_data)
            properties[prop_def["name"]] = prop
            print_success(f"Created property '{prop.display_name}' (ID: {prop.id})")

        # Create multiple customers
        print_step(3, "Creating customers")
        customers = []

        # Let's delete the below customers if existing and create new ones.
        # Need to first get the customers and then delete them.
        customers_response = client.customers.list(workspace_slug)
        print(f"Customers: {customers_response}")
        for cust in customers_response.results:
            client.customers.delete(workspace_slug, cust.id)

        customer_definitions = [
            {
                "name": "Acme Corporation",
                "description": "Leading technology company",
                "email": "contact@acme.com",
                "website_url": "https://acme.com",
                "domain": "acme.com",
                "stage": "enterprise",
                "contract_status": "active",
                "employees": 500,
            },
            {
                "name": "TechStart Inc",
                "description": "Fast-growing startup",
                "email": "hello@techstart.io",
                "website_url": "https://techstart.io",
                "domain": "techstart.io",
                "stage": "growth",
                "contract_status": "trial",
                "employees": 50,
            },
            {
                "name": "Global Finance LLC",
                "description": "Financial services company",
                "email": "info@globalfinance.com",
                "website_url": "https://globalfinance.com",
                "domain": "globalfinance.com",
                "stage": "enterprise",
                "contract_status": "active",
                "employees": 2000,
            },
        ]

        for cust_def in customer_definitions:
            customer_data = CreateCustomer(**cust_def)
            customer = client.customers.create(workspace_slug, customer_data)
            customers.append(customer)
            print_success(f"Created customer: {customer.name} (ID: {customer.id})")

        # Create customer requests
        print_step(4, "Creating customer requests")
        customer_1 = customers[0]
        customer_2 = customers[1]
        requests = []  # List of (request, customer_id) tuples

        # Create requests for first customer
        request_data_1 = CustomerRequest(
            name="Need feature X implementation",
            description="We need feature X to be implemented as per our requirements",
            description_html="<p>Feature X implementation needed urgently</p>",
            link="https://acme.com/requirements/feature-x",
        )
        request_1 = client.customers.requests.create(workspace_slug, customer_1.id, request_data_1)
        requests.append((request_1, customer_1.id))
        print_success(f"Created request: {request_1.name} for {customer_1.name}")

        # Create request for second customer
        request_data_2 = CustomerRequest(
            name="Bug fix in module Y",
            description="Critical bug in module Y affecting our workflow",
            description_html="<p>Please fix the bug ASAP</p>",
        )
        request_2 = client.customers.requests.create(workspace_slug, customer_2.id, request_data_2)
        requests.append((request_2, customer_2.id))
        print_success(f"Created request: {request_2.name} for {customer_2.name}")

        # Create request for third customer
        request_data_3 = CustomerRequest(
            name="Custom integration needed",
            description="We need a custom integration with our internal systems",
            description_html="<p>Integration with legacy systems required</p>",
        )
        request_3 = client.customers.requests.create(
            workspace_slug, customers[2].id, request_data_3
        )
        requests.append((request_3, customers[2].id))
        print_success(f"Created request: {request_3.name} for {customers[2].name}")

        # Update a customer
        print_step(5, "Updating customer information")
        update_data = UpdateCustomer(
            name="Acme Corporation (Updated)",
            description="Leading technology company - Premium Plan",
            stage="enterprise_premium",
            contract_status="active_renewal",
        )
        updated_customer = client.customers.update(workspace_slug, customer_1.id, update_data)
        print_success(f"Updated customer: {updated_customer.name}")
        print(f"  New stage: {updated_customer.stage}")
        print(f"  New contract status: {updated_customer.contract_status}")

        # Update a property
        print_step(6, "Updating customer property")
        update_prop_data = UpdateCustomerProperty(
            display_name="Email Address (Updated)",
            description="Customer email address - updated description",
            is_required=True,
        )
        updated_property = client.customers.properties.update(
            workspace_slug, properties["email"].id, update_prop_data
        )
        print_success(f"Updated property: {updated_property.display_name}")

        # List customers with search
        print_step(7, "Listing and filtering customers")
        all_customers_response = client.customers.list(workspace_slug)
        all_customers = all_customers_response.results
        print_success(f"Total customers in workspace: {len(all_customers)}")
        print(f"  Total count: {all_customers_response.total_count}")
        print(f"  Total results: {all_customers_response.total_results}")

        # Search for specific customer
        search_customers_response = client.customers.list(workspace_slug, params={"search": "Acme"})
        search_customers = search_customers_response.results
        print_success(f"Customers matching 'Acme': {len(search_customers)}")

        # Retrieve specific customer
        retrieved_customer = client.customers.retrieve(workspace_slug, customer_1.id)
        print_success(f"Retrieved customer: {retrieved_customer.name}")

        # List customer requests
        customer_1_requests = client.customers.requests.list(workspace_slug, customer_1.id)
        print_success(f"Customer 1 has {len(customer_1_requests)} requests")

        # Retrieve a specific request
        if customer_1_requests:
            retrieved_request = client.customers.requests.retrieve(
                workspace_slug, customer_1.id, customer_1_requests[0].id
            )
            print_success(f"Retrieved request: {retrieved_request.name}")

        # Update a request
        print_step(8, "Updating customer request")
        if requests:
            request_to_update, customer_id = requests[0]
            update_request_data = UpdateCustomerRequest(
                name="Need feature X implementation (URGENT)",
                description_html="<p>Feature X implementation needed urgently - Priority HIGH</p>",
            )
            updated_request = client.customers.requests.update(
                workspace_slug,
                customer_id,
                request_to_update.id,
                update_request_data,
            )
            print_success(f"Updated request: {updated_request.name}")

        # Cleanup: Delete created resources (optional)
        print_step(9, "Cleanup (optional)")
        choice = input("Delete test resources? (y/N): ").strip().lower()
        if choice == "y":
            # Delete customer requests
            for req, customer_id in requests:
                try:
                    client.customers.requests.delete(workspace_slug, customer_id, req.id)
                    print_success(f"Deleted customer request: {req.name}")
                except Exception as e:
                    print_error(f"Failed to delete customer request {req.name}: {e}")

            # Delete customers
            for customer in customers:
                try:
                    client.customers.delete(workspace_slug, customer.id)
                    print_success(f"Deleted customer: {customer.name}")
                except Exception as e:
                    print_error(f"Failed to delete customer {customer.name}: {e}")

            # Delete customer properties
            for prop in properties.values():
                try:
                    client.customers.properties.delete(workspace_slug, prop.id)
                    print_success(f"Deleted customer property: {prop.display_name}")
                except Exception as e:
                    print_error(f"Failed to delete customer property {prop.display_name}: {e}")
        else:
            print_success("Keeping test resources for inspection")

        # Summary
        print_step(10, "Test Summary")
        print(f"✓ Customer properties created: {len(properties)}")
        for prop in properties.values():
            print(f"    - {prop.display_name} ({prop.property_type})")
        print(f"✓ Customers created: {len(customers)}")
        for customer in customers:
            print(f"    - {customer.name} ({customer.stage})")
        print(f"✓ Customer requests created: {len(requests)}")
        for req, _ in requests:
            print(f"    - {req.name}")
        print("✓ Customer and properties updated successfully")
        print(f"✓ Total customers in workspace: {all_customers_response.total_count}")
        print("\nAll customer tests completed successfully!")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
