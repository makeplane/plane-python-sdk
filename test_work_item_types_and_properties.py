#!/usr/bin/env python3
"""
Standalone test script for testing Work Item Types, Custom Properties, and Property Values.
Tests creating work item types, custom properties, property options, and assigning values.

Usage:
    python test_work_item_types_and_properties.py

Requirements:
    - Set BASE_URL environment variable (e.g., https://api.plane.so)
    - Set either API_KEY or ACCESS_TOKEN environment variable
    - Set WORKSPACE_SLUG environment variable
"""

import os
import sys
from datetime import datetime

from plane.client import PlaneClient
from plane.models.enums import PropertyType
from plane.models.projects import CreateProject
from plane.models.work_item_properties import (
    CreateWorkItemProperty,
    CreateWorkItemPropertyOption,
    CreateWorkItemPropertyValue,
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

    print("Starting Work Item Types and Properties Test")
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
        project_identifier = f"TYPES{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Types & Properties Test {timestamp}",
            description="This project tests work item types and custom properties",
            identifier=project_identifier,
            emoji="🔧",
            is_issue_type_enabled=True,  # Enable work item types
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")
        print(f"  Identifier: {project.identifier}")
        print(f"  Emoji: {project.emoji}")
        print(f"  Work item types enabled: {project.is_issue_type_enabled}")

        # Ensure work item types are enabled (fallback)
        if not project.is_issue_type_enabled:
            print("  Enabling work item types on project...")
            from plane.models.projects import UpdateProject

            update_data = UpdateProject(is_issue_type_enabled=True)
            project = client.projects.update(workspace_slug, project.id, update_data)
            print_success("Work item types enabled on project")

        # Create work item types
        print_step(3, "Creating work item types")
        work_item_types = []

        # Create Bug type
        bug_type_data = CreateWorkItemType(
            name="Bug",
            description="Issues that represent bugs in the system",
            is_epic=False,
            is_active=True,
        )
        bug_type = client.work_item_types.create(workspace_slug, project.id, bug_type_data)
        work_item_types.append(bug_type)
        print_success(f"Work item type created: {bug_type.name} (ID: {bug_type.id})")

        # Create Feature type
        feature_type_data = CreateWorkItemType(
            name="Feature",
            description="New features or enhancements",
            is_epic=False,
            is_active=True,
        )
        feature_type = client.work_item_types.create(workspace_slug, project.id, feature_type_data)
        work_item_types.append(feature_type)
        print_success(f"Work item type created: {feature_type.name} (ID: {feature_type.id})")

        # Create Epic type
        epic_type_data = CreateWorkItemType(
            name="Epic",
            description="Large features that span multiple work items",
            is_epic=True,
            is_active=True,
        )
        epic_type = client.work_item_types.create(workspace_slug, project.id, epic_type_data)
        work_item_types.append(epic_type)
        print_success(f"Work item type created: {epic_type.name} (ID: {epic_type.id})")

        # Create custom properties for the Bug type
        print_step(4, "Creating custom properties for Bug type")
        bug_properties = []

        # Text property - Severity
        severity_prop_data = CreateWorkItemProperty(
            display_name="Severity",
            description="How severe is this bug?",
            property_type=PropertyType.TEXT.value,
            is_required=True,
            is_active=True,
        )
        severity_prop = client.work_item_properties.create(
            workspace_slug, project.id, bug_type.id, severity_prop_data
        )
        bug_properties.append(severity_prop)
        print_success(f"Property created: {severity_prop.display_name} (ID: {severity_prop.id})")

        # Option property - Priority
        priority_prop_data = CreateWorkItemProperty(
            display_name="Priority",
            description="Priority level for this bug",
            property_type=PropertyType.OPTION.value,
            is_required=True,
            is_active=True,
        )
        priority_prop = client.work_item_properties.create(
            workspace_slug, project.id, bug_type.id, priority_prop_data
        )
        bug_properties.append(priority_prop)
        print_success(f"Property created: {priority_prop.display_name} (ID: {priority_prop.id})")

        # Boolean property - Is Critical
        critical_prop_data = CreateWorkItemProperty(
            display_name="Is Critical",
            description="Is this a critical bug?",
            property_type=PropertyType.BOOLEAN.value,
            is_required=False,
            is_active=True,
        )
        critical_prop = client.work_item_properties.create(
            workspace_slug, project.id, bug_type.id, critical_prop_data
        )
        bug_properties.append(critical_prop)
        print_success(f"Property created: {critical_prop.display_name} (ID: {critical_prop.id})")

        # Decimal property - Estimated Hours
        hours_prop_data = CreateWorkItemProperty(
            display_name="Estimated Hours",
            description="Estimated time to fix in hours",
            property_type=PropertyType.DECIMAL.value,
            is_required=False,
            is_active=True,
        )
        hours_prop = client.work_item_properties.create(
            workspace_slug, project.id, bug_type.id, hours_prop_data
        )
        bug_properties.append(hours_prop)
        print_success(f"Property created: {hours_prop.display_name} (ID: {hours_prop.id})")

        # Create options for the Priority property
        print_step(5, "Creating property options for Priority")
        priority_options = []

        priority_levels = ["Critical", "High", "Medium", "Low"]
        for level in priority_levels:
            option_data = CreateWorkItemPropertyOption(
                name=level,
                description=f"Priority level: {level}",
                is_active=True,
                is_default=(level == "Medium"),  # Set Medium as default
            )
            option = client.work_item_properties.options.create(
                workspace_slug, project.id, priority_prop.id, option_data
            )
            priority_options.append(option)
            print_success(f"Option created: {option.name} (ID: {option.id})")

        # Create a work item with the Bug type
        print_step(6, "Creating a work item with Bug type and custom properties")
        work_item_data = CreateWorkItem(
            name="Test Bug with Custom Properties",
            description_html="<p>This is a test bug to demonstrate custom properties.</p>",
            priority="high",
            type_id=bug_type.id,  # Assign the Bug type
        )

        work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
        print_success(f"Work item created: {work_item.name} (ID: {work_item.id})")
        print(f"  Type: {bug_type.name}")
        print(f"  Priority: {work_item.priority}")

        # Assign custom property values to the work item
        print_step(7, "Assigning custom property values to work item")

        # Set Severity (text property)
        severity_value_data = CreateWorkItemPropertyValue(
            values=[CreateWorkItemPropertyValue.ValueItem(value="High")]
        )
        severity_value = client.work_item_properties.values.create(
            workspace_slug, project.id, work_item.id, severity_prop.id, severity_value_data
        )
        print_success(f"Severity value set: {severity_value.values[0].value}")

        # Set Priority (option property) - use the High option
        high_option = next(opt for opt in priority_options if opt.name == "High")
        priority_value_data = CreateWorkItemPropertyValue(
            values=[CreateWorkItemPropertyValue.ValueItem(value=high_option.id)]
        )
        client.work_item_properties.values.create(
            workspace_slug, project.id, work_item.id, priority_prop.id, priority_value_data
        )
        print_success(f"Priority value set: {high_option.name}")

        # Set Is Critical (boolean property)
        critical_value_data = CreateWorkItemPropertyValue(
            values=[CreateWorkItemPropertyValue.ValueItem(value=True)]
        )
        critical_value = client.work_item_properties.values.create(
            workspace_slug, project.id, work_item.id, critical_prop.id, critical_value_data
        )
        print_success(f"Critical value set: {critical_value.values[0].value}")

        # Set Estimated Hours (decimal property)
        hours_value_data = CreateWorkItemPropertyValue(
            values=[CreateWorkItemPropertyValue.ValueItem(value=4.5)]
        )
        hours_value = client.work_item_properties.values.create(
            workspace_slug, project.id, work_item.id, hours_prop.id, hours_value_data
        )
        print_success(f"Estimated hours value set: {hours_value.values[0].value}")

        # Retrieve and verify the work item with its property values
        print_step(8, "Verifying work item and property values")
        retrieved_work_item = client.work_items.retrieve(workspace_slug, project.id, work_item.id)
        print_success(f"Work item retrieved: {retrieved_work_item.name}")

        # Get all property values for the work item
        property_values = client.work_item_properties.values.list(
            workspace_slug, project.id, work_item.id
        )
        print_success(f"Retrieved {len(property_values)} property values")

        for prop_value in property_values:
            print(f"  Property {prop_value.property_id}: {prop_value.values}")

        # Test creating a work item with Feature type
        print_step(9, "Creating a work item with Feature type")
        feature_work_item_data = CreateWorkItem(
            name="Test Feature with Custom Properties",
            description_html=(
                "<p>This is a test feature to demonstrate different work item types.</p>"
            ),
            priority="medium",
            type_id=feature_type.id,  # Assign the Feature type
        )

        feature_work_item = client.work_items.create(
            workspace_slug, project.id, feature_work_item_data
        )
        print_success(
            f"Feature work item created: {feature_work_item.name} (ID: {feature_work_item.id})"
        )
        print(f"  Type: {feature_type.name}")

        # Summary
        print_step(10, "Test Summary")
        print(f"✓ Project created: {project.name}")
        print(f"✓ Work item types created: {len(work_item_types)}")
        print(f"✓ Custom properties created: {len(bug_properties)}")
        print(f"✓ Property options created: {len(priority_options)}")
        print("✓ Work items created: 2")
        print("✓ Property values assigned: 4")
        print("\nAll tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
