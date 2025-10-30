#!/usr/bin/env python3
"""
Comprehensive test script for testing all intake resources end-to-end.

This script demonstrates:
1. Creating a test project with intake view enabled
2. Testing intake work item CRUD operations
3. Testing intake work item list operations with pagination
4. Testing query parameters (expand, fields, order_by, etc.)

Usage:
    python test_intake.py

Requirements:
    - Set PLANE_BASE_URL environment variable (e.g., https://api.plane.so)
    - Set either PLANE_API_KEY or PLANE_ACCESS_TOKEN environment variable
    - Set WORKSPACE_SLUG environment variable
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from plane.client import PlaneClient  # noqa: E402
from plane.models.intake import CreateIntakeWorkItem, UpdateIntakeWorkItem  # noqa: E402
from plane.models.projects import CreateProject, UpdateProject  # noqa: E402
from plane.models.query_params import PaginatedQueryParams, RetrieveQueryParams  # noqa: E402
from plane.models.work_items import WorkItemForIntakeRequest  # noqa: E402


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

    print("Starting Comprehensive Intake SDK Test")
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

        # Create a test project
        print_step(2, "Creating a test project")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_identifier = f"IN{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Intake Test {timestamp}",
            description="Testing all intake resources",
            identifier=project_identifier,
            emoji="📥",
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")

        # Enable intake view on the project
        print_step(3, "Enabling intake view on project")
        update_data = UpdateProject(intake_view=True)
        updated_project = client.projects.update(workspace_slug, project.id, update_data)
        print_success(f"Intake view enabled on project: {updated_project.name}")

        # Test intake work item list without parameters
        print_step(4, "Testing intake work item list (basic)")
        intake_response = client.intake.list(workspace_slug, project.id)
        print_success(f"Listed intake work items: {intake_response.count} total")
        print_success(f"Returned {len(intake_response.results)} work item(s)")

        # Create multiple intake work items
        print_step(5, "Creating intake work items")
        intake_work_items = []

        for i in range(3):
            issue_data = WorkItemForIntakeRequest(
                name=f"Intake Work Item {i+1} - {timestamp}",
                description_html=f"<p>Test intake work item {i+1} for SDK testing.</p>",
                priority=["urgent", "high", "medium"][i],
            )
            create_data = CreateIntakeWorkItem(issue=issue_data)
            intake_item = client.intake.create(workspace_slug, project.id, create_data)
            intake_work_items.append(intake_item)
            print_success(
                f"Created intake work item: {intake_item.id} "
                f"(linked to issue: {intake_item.issue or 'pending'})"
            )

        # Test intake work item list with pagination parameters
        print_step(6, "Testing intake work item list with pagination parameters")
        paginated_params = PaginatedQueryParams(
            per_page=10,
            order_by="-created_at",
        )
        paginated_intakes = client.intake.list(
            workspace_slug, project.id, params=paginated_params
        )
        print_success(
            f"Listed intake work items with pagination: {paginated_intakes.count} total, "
            f"{len(paginated_intakes.results)} returned"
        )

        # Test intake work item list with expand parameter
        print_step(7, "Testing intake work item list with expand parameter")
        expand_params = PaginatedQueryParams(
            per_page=5,
            expand="issue_detail,intake,project",
            order_by="created_at",
        )
        expanded_intakes = client.intake.list(
            workspace_slug, project.id, params=expand_params
        )
        print_success(
            f"Listed intake work items with expand: {expanded_intakes.count} total, "
            f"{len(expanded_intakes.results)} returned"
        )

        # Test intake work item list with fields parameter
        print_step(8, "Testing intake work item list with fields parameter")
        fields_params = PaginatedQueryParams(
            per_page=5,
            fields="id,status,source,created_at,intake,issue",
        )
        fields_intakes = client.intake.list(
            workspace_slug, project.id, params=fields_params
        )
        print_success(
            f"Listed intake work items with fields filter: {fields_intakes.count} total, "
            f"{len(fields_intakes.results)} returned"
        )

        # Test intake work item retrieve
        print_step(9, "Testing intake work item retrieve")
        first_item = intake_work_items[0]
        # Use the work item ID (issue) to retrieve the intake work item
        work_item_id = first_item.issue
        if not work_item_id:
            print_error("Work item ID not available in intake work item response")
            sys.exit(1)
        
        retrieved_item = client.intake.retrieve(
            workspace_slug, project.id, work_item_id
        )
        print_success(f"Retrieved intake work item: {retrieved_item.id}")
        print_success(f"  Status: {retrieved_item.status}")
        print_success(f"  Source: {retrieved_item.source}")
        print_success(f"  Intake: {retrieved_item.intake}")

        # Test intake work item retrieve with expand parameter
        print_step(10, "Testing intake work item retrieve with expand parameter")
        retrieve_params = RetrieveQueryParams(expand="issue_detail,intake,project")
        expanded_item = client.intake.retrieve(
            workspace_slug, project.id, work_item_id, params=retrieve_params
        )
        print_success(f"Retrieved intake work item with expand: {expanded_item.id}")

        # Test intake work item retrieve with fields parameter
        print_step(11, "Testing intake work item retrieve with fields parameter")
        retrieve_fields_params = RetrieveQueryParams(
            fields="id,status,source,source_email,created_at,snoozed_till"
        )
        fields_item = client.intake.retrieve(
            workspace_slug,
            project.id,
            work_item_id,
            params=retrieve_fields_params,
        )
        print_success(f"Retrieved intake work item with fields filter: {fields_item.id}")

        # Test intake work item update
        print_step(12, "Testing intake work item update")
        snooze_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        update_data = UpdateIntakeWorkItem(
            source="test-script-updated",
            source_email="updated@example.com",
            snoozed_till=snooze_date,
        )
        updated_item = client.intake.update(
            workspace_slug, project.id, work_item_id, update_data
        )
        print_success(f"Updated intake work item: {updated_item.id}")
        print_success(f"  Updated source: {updated_item.source}")
        print_success(f"  Updated email: {updated_item.source_email}")
        if updated_item.snoozed_till:
            print_success(f"  Snoozed till: {updated_item.snoozed_till}")

        # Test intake work item update with issue data
        print_step(13, "Testing intake work item update with issue data")
        second_item = intake_work_items[1]
        second_work_item_id = second_item.issue
        if not second_work_item_id:
            print_error("Work item ID not available for second intake work item")
            sys.exit(1)
            
        updated_issue_data = WorkItemForIntakeRequest(
            name=f"Updated Intake Work Item - {timestamp}",
            description_html="<p>This work item has been updated via SDK.</p>",
            priority="high",
        )
        update_with_issue = UpdateIntakeWorkItem(issue=updated_issue_data)
        updated_with_issue = client.intake.update(
            workspace_slug, project.id, second_work_item_id, update_with_issue
        )
        print_success(f"Updated intake work item with issue data: {updated_with_issue.id}")

        # Test intake work item list with different ordering
        print_step(14, "Testing intake work item list with different ordering")
        order_tests = [
            ("created_at", "ascending by creation date"),
            ("-created_at", "descending by creation date"),
            ("status", "by status"),
        ]

        for order_by, description in order_tests:
            order_params = PaginatedQueryParams(order_by=order_by, per_page=5)
            ordered_intakes = client.intake.list(
                workspace_slug, project.id, params=order_params
            )
            print_success(
                f"Ordered {description}: {ordered_intakes.count} intake work items"
            )

        # Delete test intake work items
        print_step(15, "Testing intake work item delete")
        for item in intake_work_items:
            # Use the work item ID (issue) to delete the intake work item
            work_item_id_to_delete = item.issue
            if not work_item_id_to_delete:
                print_error(f"Work item ID not available for intake work item {item.id}")
                continue
            try:
                client.intake.delete(workspace_slug, project.id, work_item_id_to_delete)
                print_success(
                    f"Deleted intake work item: {item.id} (work item: {work_item_id_to_delete})"
                )
            except Exception as e:
                print_error(
                    f"Failed to delete intake work item {item.id}: {e}"
                )

        # Verify deletion by listing again
        final_list = client.intake.list(workspace_slug, project.id)
        print_success(
            f"After deletion: {final_list.count} intake work items remaining"
        )

        # Cleanup: Delete created resources (optional)
        print_step(16, "Cleanup (optional)")
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
        print_step(17, "Test Summary")
        print("✓ Intake work item list operations tested")
        print("  - Basic list, pagination, ordering, filtering")
        print("✓ Intake work item CRUD operations tested")
        print("  - Create, retrieve, update, delete")
        print("✓ Query parameters tested")
        print("  - per_page, order_by, expand, fields")
        print(f"✓ Project created: {project.name}")
        print(f"✓ Created and tested {len(intake_work_items)} intake work items")
        print("\nAll intake resource tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
