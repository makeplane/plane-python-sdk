#!/usr/bin/env python3
"""
Comprehensive test script for testing all cycles resources end-to-end.

This script demonstrates:
1. Creating a project with cycle view enabled
2. Creating multiple cycles
3. Testing cycle CRUD operations
4. Testing cycle archive/unarchive
5. Testing adding and removing work items from cycles
6. Testing transferring work items between cycles
7. Testing listing cycles and archived cycles

Usage:
    python test_cycles.py

Requirements:
    - Set BASE_URL environment variable (e.g., https://api.plane.so)
    - Set either API_KEY or ACCESS_TOKEN environment variable
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
from plane.models.cycles import CreateCycle, TransferCycleWorkItemsRequest, UpdateCycle  # noqa: E402
from plane.models.projects import CreateProject  # noqa: E402
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

    print("Starting Comprehensive Cycles SDK Test")
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

        # Get current user for cycle ownership
        print_step(2, "Getting current user information")
        current_user = client.users.get_me()
        print_success(f"Current user: {current_user.display_name} (ID: {current_user.id})")

        # Create a project with cycle view enabled
        print_step(3, "Creating a test project with cycle view enabled")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_identifier = f"CY{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Cycles Test {timestamp}",
            description="Testing all cycles resources",
            identifier=project_identifier,
            emoji="📅",
            cycle_view=True,
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")

        # Create some work items for cycle testing
        print_step(4, "Creating work items for cycle testing")
        work_items = []

        for i in range(5):
            work_item_data = CreateWorkItem(
                name=f"Work Item {i+1} for Cycle Testing",
                description_html=f"<p>Work item {i+1} to be used in cycle tests.</p>",
                priority=["urgent", "high", "medium", "low", "none"][i],
            )
            work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
            work_items.append(work_item)
            print_success(f"Created work item: {work_item.name} (ID: {work_item.id})")

        # Create multiple cycles
        print_step(5, "Creating multiple cycles")
        cycles = []

        # Create cycle 1 with future end_date so we can add work items to it
        # We'll complete it later by updating the end_date to the past
        cycle_start_1 = datetime.now() - timedelta(days=7)
        cycle_end_1 = datetime.now() + timedelta(days=7)  # Ends in a week
        cycle_data_1 = CreateCycle(
            name=f"Sprint 1 - Cycle {timestamp}",
            description="First sprint cycle for testing",
            start_date=cycle_start_1.strftime("%Y-%m-%d"),
            end_date=cycle_end_1.strftime("%Y-%m-%d"),
            owned_by=current_user.id,
            project_id=project.id,
        )
        cycle_1 = client.cycles.create(workspace_slug, project.id, cycle_data_1)
        cycles.append(cycle_1)
        print_success(f"Created cycle: {cycle_1.name} (ID: {cycle_1.id})")

        cycle_start_2 = datetime.now() + timedelta(days=15)
        cycle_end_2 = cycle_start_2 + timedelta(days=14)
        cycle_data_2 = CreateCycle(
            name=f"Sprint 2 - Cycle {timestamp}",
            description="Second sprint cycle for testing",
            start_date=cycle_start_2.strftime("%Y-%m-%d"),
            end_date=cycle_end_2.strftime("%Y-%m-%d"),
            owned_by=current_user.id,
            project_id=project.id,
        )
        cycle_2 = client.cycles.create(workspace_slug, project.id, cycle_data_2)
        cycles.append(cycle_2)
        print_success(f"Created cycle: {cycle_2.name} (ID: {cycle_2.id})")

        # Test cycle retrieve
        print_step(6, "Testing cycle retrieve")
        retrieved_cycle = client.cycles.retrieve(
            workspace_slug, project.id, cycle_1.id
        )
        print_success(f"Retrieved cycle: {retrieved_cycle.name}")

        # Test cycle update (only active cycles can be updated)
        # Note: Completed cycles (end_date in the past) cannot be edited
        print_step(7, "Testing cycle update (on active cycle)")
        update_data = UpdateCycle(
            name=f"{cycle_2.name} (Updated)",
            description="Updated description for the active cycle",
        )
        updated_cycle = client.cycles.update(
            workspace_slug, project.id, cycle_2.id, update_data
        )
        print_success(f"Updated cycle: {updated_cycle.name}")
        print_success(
            "Note: Only active cycles (end_date in future) can be updated"
        )

        # Test cycle list
        print_step(8, "Testing cycle list operations")
        listed_cycles = client.cycles.list(workspace_slug, project.id)
        print_success(f"Listed {len(listed_cycles.results)} cycles")

        # Add work items to cycle 1 (still active, can add work items)
        # Note: Cannot add work items to completed cycles (end_date in the past)
        print_step(9, "Adding work items to cycle 1")
        work_item_ids_1 = [wi.id for wi in work_items[:3]]
        client.cycles.add_work_items(
            workspace_slug, project.id, cycle_1.id, work_item_ids_1
        )
        print_success(f"Added {len(work_item_ids_1)} work items to cycle 1")

        # Add work items to cycle 2 (active cycle)
        print_step(10, "Adding work items to cycle 2")
        work_item_ids_2 = [wi.id for wi in work_items[3:]]
        if work_item_ids_2:
            client.cycles.add_work_items(
                workspace_slug, project.id, cycle_2.id, work_item_ids_2
            )
            print_success(f"Added {len(work_item_ids_2)} work items to cycle 2")

        # List work items in cycles
        print_step(11, "Listing work items in cycles")
        cycle_1_work_items = client.cycles.list_work_items(
            workspace_slug, project.id, cycle_1.id
        )
        print_success(
            f"Cycle 1 contains {cycle_1_work_items.count} work items "
            f"({len(cycle_1_work_items.results)} returned)"
        )

        cycle_2_work_items = client.cycles.list_work_items(
            workspace_slug, project.id, cycle_2.id
        )
        print_success(
            f"Cycle 2 contains {cycle_2_work_items.count} work items "
            f"({len(cycle_2_work_items.results)} returned)"
        )

        # Remove a work item from cycle 1
        print_step(12, "Removing a work item from cycle")
        if work_item_ids_1:
            client.cycles.remove_work_item(
                workspace_slug, project.id, cycle_1.id, work_item_ids_1[0]
            )
            print_success(f"Removed work item {work_item_ids_1[0][:8]}... from cycle 1")

            # Verify removal
            cycle_1_work_items_after = client.cycles.list_work_items(
                workspace_slug, project.id, cycle_1.id
            )
            print_success(
                f"Cycle 1 now contains {cycle_1_work_items_after.count} work items"
            )

        # Complete cycle 1 by setting end_date to the past
        # Note: This makes it a completed cycle (required for archiving)
        print_step(13, "Completing cycle 1 (setting end_date to past)")
        completed_end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        complete_data = UpdateCycle(end_date=completed_end_date)
        client.cycles.update(workspace_slug, project.id, cycle_1.id, complete_data)
        print_success(
            f"Completed cycle 1 (end_date set to {completed_end_date})"
        )

        # Archive cycle 1 (required before transferring work items)
        # Note: Only cycles with end_date in the past can be archived
        print_step(14, "Archiving cycle 1 (required for transfer)")
        archived = client.cycles.archive(workspace_slug, project.id, cycle_1.id)
        if archived:
            print_success(f"Archived cycle: {cycle_1.name} (ID: {cycle_1.id})")
        else:
            print_error("Failed to archive cycle")

        # Transfer work items from archived cycle 1 to cycle 2
        # (Transfer only works from completed/archived cycles)
        print_step(15, "Transferring work items from archived cycle")
        cycle_1_work_items_before = client.cycles.list_work_items(
            workspace_slug, project.id, cycle_1.id
        )
        if cycle_1_work_items_before.count > 0:
            transfer_data = TransferCycleWorkItemsRequest(new_cycle_id=cycle_2.id)
            client.cycles.transfer_work_items(
                workspace_slug, project.id, cycle_1.id, transfer_data
            )
            print_success(
                "Transferred all work items from archived cycle 1 to cycle 2"
            )

            # Verify transfer
            cycle_1_after_transfer = client.cycles.list_work_items(
                workspace_slug, project.id, cycle_1.id
            )
            cycle_2_after_transfer = client.cycles.list_work_items(
                workspace_slug, project.id, cycle_2.id
            )
            print_success(
                f"After transfer: Cycle 1 has {cycle_1_after_transfer.count} work items, "
                f"Cycle 2 has {cycle_2_after_transfer.count} work items"
            )
        else:
            print_success("Cycle 1 has no work items to transfer (skipping transfer test)")

        # List archived cycles
        print_step(16, "Listing archived cycles")
        archived_cycles = client.cycles.list_archived(workspace_slug, project.id)
        print_success(f"Found {len(archived_cycles.results)} archived cycles")

        # Unarchive the cycle
        print_step(17, "Testing cycle unarchive")
        unarchived = client.cycles.unarchive(
            workspace_slug, project.id, cycle_1.id
        )
        if unarchived:
            print_success(f"Unarchived cycle: {cycle_1.name} (ID: {cycle_1.id})")
        else:
            print_error("Failed to unarchive cycle")

        # Verify archived cycles list after unarchive
        archived_after_unarchive = client.cycles.list_archived(workspace_slug, project.id)
        print_success(f"After unarchive: {len(archived_after_unarchive.results)} archived cycles")

        # Cleanup: Delete created resources (optional, comment out to keep for inspection)
        print_step(18, "Cleanup (optional)")
        choice = input("Delete test resources? (y/N): ").strip().lower()
        if choice == "y":
            # Delete cycles
            for cycle in cycles:
                try:
                    client.cycles.delete(workspace_slug, project.id, cycle.id)
                    print_success(f"Deleted cycle: {cycle.id}")
                except Exception as e:
                    print_error(f"Failed to delete cycle {cycle.id}: {e}")

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
        print_step(19, "Test Summary")
        print("✓ All cycle CRUD operations tested")
        print("  - Create, retrieve, update, list")
        print("✓ Cycle work item operations tested")
        print("  - Add work items, remove work item, list work items")
        print("✓ Cycle transfer tested")
        print("  - Transfer work items between cycles")
        print("✓ Cycle archive/unarchive tested")
        print("  - Archive cycle, list archived, unarchive cycle")
        print(f"✓ Created {len(cycles)} cycles")
        print(f"✓ Created {len(work_items)} work items")
        print("\nAll cycles resource tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

