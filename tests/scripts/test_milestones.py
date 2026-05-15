#!/usr/bin/env python3
"""
Comprehensive test script for testing SDK Milestone functionality end-to-end.

This script demonstrates:
1. Creating a project with milestone view enabled
2. Creating work item types
3. Creating multiple work items
4. Creating multiple milestones
5. Adding work items to milestones
6. Updating milestone details
7. Listing work items in a milestone
8. Removing work items from a milestone

Usage:
    python test_milestones.py

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
from plane.models.milestones import CreateMilestone, UpdateMilestone  # noqa: E402
from plane.models.projects import CreateProject  # noqa: E402
from plane.models.work_item_types import CreateWorkItemType  # noqa: E402
from plane.models.work_items import CreateWorkItem  # noqa: E402


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

    print("Starting Milestone Test Suite")
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

        # Get current user for reference
        print_step(2, "Getting current user information")
        current_user = client.users.get_me()
        print_success(f"Current user: {current_user.display_name} (ID: {current_user.id})")

        # Create a project with milestone view enabled
        print_step(3, "Creating a new project")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_identifier = f"MIL{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Milestone Test Project {timestamp}",
            description="Testing milestone functionality end-to-end",
            identifier=project_identifier,
            emoji="🎯",
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")

        # Create work item types
        print_step(4, "Creating work item types")
        work_item_types = {}

        type_definitions = [
            {
                "key": "task",
                "name": "Task",
                "description": "A task to be completed",
                "is_epic": False,
            },
            {
                "key": "bug",
                "name": "Bug",
                "description": "A software bug that needs to be fixed",
                "is_epic": False,
            },
        ]

        for type_def in type_definitions:
            type_data = CreateWorkItemType(
                name=type_def["name"],
                description=type_def["description"],
                is_epic=type_def["is_epic"],
                is_active=True,
            )
            work_item_type = client.work_item_types.create(workspace_slug, project.id, type_data)
            work_item_types[type_def["key"]] = work_item_type
            print_success(
                f"Created work item type: {work_item_type.name} (ID: {work_item_type.id})"
            )

        # Create multiple work items
        print_step(5, "Creating work items")
        work_items = []

        work_item_definitions = [
            {
                "name": "Implement core API endpoints",
                "description": "Create REST API endpoints for core functionality",
                "priority": "high",
                "type_key": "task",
            },
            {
                "name": "Design user interface mockups",
                "description": "Design and document UI mockups",
                "priority": "high",
                "type_key": "task",
            },
            {
                "name": "Setup testing framework",
                "description": "Configure unit and integration testing",
                "priority": "medium",
                "type_key": "task",
            },
            {
                "name": "Fix data validation issue",
                "description": "Input data is not properly validated",
                "priority": "high",
                "type_key": "bug",
            },
            {
                "name": "Fix performance bottleneck",
                "description": "Slow response times on dashboard",
                "priority": "urgent",
                "type_key": "bug",
            },
        ]

        for item_def in work_item_definitions:
            work_item_data = CreateWorkItem(
                name=item_def["name"],
                description_html=f"<p>{item_def['description']}</p>",
                priority=item_def["priority"],
                type_id=work_item_types[item_def["type_key"]].id,
            )
            work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
            work_items.append(work_item)
            print_success(f"Created work item: {work_item.name} (ID: {work_item.id})")

        # Create multiple milestones
        print_step(6, "Creating multiple milestones")
        milestones = {}

        # Milestone 1: v1.0 Release
        v1_milestone_end = datetime.now() + timedelta(days=30)

        v1_milestone_data = CreateMilestone(
            title="v1.0 Release",
            target_date=v1_milestone_end.strftime("%Y-%m-%d"),
        )

        milestones["v1"] = client.milestones.create(workspace_slug, project.id, v1_milestone_data)
        print_success(f"Created milestone: {milestones['v1'].title} (ID: {milestones['v1'].id})")
        print(f"  Target date: {milestones['v1'].target_date}")

        # Milestone 2: v1.1 Release
        v1_1_milestone_end = datetime.now() + timedelta(days=51)

        v1_1_milestone_data = CreateMilestone(
            title="v1.1 Release",
            target_date=v1_1_milestone_end.strftime("%Y-%m-%d"),
        )

        milestones["v1_1"] = client.milestones.create(
            workspace_slug, project.id, v1_1_milestone_data
        )
        print_success(f"Created milestone: {milestones['v1_1'].title} (ID: {milestones['v1_1'].id})")

        # Milestone 3: v2.0 Release
        v2_milestone_data = CreateMilestone(
            title="v2.0 Release",
        )

        milestones["v2"] = client.milestones.create(workspace_slug, project.id, v2_milestone_data)
        print_success(f"Created milestone: {milestones['v2'].title} (ID: {milestones['v2'].id})")

        # Add work items to milestones
        print_step(7, "Adding work items to milestones")

        # Add core work items to v1.0 milestone
        v1_work_item_ids = [work_items[0].id, work_items[1].id, work_items[3].id]
        client.milestones.add_work_items(
            workspace_slug, project.id, milestones["v1"].id, v1_work_item_ids
        )
        print_success(f"Added {len(v1_work_item_ids)} work items to {milestones['v1'].title}")

        # Add testing work item to v1.1 milestone
        v1_1_work_item_ids = [work_items[2].id]
        client.milestones.add_work_items(
            workspace_slug, project.id, milestones["v1_1"].id, v1_1_work_item_ids
        )
        print_success(f"Added {len(v1_1_work_item_ids)} work item to {milestones['v1_1'].title}")

        # Add critical bug to v1.0 milestone
        critical_bug_ids = [work_items[4].id]
        client.milestones.add_work_items(
            workspace_slug, project.id, milestones["v1"].id, critical_bug_ids
        )
        print_success(f"Added critical bug to {milestones['v1'].title}")

        # List work items in milestones
        print_step(8, "Listing work items in milestones")

        for _, milestone in milestones.items():
            milestone_work_items = client.milestones.list_work_items(
                workspace_slug, project.id, milestone.id
            )
            print_success(f"{milestone.title} contains {milestone_work_items.count} work items")

        # Update milestone details
        print_step(9, "Updating milestone details")

        # Update v1.0 milestone title
        update_v1_data = UpdateMilestone(
            title="v1.0 Release - Updated",
        )
        updated_v1_milestone = client.milestones.update(
            workspace_slug, project.id, milestones["v1"].id, update_v1_data
        )
        print_success(f"Updated milestone title to: {updated_v1_milestone.title}")

        # Update v1.1 milestone target date
        new_v1_1_end = datetime.now() + timedelta(days=49)
        update_v1_1_data = UpdateMilestone(
            target_date=new_v1_1_end.strftime("%Y-%m-%d"),
        )
        updated_v1_1_milestone = client.milestones.update(
            workspace_slug, project.id, milestones["v1_1"].id, update_v1_1_data
        )
        print_success(f"Updated {updated_v1_1_milestone.title} target date")
        print(f"  New target date: {updated_v1_1_milestone.target_date}")

        # Retrieve a specific milestone
        print_step(10, "Retrieving specific milestone")
        retrieved_milestone = client.milestones.retrieve(
            workspace_slug, project.id, milestones["v1"].id
        )
        print_success(f"Retrieved milestone: {retrieved_milestone.title}")

        # List all milestones in project
        print_step(11, "Listing all milestones in project")
        all_milestones = client.milestones.list(workspace_slug, project.id)
        print_success(f"Found {all_milestones.count} milestones in project")
        for milestone in all_milestones.results:
            print(f"  - {milestone.title}")

        # Remove work items from a milestone
        print_step(12, "Removing work item from milestone")
        work_item_to_remove = [work_items[3].id]  # Data validation bug
        client.milestones.remove_work_items(
            workspace_slug, project.id, milestones["v1"].id, work_item_to_remove
        )
        print_success(f"Removed work item '{work_items[3].name}' from {milestones['v1'].title}")

        # Verify removal
        v1_work_items_after_removal = client.milestones.list_work_items(
            workspace_slug, project.id, milestones["v1"].id
        )
        print_success(
            f"{milestones['v1'].title} now contains "
            f"{v1_work_items_after_removal.count} work items"
        )

        # Final milestone count
        print_step(13, "Final verification")
        final_milestones = client.milestones.list(workspace_slug, project.id)
        print_success(f"Total milestones: {final_milestones.count}")

        # Cleanup: Delete created resources (optional)
        print_step(14, "Cleanup (optional)")
        try:
            choice = input("Delete test resources? (y/N): ").strip().lower()
        except EOFError:
            choice = "n"
        if choice == "y":
            # Delete milestones
            for milestone in milestones.values():
                try:
                    client.milestones.delete(workspace_slug, project.id, milestone.id)
                    print_success(f"Deleted milestone: {milestone.title}")
                except Exception as e:
                    print_error(f"Failed to delete milestone {milestone.id}: {e}")

            # Delete work items
            for work_item in work_items:
                try:
                    client.work_items.delete(workspace_slug, project.id, work_item.id)
                    print_success(f"Deleted work item: {work_item.id}")
                except Exception as e:
                    print_error(f"Failed to delete work item {work_item.id}: {e}")

            # Delete project
            try:
                client.projects.delete(workspace_slug, project.id)
                print_success("Deleted test project")
            except Exception as e:
                print_error(f"Failed to delete project: {e}")
        else:
            print_success("Keeping test resources for inspection")

        # Summary
        print_step(15, "Test Summary")
        print(f"✓ Project created: {project.name}")
        print(f"✓ Work item types created: {len(work_item_types)}")
        print(f"✓ Work items created: {len(work_items)}")
        print(f"✓ Milestones created: {len(milestones)}")
        print("✓ Work items added to milestones")
        print("✓ Work items removed from milestones")
        print("✓ Milestones updated (title, target date)")
        print("✓ Milestone retrieved successfully")
        print("✓ Milestones listed successfully")
        print("\nAll milestone tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
