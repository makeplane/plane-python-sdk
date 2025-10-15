#!/usr/bin/env python3
"""
Focused test script for testing Work Item Property Values operations.
Tests creating, updating, retrieving, and deleting property values.

This test validates the single-value API where each work item has
exactly ONE value per property, and the create operation acts as an upsert.

Usage:
    python test_property_values.py

Requirements:
    - Set BASE_URL environment variable (e.g., https://api.plane.so)
    - Set either API_KEY or ACCESS_TOKEN environment variable
    - Set WORKSPACE_SLUG environment variable
"""

import os
import sys
from datetime import datetime, timedelta

from plane.client import PlaneClient
from plane.models.enums import PropertyType
from plane.models.projects import CreateProject
from plane.models.work_item_properties import (
    CreateWorkItemProperty,
    CreateWorkItemPropertyOption,
    CreateWorkItemPropertyValue,
)
from plane.models.work_item_property_configurations import (
    DateAttributeSettings,
    TextAttributeSettings,
)
from plane.models.work_item_types import CreateWorkItemType
from plane.models.work_items import CreateWorkItem


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

    print("Starting Property Values Test")
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
        project_identifier = f"VAL{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Property Values Test {timestamp}",
            description="This project tests property value operations",
            identifier=project_identifier,
            emoji="📊",
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

        # Create a work item type
        print_step(3, "Creating work item type")
        task_type_data = CreateWorkItemType(
            name="Property Test Task",
            description="Tasks for testing property values",
            is_epic=False,
            is_active=True,
        )
        task_type = client.work_item_types.create(workspace_slug, project.id, task_type_data)
        print_success(f"Work item type created: {task_type.name} (ID: {task_type.id})")

        # Create various property types for testing
        print_step(4, "Creating properties for value testing")
        properties = {}

        # Text property
        text_prop_data = CreateWorkItemProperty(
            display_name="Description",
            description="Text description",
            property_type=PropertyType.TEXT.value,
            is_required=False,
            is_active=True,
            settings=TextAttributeSettings(display_format="multi-line"),
        )
        text_prop = client.work_item_properties.create(
            workspace_slug, project.id, task_type.id, text_prop_data
        )
        properties["text"] = text_prop
        print_success(f"Text property created: {text_prop.display_name}")

        # Boolean property
        bool_prop_data = CreateWorkItemProperty(
            display_name="Is Completed",
            description="Whether the task is completed",
            property_type=PropertyType.BOOLEAN.value,
            is_required=False,
            is_active=True,
        )
        bool_prop = client.work_item_properties.create(
            workspace_slug, project.id, task_type.id, bool_prop_data
        )
        properties["boolean"] = bool_prop
        print_success(f"Boolean property created: {bool_prop.display_name}")

        # Decimal property
        decimal_prop_data = CreateWorkItemProperty(
            display_name="Progress",
            description="Progress percentage (0-100)",
            property_type=PropertyType.DECIMAL.value,
            is_required=False,
            is_active=True,
        )
        decimal_prop = client.work_item_properties.create(
            workspace_slug, project.id, task_type.id, decimal_prop_data
        )
        properties["decimal"] = decimal_prop
        print_success(f"Decimal property created: {decimal_prop.display_name}")

        # DateTime property
        datetime_prop_data = CreateWorkItemProperty(
            display_name="Start Date",
            description="When the task started",
            property_type=PropertyType.DATETIME.value,
            is_required=False,
            is_active=True,
            settings=DateAttributeSettings(display_format="MMM dd, yyyy"),
        )
        datetime_prop = client.work_item_properties.create(
            workspace_slug, project.id, task_type.id, datetime_prop_data
        )
        properties["datetime"] = datetime_prop
        print_success(f"DateTime property created: {datetime_prop.display_name}")

        # Option property
        option_prop_data = CreateWorkItemProperty(
            display_name="Status",
            description="Current status of the task",
            property_type=PropertyType.OPTION.value,
            is_required=False,
            is_active=True,
        )
        option_prop = client.work_item_properties.create(
            workspace_slug, project.id, task_type.id, option_prop_data
        )
        properties["option"] = option_prop
        print_success(f"Option property created: {option_prop.display_name}")

        # Create options for the option property
        print_step(5, "Creating property options")
        status_options = []

        statuses = ["Not Started", "In Progress", "Review", "Completed", "Cancelled"]
        for status in statuses:
            option_data = CreateWorkItemPropertyOption(
                name=status,
                description=f"Status: {status}",
                is_active=True,
            )
            option = client.work_item_properties.options.create(
                workspace_slug, project.id, option_prop.id, option_data
            )
            status_options.append(option)
            print_success(f"Status option created: {option.name}")

        # Create work items for testing
        print_step(6, "Creating work items for property value testing")
        work_items = []

        for i in range(3):
            work_item_data = CreateWorkItem(
                name=f"Test Task {i+1}",
                description_html=f"<p>This is test task {i+1} for property value testing.</p>",
                priority="medium",
                type_id=task_type.id,
            )
            work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
            work_items.append(work_item)
            print_success(f"Work item created: {work_item.name} (ID: {work_item.id})")

        # Test property value operations
        print_step(7, "Testing property value operations")

        # Create property values for the first work item
        main_work_item = work_items[0]
        property_values = {}

        # Text value
        text_value_data = CreateWorkItemPropertyValue(
            value="This is a detailed description for testing."
        )
        text_value = client.work_item_properties.values.create(
            workspace_slug, project.id, main_work_item.id, text_prop.id, text_value_data
        )
        property_values["text"] = text_value
        print_success(f"Text value created: {text_value.value}")

        # Boolean value
        bool_value_data = CreateWorkItemPropertyValue(value="false")
        bool_value = client.work_item_properties.values.create(
            workspace_slug, project.id, main_work_item.id, bool_prop.id, bool_value_data
        )
        property_values["boolean"] = bool_value
        print_success(f"Boolean value created: {bool_value.value}")

        # Decimal value
        decimal_value_data = CreateWorkItemPropertyValue(value="25.5")
        decimal_value = client.work_item_properties.values.create(
            workspace_slug, project.id, main_work_item.id, decimal_prop.id, decimal_value_data
        )
        property_values["decimal"] = decimal_value
        print_success(f"Decimal value created: {decimal_value.value}")

        # DateTime value
        start_date = datetime.now() - timedelta(days=2)
        datetime_value_data = CreateWorkItemPropertyValue(value=start_date.strftime("%Y-%m-%d"))
        datetime_value = client.work_item_properties.values.create(
            workspace_slug, project.id, main_work_item.id, datetime_prop.id, datetime_value_data
        )
        property_values["datetime"] = datetime_value
        print_success(f"DateTime value created: {datetime_value.value}")

        # Option value
        in_progress_option = next(opt for opt in status_options if opt.name == "In Progress")
        option_value_data = CreateWorkItemPropertyValue(value=in_progress_option.id)
        option_value = client.work_item_properties.values.create(
            workspace_slug, project.id, main_work_item.id, option_prop.id, option_value_data
        )
        property_values["option"] = option_value
        print_success(f"Option value created: {in_progress_option.name}")

        # Test retrieving property values
        print_step(8, "Testing property value retrieval")

        # Retrieve individual property values for the work item
        retrieved_text = client.work_item_properties.values.retrieve(
            workspace_slug, project.id, main_work_item.id, text_prop.id
        )
        print_success(f"Retrieved text value: {retrieved_text.value}")

        retrieved_bool = client.work_item_properties.values.retrieve(
            workspace_slug, project.id, main_work_item.id, bool_prop.id
        )
        print_success(f"Retrieved boolean value: {retrieved_bool.value}")

        retrieved_decimal = client.work_item_properties.values.retrieve(
            workspace_slug, project.id, main_work_item.id, decimal_prop.id
        )
        print_success(f"Retrieved decimal value: {retrieved_decimal.value}")

        retrieved_datetime = client.work_item_properties.values.retrieve(
            workspace_slug, project.id, main_work_item.id, datetime_prop.id
        )
        print_success(f"Retrieved datetime value: {retrieved_datetime.value}")

        retrieved_option = client.work_item_properties.values.retrieve(
            workspace_slug, project.id, main_work_item.id, option_prop.id
        )
        print_success(f"Retrieved option value: {retrieved_option.value}")

        # Test updating property values
        print_step(9, "Testing property value updates")

        # Update text value (using upsert behavior with create)
        updated_text_data = CreateWorkItemPropertyValue(
            value="This is an updated description after initial testing."
        )
        updated_text = client.work_item_properties.values.update(
            workspace_slug, project.id, main_work_item.id, text_prop.id, updated_text_data
        )
        print_success(f"Text value updated: {updated_text.value}")

        # Update boolean value using dict
        updated_bool = client.work_item_properties.values.update(
            workspace_slug, project.id, main_work_item.id, bool_prop.id, {"value": "true"}
        )
        print_success(f"Boolean value updated to: {updated_bool.value}")

        # Update decimal value
        updated_decimal_data = CreateWorkItemPropertyValue(value="75.25")
        updated_decimal = client.work_item_properties.values.update(
            workspace_slug, project.id, main_work_item.id, decimal_prop.id, updated_decimal_data
        )
        print_success(f"Decimal value updated to: {updated_decimal.value}")

        # Update option value to a different status
        completed_option = next(opt for opt in status_options if opt.name == "Completed")
        updated_option_data = CreateWorkItemPropertyValue(value=completed_option.id)
        updated_option = client.work_item_properties.values.update(
            workspace_slug, project.id, main_work_item.id, option_prop.id, updated_option_data
        )
        print_success(f"Option value updated to: {completed_option.name}")

        # Test creating property values for other work items
        print_step(10, "Testing property values for multiple work items")

        for i, work_item in enumerate(work_items[1:], 1):
            # Create different values for each work item
            text_value_data = CreateWorkItemPropertyValue(value=f"Description for task {i+1}")
            client.work_item_properties.values.create(
                workspace_slug, project.id, work_item.id, text_prop.id, text_value_data
            )

            bool_value_data = CreateWorkItemPropertyValue(
                value="true" if i % 2 == 0 else "false"  # Alternate true/false
            )
            client.work_item_properties.values.create(
                workspace_slug, project.id, work_item.id, bool_prop.id, bool_value_data
            )

            decimal_value_data = CreateWorkItemPropertyValue(
                value=str(float(i * 30))  # "30.0", "60.0"
            )
            client.work_item_properties.values.create(
                workspace_slug, project.id, work_item.id, decimal_prop.id, decimal_value_data
            )

            print_success(f"Property values created for work item {i+1}")

        # Test deleting property values
        print_step(11, "Testing property value deletion")

        # Delete the datetime value for the main work item
        client.work_item_properties.values.delete(
            workspace_slug, project.id, main_work_item.id, datetime_prop.id
        )
        print_success("DateTime value deleted successfully")

        # Verify deletion by trying to retrieve (should fail with 404)
        try:
            client.work_item_properties.values.retrieve(
                workspace_slug, project.id, main_work_item.id, datetime_prop.id
            )
            print_error("Expected 404 error after deletion, but value was still found")
        except Exception as e:
            if "404" in str(e):
                print_success("Verified: Value is deleted (404 error as expected)")
            else:
                print_error(f"Unexpected error during verification: {e}")

        # Final verification
        print_step(12, "Final verification")

        # Verify remaining values for the main work item
        remaining_values = []
        for prop_name, prop in properties.items():
            try:
                value = client.work_item_properties.values.retrieve(
                    workspace_slug, project.id, main_work_item.id, prop.id
                )
                remaining_values.append((prop_name, value.value))
                print(f"  {prop.display_name}: {value.value}")
            except Exception as e:
                if "404" in str(e):
                    print(f"  {prop.display_name}: (not set)")
                else:
                    print(f"  {prop.display_name}: error - {e}")

        print_success(f"Final property values verified: {len(remaining_values)} values found")

        # Summary
        print_step(13, "Test Summary")
        print(f"✓ Project created: {project.name}")
        print(f"✓ Work item type created: {task_type.name}")
        print(f"✓ Properties created: {len(properties)} different types")
        print(f"✓ Property options created: {len(status_options)}")
        print(f"✓ Work items created: {len(work_items)}")
        print("✓ Property values created: Text, Boolean, Decimal, DateTime, and Option types")
        print("✓ Property value retrieval tested")
        print("✓ Property value updates tested")
        print("✓ Property value deletion tested")
        print("\nAll property value CRUD operations completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        raise
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
