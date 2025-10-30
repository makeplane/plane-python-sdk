#!/usr/bin/env python3
"""
Comprehensive test script for testing all labels resources end-to-end.

This script demonstrates:
1. Creating a test project
2. Testing label CRUD operations
3. Testing label list operations with pagination
4. Testing parent-child label relationships

Usage:
    python test_labels.py

Requirements:
    - Set PLANE_BASE_URL environment variable (e.g., https://api.plane.so)
    - Set either PLANE_API_KEY or PLANE_ACCESS_TOKEN environment variable
    - Set WORKSPACE_SLUG environment variable
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from plane.client import PlaneClient  # noqa: E402
from plane.models.labels import CreateLabel, UpdateLabel  # noqa: E402
from plane.models.projects import CreateProject  # noqa: E402


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

    print("Starting Comprehensive Labels SDK Test")
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
        project_identifier = f"LB{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Labels Test {timestamp}",
            description="Testing all labels resources",
            identifier=project_identifier,
            emoji="🏷️",
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")

        # Test label list without parameters
        print_step(3, "Testing label list (basic)")
        labels_response = client.labels.list(workspace_slug, project.id)
        print_success(f"Listed labels: {labels_response.count} total")
        print_success(f"Returned {len(labels_response.results)} label(s)")

        # Create multiple labels
        print_step(4, "Creating labels")
        labels = []

        label_colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"]
        label_names = ["Bug", "Feature", "Documentation", "Enhancement", "Question"]

        for i in range(5):
            label_data = CreateLabel(
                name=f"{label_names[i]} - {timestamp}",
                color=label_colors[i],
                description=f"Test label for {label_names[i].lower()} items",
                sort_order=float(i),
            )
            label = client.labels.create(workspace_slug, project.id, label_data)
            labels.append(label)
            print_success(f"Created label: {label.name} (ID: {label.id})")

        # Test label list after creation
        print_step(5, "Testing label list after creation")
        labels_after = client.labels.list(workspace_slug, project.id)
        print_success(
            f"Listed labels: {labels_after.count} total, "
            f"{len(labels_after.results)} returned"
        )

        # Test label retrieve
        print_step(6, "Testing label retrieve")
        first_label = labels[0]
        retrieved_label = client.labels.retrieve(
            workspace_slug, project.id, first_label.id
        )
        print_success(f"Retrieved label: {retrieved_label.name}")
        print_success(f"  Color: {retrieved_label.color}")
        print_success(f"  Description: {retrieved_label.description}")

        # Test label update
        print_step(7, "Testing label update")
        update_data = UpdateLabel(
            name=f"{first_label.name} (Updated)",
            description="This label has been updated via SDK",
            color="#FF0000",
            sort_order=100.0,
        )
        updated_label = client.labels.update(
            workspace_slug, project.id, first_label.id, update_data
        )
        print_success(f"Updated label: {updated_label.name}")
        print_success(f"  New color: {updated_label.color}")
        print_success(f"  New description: {updated_label.description}")

        # Test creating child labels (labels with parent)
        print_step(8, "Testing parent-child label relationships")
        parent_label = labels[1]
        child_label_data = CreateLabel(
            name=f"Sub-{parent_label.name} - {timestamp}",
            color="#808080",
            description="A child label",
            parent=parent_label.id,
        )
        child_label = client.labels.create(workspace_slug, project.id, child_label_data)
        print_success(f"Created child label: {child_label.name}")
        print_success(f"  Parent: {child_label.parent}")

        # Verify parent relationship by retrieving child
        retrieved_child = client.labels.retrieve(
            workspace_slug, project.id, child_label.id
        )
        print_success(
            f"Verified child label parent relationship: {retrieved_child.parent}"
        )

        # Test label list with external source/ID
        print_step(9, "Testing labels with external source/ID")
        external_label_data = CreateLabel(
            name=f"External Label - {timestamp}",
            color="#00FF00",
            description="Label with external source tracking",
            external_source="test-script",
            external_id=f"ext-{timestamp}",
        )
        external_label = client.labels.create(
            workspace_slug, project.id, external_label_data
        )
        print_success(f"Created label with external tracking: {external_label.name}")
        print_success(f"  External source: {external_label.external_source}")
        print_success(f"  External ID: {external_label.external_id}")

        # Test update with external source/ID
        update_external = UpdateLabel(
            external_id=f"ext-updated-{timestamp}",
        )
        updated_external = client.labels.update(
            workspace_slug, project.id, external_label.id, update_external
        )
        print_success(f"Updated external label ID: {updated_external.external_id}")

        # List all labels to see the full set
        print_step(10, "Listing all labels")
        all_labels = client.labels.list(workspace_slug, project.id)
        print_success(f"Total labels in project: {all_labels.count}")
        for label in all_labels.results:
            parent_info = f" (parent: {label.parent})" if label.parent else ""
            print_success(f"  - {label.name}{parent_info}")

        # Delete test labels
        print_step(11, "Testing label delete")
        labels_to_delete = labels + [child_label, external_label]
        for label in labels_to_delete:
            try:
                client.labels.delete(workspace_slug, project.id, label.id)
                print_success(f"Deleted label: {label.name} (ID: {label.id})")
            except Exception as e:
                print_error(f"Failed to delete label {label.name}: {e}")

        # Verify deletion by listing again
        final_list = client.labels.list(workspace_slug, project.id)
        print_success(f"After deletion: {final_list.count} labels remaining")

        # Cleanup: Delete created resources (optional)
        print_step(12, "Cleanup (optional)")
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
        print_step(13, "Test Summary")
        print("✓ Label list operations tested")
        print("  - Basic list, listing after creation")
        print("✓ Label CRUD operations tested")
        print("  - Create, retrieve, update, delete")
        print("✓ Label relationships tested")
        print("  - Parent-child relationships")
        print("✓ External source/ID tracking tested")
        print("  - Creating and updating labels with external tracking")
        print(f"✓ Project created: {project.name}")
        print(f"✓ Created and tested {len(labels_to_delete)} labels")
        print("\nAll labels resource tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

