#!/usr/bin/env python3
"""
Standalone test script for testing the Plane Python SDK.
Tests creating projects, work items, and labels.

Usage:
    python test_sdk.py

Requirements:
    - Set BASE_URL environment variable (e.g., https://api.plane.so)
    - Set either API_KEY or ACCESS_TOKEN environment variable
    - Set WORKSPACE_SLUG environment variable
"""

import os
import sys
from datetime import datetime

from plane.client import PlaneClient
from plane.models.labels import CreateLabel
from plane.models.projects import CreateProject
from plane.models.work_items import CreateWorkItem, UpdateWorkItem


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
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    api_key = os.getenv("API_KEY", "plane_api_cb7c33dbf12348988e5e745040bbac84")
    access_token = os.getenv("ACCESS_TOKEN")
    workspace_slug = os.getenv("WORKSPACE_SLUG", "plane")

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

    print("Starting Plane Python SDK Test")
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

        # Create a project
        print_step(2, "Creating a new project")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_identifier = f"TEST{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Test Project {timestamp}",
            description="This is a test project created by the SDK test script",
            identifier=project_identifier,
            emoji="🧪",
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")
        print(f"  Identifier: {project.identifier}")
        print(f"  Emoji: {project.emoji}")

        # Create labels
        print_step(3, "Creating labels")
        label_configs = [
            {"name": "Bug", "color": "#FF0000", "description": "Something isn't working"},
            {"name": "Feature", "color": "#00FF00", "description": "New feature request"},
            {"name": "Documentation", "color": "#0000FF", "description": "Documentation"},
        ]

        created_labels = []
        for label_config in label_configs:
            label_data = CreateLabel(**label_config)
            label = client.labels.create(workspace_slug, project.id, label_data)
            created_labels.append(label)
            print_success(f"Label created: {label.name} (ID: {label.id}, Color: {label.color})")

        # Create a work item without labels
        print_step(4, "Creating a work item")
        work_item_data = CreateWorkItem(
            name="Test Work Item - SDK Testing",
            description_html="<p>This work item was created by the SDK test script.</p>",
            priority="medium",
        )

        work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
        print_success(f"Work item created: {work_item.name} (ID: {work_item.id})")
        print(f"  Priority: {work_item.priority}")
        print(f"  Sequence ID: {work_item.sequence_id}")

        # Assign labels to the work item
        print_step(5, "Assigning labels to work item")
        label_ids = [label.id for label in created_labels]

        update_data = UpdateWorkItem(labels=label_ids)
        updated_work_item = client.work_items.update(
            workspace_slug,
            project.id,
            work_item.id,
            update_data,
        )
        print_success(f"Labels assigned to work item: {len(label_ids)} labels")

        # Verify the work item has labels (if the API returns them)
        print_step(6, "Verifying work item")
        retrieved_work_item = client.work_items.retrieve(
            workspace_slug,
            project.id,
            work_item.id,
        )
        print_success(f"Work item retrieved: {retrieved_work_item.name}")
        print(f"  ID: {retrieved_work_item.id}")
        print(f"  State: {retrieved_work_item.state}")
        print(f"  Priority: {retrieved_work_item.priority}")
        print(
            f"  Assignees: {len(retrieved_work_item.assignees) if hasattr(retrieved_work_item, 'assignees') else 'N/A'}"
        )
        print(
            f"  Labels: {len(retrieved_work_item.labels) if hasattr(retrieved_work_item, 'labels') else 'N/A'}"
        )

        # Summary
        print_step(7, "Test Summary")
        print(f"✓ Project created: {project.name}")
        print(f"✓ Labels created: {len(created_labels)}")
        print(f"✓ Work item created: {work_item.name}")
        print("✓ Labels assigned to work item")
        print("\nAll tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
