#!/usr/bin/env python3
"""
Comprehensive test script for testing SDK Module functionality end-to-end.

This script demonstrates:
1. Creating a project with module view enabled
2. Creating work item types
3. Creating multiple work items
4. Creating multiple modules with different configurations
5. Adding work items to modules
6. Updating module details and status
7. Listing work items in a module
8. Removing work items from a module
9. Archiving and unarchiving modules
10. Listing archived modules

Usage:
    python test_modules.py

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
from plane.models.enums import ModuleStatus  # noqa: E402
from plane.models.modules import CreateModule, UpdateModule  # noqa: E402
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

    print("Starting Module Test Suite")
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

        # Get current user for module lead assignment
        print_step(2, "Getting current user information")
        current_user = client.users.get_me()
        print_success(f"Current user: {current_user.display_name} (ID: {current_user.id})")

        # Create a project with module view enabled
        print_step(3, "Creating a new project with module view enabled")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_identifier = f"MOD{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Module Test Project {timestamp}",
            description="Testing module functionality end-to-end",
            identifier=project_identifier,
            emoji="📦",
            module_view=True,
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")
        print(f"  Module view enabled: {project.module_view}")

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
                "name": "Implement user authentication module",
                "description": "Create authentication module with login/logout",
                "priority": "high",
                "type_key": "task",
            },
            {
                "name": "Design database schema",
                "description": "Design and document database schema",
                "priority": "high",
                "type_key": "task",
            },
            {
                "name": "Setup CI/CD pipeline",
                "description": "Configure continuous integration and deployment",
                "priority": "medium",
                "type_key": "task",
            },
            {
                "name": "Fix login redirect issue",
                "description": "Users are not redirected after login",
                "priority": "high",
                "type_key": "bug",
            },
            {
                "name": "Fix memory leak in API",
                "description": "Memory leak detected in API endpoints",
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

        # Create multiple modules with different configurations
        print_step(6, "Creating multiple modules")
        modules = {}

        # Module 1: Authentication Module (in progress)
        auth_module_start = datetime.now()
        auth_module_end = auth_module_start + timedelta(days=21)

        auth_module_data = CreateModule(
            name="Authentication Module",
            description="User authentication and authorization features",
            start_date=auth_module_start.strftime("%Y-%m-%d"),
            target_date=auth_module_end.strftime("%Y-%m-%d"),
            status=ModuleStatus.IN_PROGRESS.value,
            lead=current_user.id,
            members=[current_user.id],
        )

        modules["auth"] = client.modules.create(workspace_slug, project.id, auth_module_data)
        print_success(f"Created module: {modules['auth'].name} (ID: {modules['auth'].id})")
        print(f"  Status: {modules['auth'].status}")
        print(f"  Start date: {modules['auth'].start_date}")
        print(f"  Target date: {modules['auth'].target_date}")

        # Module 2: Database Module (planned)
        db_module_start = datetime.now() + timedelta(days=7)
        db_module_end = db_module_start + timedelta(days=14)

        db_module_data = CreateModule(
            name="Database Schema",
            description="Database design and implementation",
            start_date=db_module_start.strftime("%Y-%m-%d"),
            target_date=db_module_end.strftime("%Y-%m-%d"),
            status=ModuleStatus.PLANNED.value,
            lead=current_user.id,
        )

        modules["database"] = client.modules.create(workspace_slug, project.id, db_module_data)
        print_success(f"Created module: {modules['database'].name} (ID: {modules['database'].id})")
        print(f"  Status: {modules['database'].status}")

        # Module 3: DevOps Module (backlog)
        devops_module_data = CreateModule(
            name="DevOps Infrastructure",
            description="CI/CD and deployment infrastructure",
            status=ModuleStatus.BACKLOG.value,
            lead=current_user.id,
        )

        modules["devops"] = client.modules.create(workspace_slug, project.id, devops_module_data)
        print_success(f"Created module: {modules['devops'].name} (ID: {modules['devops'].id})")
        print(f"  Status: {modules['devops'].status}")

        # Add work items to modules
        print_step(7, "Adding work items to modules")

        # Add authentication-related work items to auth module
        auth_work_item_ids = [work_items[0].id, work_items[3].id]  # Auth task and bug
        client.modules.add_work_items(
            workspace_slug, project.id, modules["auth"].id, auth_work_item_ids
        )
        print_success(f"Added {len(auth_work_item_ids)} work items to {modules['auth'].name}")

        # Add database work item to database module
        db_work_item_ids = [work_items[1].id]  # Database task
        client.modules.add_work_items(
            workspace_slug, project.id, modules["database"].id, db_work_item_ids
        )
        print_success(f"Added {len(db_work_item_ids)} work item to {modules['database'].name}")

        # Add DevOps work item to devops module
        devops_work_item_ids = [work_items[2].id]  # CI/CD task
        client.modules.add_work_items(
            workspace_slug, project.id, modules["devops"].id, devops_work_item_ids
        )
        print_success(f"Added {len(devops_work_item_ids)} work item to {modules['devops'].name}")

        # Add critical bug to multiple modules
        critical_bug_ids = [work_items[4].id]  # Memory leak bug
        client.modules.add_work_items(
            workspace_slug, project.id, modules["auth"].id, critical_bug_ids
        )
        client.modules.add_work_items(
            workspace_slug, project.id, modules["devops"].id, critical_bug_ids
        )
        print_success(
            f"Added critical bug to both {modules['auth'].name} and " f"{modules['devops'].name}"
        )

        # List work items in modules
        print_step(8, "Listing work items in modules")

        for _, module in modules.items():
            module_work_items = client.modules.list_work_items(
                workspace_slug, project.id, module.id
            )
            print_success(f"{module.name} contains {module_work_items.count} work items")

        # Update module details
        print_step(9, "Updating module details")

        # Update auth module status to completed
        update_auth_data = UpdateModule(
            status=ModuleStatus.COMPLETED.value,
            description="User authentication and authorization features - COMPLETED",
        )
        updated_auth_module = client.modules.update(
            workspace_slug, project.id, modules["auth"].id, update_auth_data
        )
        print_success(f"Updated {updated_auth_module.name} status to: {updated_auth_module.status}")

        # Update database module dates
        new_db_start = datetime.now()
        new_db_end = new_db_start + timedelta(days=10)
        update_db_data = UpdateModule(
            start_date=new_db_start.strftime("%Y-%m-%d"),
            target_date=new_db_end.strftime("%Y-%m-%d"),
            status=ModuleStatus.IN_PROGRESS.value,
        )
        updated_db_module = client.modules.update(
            workspace_slug, project.id, modules["database"].id, update_db_data
        )
        print_success(f"Updated {updated_db_module.name} status to: {updated_db_module.status}")
        print(f"  New start date: {updated_db_module.start_date}")
        print(f"  New target date: {updated_db_module.target_date}")

        # Retrieve a specific module
        print_step(10, "Retrieving specific module")
        retrieved_module = client.modules.retrieve(workspace_slug, project.id, modules["auth"].id)
        print_success(f"Retrieved module: {retrieved_module.name}")
        print(f"  Total work items: {retrieved_module.total_issues}")
        print(f"  Completed work items: {retrieved_module.completed_issues}")
        print(f"  In-progress work items: {retrieved_module.started_issues}")

        # List all modules in project
        print_step(11, "Listing all modules in project")
        all_modules = client.modules.list(workspace_slug, project.id)
        print_success(f"Found {all_modules.count} modules in project")
        for module in all_modules.results:
            print(f"  - {module.name} (Status: {module.status})")

        # Remove a work item from a module
        print_step(12, "Removing work item from module")
        work_item_to_remove = work_items[3].id  # Login redirect bug
        client.modules.remove_work_item(
            workspace_slug, project.id, modules["auth"].id, work_item_to_remove
        )
        print_success(f"Removed work item '{work_items[3].name}' from {modules['auth'].name}")

        # Verify removal
        auth_work_items_after_removal = client.modules.list_work_items(
            workspace_slug, project.id, modules["auth"].id
        )
        print_success(
            f"{modules['auth'].name} now contains "
            f"{auth_work_items_after_removal.count} work items"
        )

        # Archive a module
        print_step(13, "Archiving a module")
        # First update the devops module to completed status
        # (only completed/cancelled can be archived)
        update_devops_data = UpdateModule(status=ModuleStatus.COMPLETED.value)
        client.modules.update(workspace_slug, project.id, modules["devops"].id, update_devops_data)
        print_success(
            f"Updated {modules['devops'].name} status to completed (required for archiving)"
        )

        # Now archive it
        client.modules.archive(workspace_slug, project.id, modules["devops"].id)
        print_success(f"Archived module: {modules['devops'].name}")

        # List archived modules
        print_step(14, "Listing archived modules")
        archived_modules = client.modules.list_archived(workspace_slug, project.id)
        print_success(f"Found {archived_modules.count} archived modules")
        for module in archived_modules.results:
            print(f"  - {module.name} (Archived at: {module.archived_at})")

        # Unarchive the module
        print_step(15, "Unarchiving a module")
        client.modules.unarchive(workspace_slug, project.id, modules["devops"].id)
        print_success(f"Unarchived module: {modules['devops'].name}")

        # Final module count
        print_step(16, "Final verification")
        final_modules = client.modules.list(workspace_slug, project.id)
        print_success(f"Total active modules: {final_modules.count}")

        final_archived_modules = client.modules.list_archived(workspace_slug, project.id)
        print_success(f"Total archived modules: {final_archived_modules.count}")

        # Cleanup: Delete created resources (optional)
        print_step(17, "Cleanup (optional)")
        choice = input("Delete test resources? (y/N): ").strip().lower()
        if choice == "y":
            # Delete modules
            for module in modules.values():
                try:
                    client.modules.delete(workspace_slug, project.id, module.id)
                    print_success(f"Deleted module: {module.name}")
                except Exception as e:
                    print_error(f"Failed to delete module {module.id}: {e}")

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
        print_step(18, "Test Summary")
        print(f"✓ Project created: {project.name}")
        print(f"✓ Work item types created: {len(work_item_types)}")
        print(f"✓ Work items created: {len(work_items)}")
        print(f"✓ Modules created: {len(modules)}")
        print("✓ Module statuses tested:")
        print(f"    - {ModuleStatus.BACKLOG.value}")
        print(f"    - {ModuleStatus.PLANNED.value}")
        print(f"    - {ModuleStatus.IN_PROGRESS.value}")
        print(f"    - {ModuleStatus.COMPLETED.value}")
        print("✓ Work items added to modules")
        print("✓ Work items removed from modules")
        print("✓ Modules updated (status, dates, description)")
        print("✓ Module retrieved successfully")
        print("✓ Modules listed successfully")
        print("✓ Module archived and unarchived")
        print("\nAll module tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
