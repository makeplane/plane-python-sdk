#!/usr/bin/env python3
"""
Comprehensive test script for testing all epics resources end-to-end.

This script demonstrates:
1. Creating a test project
2. Testing epic list operations with pagination
3. Testing epic retrieve operations
4. Testing query parameters (expand, fields, order_by, etc.)

Usage:
    python test_epics.py

Requirements:
    - Set PLANE_BASE_URL environment variable (e.g., https://api.plane.so)
    - Set either PLANE_API_KEY or PLANE_ACCESS_TOKEN environment variable
    - Set WORKSPACE_SLUG environment variable
    - Have a project with at least one epic (or the test will demonstrate listing empty results)
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from plane.client import PlaneClient  # noqa: E402
from plane.models.projects import CreateProject  # noqa: E402
from plane.models.query_params import PaginatedQueryParams, RetrieveQueryParams  # noqa: E402


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
    base_url = os.getenv("PLANE_BASE_URL")
    api_key = os.getenv("PLANE_API_KEY")
    access_token = os.getenv("PLANE_ACCESS_TOKEN")
    workspace_slug = os.getenv("WORKSPACE_SLUG")

    # Validate required environment variables
    if not base_url:
        print_error("PLANE_BASE_URL environment variable is required")
        sys.exit(1)

    if not api_key and not access_token:
        print_error("Either PLANE_API_KEY or PLANE_ACCESS_TOKEN environment variable is required")
        sys.exit(1)

    if not workspace_slug:
        print_error("WORKSPACE_SLUG environment variable is required")
        sys.exit(1)

    print("Starting Comprehensive Epics SDK Test")
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

        # Create or use an existing project
        print_step(2, "Setting up test project")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_identifier = f"EP{timestamp[-6:]}"

        # Create a test project
        project_data = CreateProject(
            name=f"Epics Test {timestamp}",
            description="Testing all epics resources",
            identifier=project_identifier,
            emoji="📊",
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")

        # Test epic list without parameters
        print_step(3, "Testing epic list (basic)")
        epics_response = client.epics.list(workspace_slug, project.id)
        print_success(f"Listed epics: {epics_response.count} total")
        print_success(f"Returned {len(epics_response.results)} epic(s)")
        
        if epics_response.results:
            for epic in epics_response.results:
                print_success(f"  - Epic: {epic.name} (ID: {epic.id})")
        else:
            print_success("No epics found in project (this is expected for a new project)")

        # Test epic list with pagination parameters
        print_step(4, "Testing epic list with pagination parameters")
        paginated_params = PaginatedQueryParams(
            per_page=10,
            order_by="-created_at",  # Sort by creation date descending
        )
        paginated_epics = client.epics.list(
            workspace_slug, project.id, params=paginated_params
        )
        print_success(
            f"Listed epics with pagination: {paginated_epics.count} total, "
            f"{len(paginated_epics.results)} returned"
        )

        # Test epic list with expand parameter
        print_step(5, "Testing epic list with expand parameter")
        expand_params = PaginatedQueryParams(
            per_page=5,
            expand="project,state",  # Expand related objects
            order_by="name",
        )
        expanded_epics = client.epics.list(
            workspace_slug, project.id, params=expand_params
        )
        print_success(
            f"Listed epics with expand: {expanded_epics.count} total, "
            f"{len(expanded_epics.results)} returned"
        )

        # Test epic list with fields parameter
        print_step(6, "Testing epic list with fields parameter")
        fields_params = PaginatedQueryParams(
            per_page=5,
            fields="id,name,priority,start_date,target_date",  # Only specific fields
        )
        fields_epics = client.epics.list(
            workspace_slug, project.id, params=fields_params
        )
        print_success(
            f"Listed epics with fields filter: {fields_epics.count} total, "
            f"{len(fields_epics.results)} returned"
        )

        # Test epic retrieve if any epics exist
        if epics_response.results:
            print_step(7, "Testing epic retrieve")
            first_epic = epics_response.results[0]
            retrieved_epic = client.epics.retrieve(
                workspace_slug, project.id, first_epic.id
            )
            print_success(f"Retrieved epic: {retrieved_epic.name} (ID: {retrieved_epic.id})")
            print_success(f"  Priority: {retrieved_epic.priority}")
            print_success(f"  Project: {retrieved_epic.project}")
            print_success(f"  Workspace: {retrieved_epic.workspace}")

            # Test epic retrieve with expand parameter
            print_step(8, "Testing epic retrieve with expand parameter")
            retrieve_params = RetrieveQueryParams(expand="project,state,assignees")
            expanded_epic = client.epics.retrieve(
                workspace_slug, project.id, first_epic.id, params=retrieve_params
            )
            print_success(f"Retrieved epic with expand: {expanded_epic.name}")

            # Test epic retrieve with fields parameter
            print_step(9, "Testing epic retrieve with fields parameter")
            retrieve_fields_params = RetrieveQueryParams(
                fields="id,name,description,priority,completed_at"
            )
            fields_epic = client.epics.retrieve(
                workspace_slug,
                project.id,
                first_epic.id,
                params=retrieve_fields_params,
            )
            print_success(f"Retrieved epic with fields filter: {fields_epic.name}")
        else:
            print_step(7, "Skipping retrieve tests (no epics available)")
            print_success(
                "No epics found to retrieve. "
                "Epics can be created through the Plane UI or API."
            )
            print_success(
                "To test retrieve functionality, create at least one epic in the project."
            )

        # Test epic list with ordering
        print_step(10, "Testing epic list with different ordering")
        order_tests = [
            ("name", "ascending by name"),
            ("-name", "descending by name"),
            ("created_at", "ascending by creation date"),
            ("-created_at", "descending by creation date"),
            ("priority", "by priority"),
            ("sort_order", "by sort order"),
        ]

        for order_by, description in order_tests:
            order_params = PaginatedQueryParams(order_by=order_by, per_page=5)
            ordered_epics = client.epics.list(
                workspace_slug, project.id, params=order_params
            )
            print_success(
                f"Ordered {description}: "
                f"{ordered_epics.count} epics ({description})"
            )

        # Cleanup: Delete created resources (optional)
        print_step(11, "Cleanup (optional)")
        choice = input("Delete test project? (y/N): ").strip().lower()
        if choice == "y":
            try:
                client.projects.delete(workspace_slug, project.id)
                print_success("Deleted test project")
            except Exception as e:
                print_error(f"Failed to delete project: {e}")
        else:
            print_success("Keeping test project for inspection")
            print_success(
                f"You can view the project at: {base_url}/w/{workspace_slug}/p/{project.id}"
            )

        # Summary
        print_step(12, "Test Summary")
        print("✓ Epic list operations tested")
        print("  - Basic list, pagination, ordering, filtering")
        print("✓ Epic retrieve operations tested")
        if epics_response.results:
            print("  - Basic retrieve, with expand, with fields")
        else:
            print("  - (Skipped: no epics available in project)")
        print("✓ Query parameters tested")
        print("  - per_page, order_by, expand, fields")
        print(f"✓ Project created: {project.name}")
        print("\nAll epics resource tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

