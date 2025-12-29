#!/usr/bin/env python3
"""
Standalone test script for testing Work Item Types, Custom Properties, and Property Values.
Tests creating work item types, custom properties, property options, and assigning values.

Usage:
    python test_work_item_types_and_properties.py

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
from plane.models.enums import PropertyType  # noqa: E402
from plane.models.projects import CreateProject  # noqa: E402
from plane.models.work_item_properties import (  # noqa: E402
    CreateWorkItemProperty,
    CreateWorkItemPropertyOption,
    CreateWorkItemPropertyValue,
)
from plane.models.work_item_property_configurations import (  # noqa: E402
    TextAttributeSettings,
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
            settings=TextAttributeSettings(display_format="single-line"),
        )
        severity_prop = client.work_item_properties.create(
            workspace_slug, project.id, bug_type.id, severity_prop_data
        )
        bug_properties.append(severity_prop)
        print_success(f"Property created: {severity_prop.display_name} (ID: {severity_prop.id})")

        # Option property - Priority (with inline options)
        priority_prop_data = CreateWorkItemProperty(
            display_name="Priority",
            description="Priority level for this bug",
            property_type=PropertyType.OPTION.value,
            is_required=True,
            is_active=True,
            options=[
                CreateWorkItemPropertyOption(
                    name="Critical",
                    description="Priority level: Critical",
                    is_active=True,
                    is_default=False,
                ),
                CreateWorkItemPropertyOption(
                    name="High",
                    description="Priority level: High",
                    is_active=True,
                    is_default=False,
                ),
                CreateWorkItemPropertyOption(
                    name="Medium",
                    description="Priority level: Medium",
                    is_active=True,
                    is_default=True,  # Set Medium as default
                ),
                CreateWorkItemPropertyOption(
                    name="Low",
                    description="Priority level: Low",
                    is_active=True,
                    is_default=False,
                ),
            ],
        )
        priority_prop = client.work_item_properties.create(
            workspace_slug, project.id, bug_type.id, priority_prop_data
        )
        bug_properties.append(priority_prop)
        print_success(f"Property created: {priority_prop.display_name} (ID: {priority_prop.id})")
        print(f"  Options created inline: {len(priority_prop.options)} options")

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

        # Get options from the Priority property (created inline)
        print_step(5, "Verifying inline options for Priority property")
        priority_options = priority_prop.options
        print_success(f"Priority property has {len(priority_options)} options (created inline)")
        for option in priority_options:
            print(f"  - {option.name} (ID: {option.id})")

        # Verify options are included in list and retrieve responses
        print_step(5.5, "Verifying options in list/retrieve responses")

        # Test list response includes options
        all_properties = client.work_item_properties.list(workspace_slug, project.id, bug_type.id)
        print_success(f"Listed {len(all_properties)} properties for Bug type")

        # Find the priority property in the list
        listed_priority_prop = next((p for p in all_properties if p.id == priority_prop.id), None)
        assert listed_priority_prop is not None, "Priority property should be in list"
        assert listed_priority_prop.options is not None, "Options should be in list response"
        assert len(listed_priority_prop.options) == 4, "Should have 4 options in list response"
        print_success("List response includes options ✓")
        for opt in listed_priority_prop.options:
            print(f"  - {opt.name}")

        # Test retrieve response includes options
        retrieved_priority_prop = client.work_item_properties.retrieve(
            workspace_slug, project.id, bug_type.id, priority_prop.id
        )
        assert retrieved_priority_prop.options is not None, "Options in retrieve response"
        assert len(retrieved_priority_prop.options) == 4, "Should have 4 options in retrieve"
        print_success("Retrieve response includes options ✓")

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
        severity_value_data = CreateWorkItemPropertyValue(value="High")
        severity_value = client.work_item_properties.values.create(
            workspace_slug, project.id, work_item.id, severity_prop.id, severity_value_data
        )
        print_success(f"Severity value set: {severity_value.value}")

        # Set Priority (option property) - use the High option
        high_option = next(opt for opt in priority_options if opt.name == "High")
        priority_value_data = CreateWorkItemPropertyValue(value=high_option.id)
        client.work_item_properties.values.create(
            workspace_slug, project.id, work_item.id, priority_prop.id, priority_value_data
        )
        print_success(f"Priority value set: {high_option.name}")

        # Set Is Critical (boolean property)
        critical_value_data = CreateWorkItemPropertyValue(value=True)
        critical_value = client.work_item_properties.values.create(
            workspace_slug, project.id, work_item.id, critical_prop.id, critical_value_data
        )
        print_success(f"Critical value set: {critical_value.value}")

        # Set Estimated Hours (decimal property)
        hours_value_data = CreateWorkItemPropertyValue(value=4.5)
        hours_value = client.work_item_properties.values.create(
            workspace_slug, project.id, work_item.id, hours_prop.id, hours_value_data
        )
        print_success(f"Estimated hours value set: {hours_value.value}")

        # Retrieve and verify the work item with its property values
        print_step(8, "Verifying work item and property values")
        retrieved_work_item = client.work_items.retrieve(workspace_slug, project.id, work_item.id)
        print_success(f"Work item retrieved: {retrieved_work_item.name}")

        # Retrieve individual property values to verify they were set correctly
        retrieved_severity = client.work_item_properties.values.retrieve(
            workspace_slug, project.id, work_item.id, severity_prop.id
        )
        print(f"  Severity: {retrieved_severity.value}")

        retrieved_priority = client.work_item_properties.values.retrieve(
            workspace_slug, project.id, work_item.id, priority_prop.id
        )
        print(f"  Priority: {retrieved_priority.value}")

        retrieved_critical = client.work_item_properties.values.retrieve(
            workspace_slug, project.id, work_item.id, critical_prop.id
        )
        print(f"  Is Critical: {retrieved_critical.value}")

        retrieved_hours = client.work_item_properties.values.retrieve(
            workspace_slug, project.id, work_item.id, hours_prop.id
        )
        print(f"  Estimated Hours: {retrieved_hours.value}")

        print_success("All property values retrieved successfully")

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

        # Cleanup: Delete created resources (optional)
        print_step(10, "Cleanup (optional)")
        choice = input("Delete test resources? (y/N): ").strip().lower()
        if choice == "y":
            # Delete work items
            for work_item in [work_item, feature_work_item]:
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
        print_step(11, "Test Summary")
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
