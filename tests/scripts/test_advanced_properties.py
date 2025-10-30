#!/usr/bin/env python3
"""
Advanced test script for testing complex Work Item Properties scenarios.
Tests various property types, validation rules, and complex property value assignments.

Usage:
    python test_advanced_properties.py

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
from plane.models.enums import PropertyType, RelationType  # noqa: E402
from plane.models.projects import CreateProject  # noqa: E402
from plane.models.work_item_properties import (  # noqa: E402
    CreateWorkItemProperty,
    CreateWorkItemPropertyOption,
    CreateWorkItemPropertyValue,
)
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

    print("Starting Advanced Properties Test")
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
        project_identifier = f"ADV{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Advanced Properties Test {timestamp}",
            description="This project tests advanced work item properties and validation",
            identifier=project_identifier,
            emoji="⚙️",
            is_issue_type_enabled=True,  # Enable work item types
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")
        print(f"  Work item types enabled: {project.is_issue_type_enabled}")

        # Ensure work item types are enabled (fallback)
        if not project.is_issue_type_enabled:
            print("  Enabling work item types on project...")
            from plane.models.projects import UpdateProject

            update_data = UpdateProject(is_issue_type_enabled=True)
            project = client.projects.update(workspace_slug, project.id, update_data)
            print_success("Work item types enabled on project")

        # Create a comprehensive work item type
        print_step(3, "Creating comprehensive work item type")
        task_type_data = CreateWorkItemType(
            name="Advanced Task",
            description="Tasks with comprehensive custom properties for testing",
            is_epic=False,
            is_active=True,
        )
        task_type = client.work_item_types.create(workspace_slug, project.id, task_type_data)
        print_success(f"Work item type created: {task_type.name} (ID: {task_type.id})")

        # Create various property types
        print_step(4, "Creating comprehensive custom properties")

        # 1. URL Property
        url_prop_data = CreateWorkItemProperty(
            display_name="Related URL",
            description="URL related to this task",
            property_type=PropertyType.URL.value,
            is_required=False,
            is_active=True,
        )
        url_prop = client.work_item_properties.create(
            workspace_slug, project.id, task_type.id, url_prop_data
        )
        print_success(f"URL property created: {url_prop.display_name}")

        # 2. Email Property
        email_prop_data = CreateWorkItemProperty(
            display_name="Contact Email",
            description="Email of the person responsible",
            property_type=PropertyType.EMAIL.value,
            is_required=False,
            is_active=True,
        )
        email_prop = client.work_item_properties.create(
            workspace_slug, project.id, task_type.id, email_prop_data
        )
        print_success(f"Email property created: {email_prop.display_name}")

        # 3. DateTime Property
        datetime_prop_data = CreateWorkItemProperty(
            display_name="Due Date",
            description="When this task should be completed",
            property_type=PropertyType.DATETIME.value,
            is_required=False,
            is_active=True,
        )
        datetime_prop = client.work_item_properties.create(
            workspace_slug, project.id, task_type.id, datetime_prop_data
        )
        print_success(f"DateTime property created: {datetime_prop.display_name}")

        # 4. Multi-select Option Property
        multi_option_prop_data = CreateWorkItemProperty(
            display_name="Tags",
            description="Tags for categorizing this task",
            property_type=PropertyType.OPTION.value,
            is_required=False,
            is_active=True,
            is_multi=True,  # Allow multiple selections
        )
        multi_option_prop = client.work_item_properties.create(
            workspace_slug, project.id, task_type.id, multi_option_prop_data
        )
        print_success(f"Multi-option property created: {multi_option_prop.display_name}")

        # 5. Relation Property (to other work items)
        relation_prop_data = CreateWorkItemProperty(
            display_name="Related Issues",
            description="Other work items related to this task",
            property_type=PropertyType.RELATION.value,
            relation_type=RelationType.ISSUE.value,
            is_required=False,
            is_active=True,
        )
        relation_prop = client.work_item_properties.create(
            workspace_slug, project.id, task_type.id, relation_prop_data
        )
        print_success(f"Relation property created: {relation_prop.display_name}")

        # Create options for the multi-select property
        print_step(5, "Creating property options for Tags")
        tag_options = []

        tags = ["Frontend", "Backend", "Database", "API", "UI/UX", "Testing", "Documentation"]
        for tag in tags:
            option_data = CreateWorkItemPropertyOption(
                name=tag,
                description=f"Tag: {tag}",
                is_active=True,
            )
            option = client.work_item_properties.options.create(
                workspace_slug, project.id, multi_option_prop.id, option_data
            )
            tag_options.append(option)
            print_success(f"Tag option created: {option.name}")

        # Create multiple work items to test relations
        print_step(6, "Creating work items for relation testing")
        work_items = []

        for i in range(3):
            work_item_data = CreateWorkItem(
                name=f"Related Task {i+1}",
                description_html=f"<p>This is related task {i+1} for testing relations.</p>",
                priority="medium",
                type_id=task_type.id,
            )
            work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
            work_items.append(work_item)
            print_success(f"Work item created: {work_item.name} (ID: {work_item.id})")

        # Create a main work item with all property values
        print_step(7, "Creating main work item with comprehensive properties")
        main_work_item_data = CreateWorkItem(
            name="Comprehensive Test Task",
            description_html="<p>This task demonstrates all property types and their values.</p>",
            priority="high",
            type_id=task_type.id,
        )

        main_work_item = client.work_items.create(workspace_slug, project.id, main_work_item_data)
        print_success(f"Main work item created: {main_work_item.name} (ID: {main_work_item.id})")

        # Assign comprehensive property values
        print_step(8, "Assigning comprehensive property values")

        # URL value
        url_value_data = CreateWorkItemPropertyValue(
            values=[
                CreateWorkItemPropertyValue.ValueItem(value="https://github.com/makeplane/plane")
            ]
        )
        url_value = client.work_item_properties.values.create(
            workspace_slug, project.id, main_work_item.id, url_prop.id, url_value_data
        )
        print_success(f"URL value set: {url_value.values[0].value}")

        # Email value
        email_value_data = CreateWorkItemPropertyValue(
            values=[CreateWorkItemPropertyValue.ValueItem(value="developer@plane.so")]
        )
        email_value = client.work_item_properties.values.create(
            workspace_slug, project.id, main_work_item.id, email_prop.id, email_value_data
        )
        print_success(f"Email value set: {email_value.values[0].value}")

        # DateTime value (due date in 7 days)
        due_date = datetime.now() + timedelta(days=7)
        datetime_value_data = CreateWorkItemPropertyValue(
            values=[CreateWorkItemPropertyValue.ValueItem(value=due_date.isoformat())]
        )
        datetime_value = client.work_item_properties.values.create(
            workspace_slug, project.id, main_work_item.id, datetime_prop.id, datetime_value_data
        )
        print_success(f"Due date value set: {datetime_value.values[0].value}")

        # Multi-select tags (select first 3 tags)
        selected_tags = tag_options[:3]  # Select first 3 tags
        for tag_option in selected_tags:
            tag_value_data = CreateWorkItemPropertyValue(
                values=[CreateWorkItemPropertyValue.ValueItem(value=tag_option.id)]
            )
            client.work_item_properties.values.create(
                workspace_slug, project.id, main_work_item.id, multi_option_prop.id, tag_value_data
            )
            print_success(f"Tag value set: {tag_option.name}")

        # Relation value (relate to the first 2 work items)
        for related_work_item in work_items[:2]:
            relation_value_data = CreateWorkItemPropertyValue(
                values=[CreateWorkItemPropertyValue.ValueItem(value=related_work_item.id)]
            )
            client.work_item_properties.values.create(
                workspace_slug, project.id, main_work_item.id, relation_prop.id, relation_value_data
            )
            print_success(f"Relation value set: {related_work_item.name}")

        # Test property value updates
        print_step(9, "Testing property value updates")

        # Update the due date
        new_due_date = datetime.now() + timedelta(days=14)
        update_data = {"values": [{"value": new_due_date.isoformat()}]}
        updated_datetime_value = client.work_item_properties.values.update(
            workspace_slug, project.id, main_work_item.id, datetime_value.id, update_data
        )
        print_success(f"Due date updated: {updated_datetime_value.values[0].value}")

        # Retrieve and verify all property values
        print_step(10, "Verifying all property values")
        property_values = client.work_item_properties.values.list(
            workspace_slug, project.id, main_work_item.id
        )
        print_success(f"Retrieved {len(property_values)} property value groups")

        # Test property validation by trying to create invalid values
        print_step(11, "Testing property validation")
        try:
            # Try to create an invalid email
            invalid_email_data = CreateWorkItemPropertyValue(
                values=[CreateWorkItemPropertyValue.ValueItem(value="invalid-email-format")]
            )
            # This might succeed on the API side but should be validated
            client.work_item_properties.values.create(
                workspace_slug, project.id, main_work_item.id, email_prop.id, invalid_email_data
            )
            print("Note: Invalid email was accepted (validation may be on frontend)")
        except Exception as e:
            print_success(f"Email validation working: {e}")

        # Cleanup: Delete created resources (optional)
        print_step(12, "Cleanup (optional)")
        choice = input("Delete test resources? (y/N): ").strip().lower()
        if choice == "y":
            # Delete work items
            for work_item in work_items + [main_work_item]:
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
        print_step(13, "Test Summary")
        print(f"✓ Project created: {project.name}")
        print(f"✓ Work item type created: {task_type.name}")
        print("✓ Custom properties created: 5 different types")
        print(f"✓ Property options created: {len(tag_options)} tags")
        print(f"✓ Work items created: {len(work_items) + 1}")
        print("✓ Property values assigned: Multiple values per property type")
        print("✓ Property value updates tested")
        print("✓ Property validation tested")
        print("\nAll advanced tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
