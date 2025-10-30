#!/usr/bin/env python3
"""
Comprehensive test script for testing SDK functionality end-to-end.

This script demonstrates:
1. Creating a project with all features enabled
2. Creating multiple work item types
3. Creating multiple properties for work item types
4. Creating work items with different types
5. Adding property values to work items
6. Creating labels and assigning them to work items
7. Creating a module and adding work items
8. Creating work item relations (relates_to, blocking)
9. Creating work item links
10. Creating work item comments
11. Creating a project page
12. Creating a cycle and adding work items

Usage:
    python test_comprehensive.py

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
from plane.models.cycles import CreateCycle  # noqa: E402
from plane.models.enums import ModuleStatus, PropertyType, WorkItemRelationType  # noqa: E402
from plane.models.labels import CreateLabel  # noqa: E402
from plane.models.modules import CreateModule  # noqa: E402
from plane.models.pages import CreatePage  # noqa: E402
from plane.models.projects import CreateProject, UpdateProject  # noqa: E402
from plane.models.work_item_properties import (  # noqa: E402
    CreateWorkItemProperty,
    CreateWorkItemPropertyOption,
    CreateWorkItemPropertyValue,
)
from plane.models.work_item_property_configurations import (  # noqa: E402
    DateAttributeSettings,
    TextAttributeSettings,
)
from plane.models.work_item_types import CreateWorkItemType  # noqa: E402
from plane.models.work_items import (  # noqa: E402
    CreateWorkItem,
    CreateWorkItemComment,
    CreateWorkItemLink,
    CreateWorkItemRelation,
    UpdateWorkItem,
)


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

    print("Starting Comprehensive SDK Test")
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

        # Create a project
        print_step(3, "Creating a new project")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_identifier = f"CMP{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Comprehensive Test {timestamp}",
            description="Testing all SDK features end-to-end",
            identifier=project_identifier,
            emoji="🚀",
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")

        # Enable all features
        print_step(4, "Enabling all project features")
        update_data = UpdateProject(
            module_view=True,
            cycle_view=True,
            issue_views_view=True,
            page_view=True,
            intake_view=True,
            is_issue_type_enabled=True,
            guest_view_all_features=True,
        )
        project = client.projects.update(workspace_slug, project.id, update_data)
        print_success("All features enabled on project")
        print(f"  Module view: {project.module_view}")
        print(f"  Cycle view: {project.cycle_view}")
        print(f"  Issue views: {project.issue_views_view}")
        print(f"  Page view: {project.page_view}")
        print(f"  Intake view: {project.intake_view}")
        print(f"  Work item types enabled: {project.is_issue_type_enabled}")
        print(f"  Guest view all features: {project.guest_view_all_features}")

        # Create multiple work item types
        print_step(5, "Creating multiple work item types")
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
            {
                "key": "feature",
                "name": "Feature",
                "description": "A new feature to be implemented",
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

        # Create multiple properties for the work item types
        print_step(6, "Creating multiple properties for work item types")
        properties = {}

        # Properties to create for non-epic types
        property_definitions = [
            {
                "key": "description",
                "display_name": "Detailed Description",
                "description": "Full description of the work item",
                "type": PropertyType.TEXT.value,
                "settings": TextAttributeSettings(display_format="multi-line"),
            },
            {
                "key": "priority_score",
                "display_name": "Priority Score",
                "description": "Numerical priority score (0-100)",
                "type": PropertyType.DECIMAL.value,
                "settings": None,
            },
            {
                "key": "is_blocked",
                "display_name": "Is Blocked",
                "description": "Whether this item is blocked",
                "type": PropertyType.BOOLEAN.value,
                "settings": None,
            },
            {
                "key": "due_date",
                "display_name": "Due Date",
                "description": "When this item is due",
                "type": PropertyType.DATETIME.value,
                "settings": DateAttributeSettings(display_format="MMM dd, yyyy"),
            },
            {
                "key": "severity",
                "display_name": "Severity",
                "description": "Severity level (for bugs)",
                "type": PropertyType.OPTION.value,
                "settings": None,
            },
        ]

        # Create properties for Task, Bug, and Feature types
        for type_key in ["task", "bug", "feature"]:
            properties[type_key] = {}
            work_item_type = work_item_types[type_key]

            for prop_def in property_definitions:
                prop_data = CreateWorkItemProperty(
                    display_name=prop_def["display_name"],
                    description=prop_def["description"],
                    property_type=prop_def["type"],
                    is_required=False,
                    is_active=True,
                    settings=prop_def["settings"],
                )
                prop = client.work_item_properties.create(
                    workspace_slug, project.id, work_item_type.id, prop_data
                )
                properties[type_key][prop_def["key"]] = prop
                print_success(f"Created property '{prop.display_name}' for {work_item_type.name}")

        # Create options for the severity property (for Bug type)
        print_step(7, "Creating property options for Bug severity")
        severity_options = {}

        severity_levels = [
            ("critical", "Critical", "System is unusable"),
            ("high", "High", "Major functionality affected"),
            ("medium", "Medium", "Some functionality affected"),
            ("low", "Low", "Minor issue"),
        ]

        for key, name, description in severity_levels:
            option_data = CreateWorkItemPropertyOption(
                name=name,
                description=description,
                is_active=True,
            )
            option = client.work_item_properties.options.create(
                workspace_slug,
                project.id,
                properties["bug"]["severity"].id,
                option_data,
            )
            severity_options[key] = option
            print_success(f"Created severity option: {option.name}")

        # Create work items with different types
        print_step(8, "Creating work items with different types")
        work_items = {}

        # Create 2 tasks
        work_items["tasks"] = []
        for i in range(2):
            work_item_data = CreateWorkItem(
                name=f"Task: Implement feature component {i+1}",
                description_html=f"<p>This is task {i+1} for implementing a component.</p>",
                priority="medium",
                type_id=work_item_types["task"].id,
            )
            work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
            work_items["tasks"].append(work_item)
            print_success(f"Created task: {work_item.name} (ID: {work_item.id})")

        # Create 2 bugs
        work_items["bugs"] = []
        for i in range(2):
            work_item_data = CreateWorkItem(
                name=f"Bug: Fix issue in {['login', 'dashboard'][i]} module",
                description_html=f"<p>This is bug {i+1} that needs to be fixed.</p>",
                priority=["high", "medium"][i],
                type_id=work_item_types["bug"].id,
            )
            work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
            work_items["bugs"].append(work_item)
            print_success(f"Created bug: {work_item.name} (ID: {work_item.id})")

        # Create 1 feature
        work_items["features"] = []
        work_item_data = CreateWorkItem(
            name="Feature: Add user profile management",
            description_html="<p>Implement comprehensive user profile management.</p>",
            priority="high",
            type_id=work_item_types["feature"].id,
        )
        work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
        work_items["features"].append(work_item)
        print_success(f"Created feature: {work_item.name} (ID: {work_item.id})")

        # Add property values to work items
        print_step(9, "Adding property values to work items")

        # Add property values to first task
        task_1 = work_items["tasks"][0]
        task_props = properties["task"]

        # Description
        desc_value = CreateWorkItemPropertyValue(
            value=(
                "This task involves implementing the main feature component "
                "with all required functionality."
            )
        )
        client.work_item_properties.values.create(
            workspace_slug, project.id, task_1.id, task_props["description"].id, desc_value
        )
        print_success(f"Added description to task: {task_1.name}")

        # Priority score
        priority_value = CreateWorkItemPropertyValue(value=75.5)
        client.work_item_properties.values.create(
            workspace_slug, project.id, task_1.id, task_props["priority_score"].id, priority_value
        )
        print_success(f"Added priority score to task: {task_1.name}")

        # Is blocked
        blocked_value = CreateWorkItemPropertyValue(value=False)
        client.work_item_properties.values.create(
            workspace_slug, project.id, task_1.id, task_props["is_blocked"].id, blocked_value
        )
        print_success(f"Added blocked status to task: {task_1.name}")

        # Due date
        due_date = datetime.now() + timedelta(days=7)
        due_date_value = CreateWorkItemPropertyValue(value=due_date.strftime("%Y-%m-%d"))
        client.work_item_properties.values.create(
            workspace_slug, project.id, task_1.id, task_props["due_date"].id, due_date_value
        )
        print_success(f"Added due date to task: {task_1.name}")

        # Add property values to first bug
        bug_1 = work_items["bugs"][0]
        bug_props = properties["bug"]

        # Description
        bug_desc_value = CreateWorkItemPropertyValue(
            value="Critical bug in the login flow that prevents users from authenticating."
        )
        client.work_item_properties.values.create(
            workspace_slug, project.id, bug_1.id, bug_props["description"].id, bug_desc_value
        )
        print_success(f"Added description to bug: {bug_1.name}")

        # Priority score
        bug_priority_value = CreateWorkItemPropertyValue(value=95.0)
        client.work_item_properties.values.create(
            workspace_slug,
            project.id,
            bug_1.id,
            bug_props["priority_score"].id,
            bug_priority_value,
        )
        print_success(f"Added priority score to bug: {bug_1.name}")

        # Is blocked
        bug_blocked_value = CreateWorkItemPropertyValue(value=False)
        client.work_item_properties.values.create(
            workspace_slug, project.id, bug_1.id, bug_props["is_blocked"].id, bug_blocked_value
        )
        print_success(f"Added blocked status to bug: {bug_1.name}")

        # Severity
        severity_value = CreateWorkItemPropertyValue(value=severity_options["critical"].id)
        client.work_item_properties.values.create(
            workspace_slug, project.id, bug_1.id, bug_props["severity"].id, severity_value
        )
        print_success(f"Added severity (Critical) to bug: {bug_1.name}")

        # Add property values to feature
        feature_1 = work_items["features"][0]
        feature_props = properties["feature"]

        # Description
        feature_desc_value = CreateWorkItemPropertyValue(
            value="Implement user profile management with avatar upload, bio, and settings."
        )
        client.work_item_properties.values.create(
            workspace_slug,
            project.id,
            feature_1.id,
            feature_props["description"].id,
            feature_desc_value,
        )
        print_success(f"Added description to feature: {feature_1.name}")

        # Priority score
        feature_priority_value = CreateWorkItemPropertyValue(value=85.0)
        client.work_item_properties.values.create(
            workspace_slug,
            project.id,
            feature_1.id,
            feature_props["priority_score"].id,
            feature_priority_value,
        )
        print_success(f"Added priority score to feature: {feature_1.name}")

        # Due date
        feature_due_date = datetime.now() + timedelta(days=14)
        feature_due_date_value = CreateWorkItemPropertyValue(
            value=feature_due_date.strftime("%Y-%m-%d")
        )
        client.work_item_properties.values.create(
            workspace_slug,
            project.id,
            feature_1.id,
            feature_props["due_date"].id,
            feature_due_date_value,
        )
        print_success(f"Added due date to feature: {feature_1.name}")

        # Create a cycle
        print_step(10, "Creating a cycle")
        cycle_start = datetime.now()
        cycle_end = cycle_start + timedelta(days=14)

        cycle_data = CreateCycle(
            name="Sprint 1 - MVP Development",
            description="First sprint focused on building the MVP features",
            start_date=cycle_start.strftime("%Y-%m-%d"),
            end_date=cycle_end.strftime("%Y-%m-%d"),
            owned_by=current_user.id,
            project_id=project.id,
        )

        cycle = client.cycles.create(workspace_slug, project.id, cycle_data)
        print_success(f"Cycle created: {cycle.name} (ID: {cycle.id})")
        print(f"  Start date: {cycle.start_date}")
        print(f"  End date: {cycle.end_date}")
        print(f"  Owner: {current_user.display_name}")

        # Add work items to cycle
        print_step(11, "Adding work items to cycle")

        # Collect all work item IDs
        work_item_ids = []
        for task in work_items["tasks"]:
            work_item_ids.append(task.id)
        for bug in work_items["bugs"]:
            work_item_ids.append(bug.id)
        for feature in work_items["features"]:
            work_item_ids.append(feature.id)

        client.cycles.add_work_items(workspace_slug, project.id, cycle.id, work_item_ids)
        print_success(f"Added {len(work_item_ids)} work items to cycle")

        # List work items in cycle
        cycle_work_items = client.cycles.list_work_items(workspace_slug, project.id, cycle.id)
        print_success(f"Verified: Cycle now contains {cycle_work_items.count} work items")

        # Create labels
        print_step(12, "Creating labels and assigning to work items")
        labels = []
        label_configs = [
            {"name": "Frontend", "color": "#FF6B6B", "description": "Frontend related"},
            {"name": "Backend", "color": "#4ECDC4", "description": "Backend related"},
            {"name": "Critical", "color": "#FF0000", "description": "Critical priority"},
        ]

        for label_config in label_configs:
            label_data = CreateLabel(**label_config)
            label = client.labels.create(workspace_slug, project.id, label_data)
            labels.append(label)
            print_success(f"Created label: {label.name} (ID: {label.id})")

        # Assign labels to work items
        label_ids = [label.id for label in labels]
        for work_item_type_key, work_item_list in work_items.items():
            if work_item_list:
                update_data = UpdateWorkItem(labels=label_ids[:2])  # Assign first 2 labels
                client.work_items.update(
                    workspace_slug, project.id, work_item_list[0].id, update_data
                )
                print_success(f"Assigned labels to {work_item_type_key}")

        # Create a module
        print_step(13, "Creating a module and adding work items")
        module_start = datetime.now()
        module_end = module_start + timedelta(days=21)

        module_data = CreateModule(
            name="MVP Development Module",
            description="Module for comprehensive SDK testing",
            start_date=module_start.strftime("%Y-%m-%d"),
            target_date=module_end.strftime("%Y-%m-%d"),
            status=ModuleStatus.IN_PROGRESS.value,
            lead=current_user.id,
            members=[current_user.id],
        )

        module = client.modules.create(workspace_slug, project.id, module_data)
        print_success(f"Created module: {module.name} (ID: {module.id})")

        # Add work items to module (add all tasks and the first bug)
        module_work_item_ids = [work_items["tasks"][0].id]
        if work_items["bugs"]:
            module_work_item_ids.append(work_items["bugs"][0].id)
        client.modules.add_work_items(workspace_slug, project.id, module.id, module_work_item_ids)
        print_success(f"Added {len(module_work_item_ids)} work items to module")

        # Create work item relations
        print_step(14, "Creating work item relations")
        primary_work_item = work_items["tasks"][0]
        related_work_item = work_items["bugs"][0] if work_items["bugs"] else work_items["tasks"][1]

        # Create relates_to relation
        relation_data = CreateWorkItemRelation(
            relation_type=WorkItemRelationType.RELATES_TO.value,
            issues=[related_work_item.id],
        )
        client.work_items.relations.create(
            workspace_slug, project.id, primary_work_item.id, relation_data
        )
        print_success("Created 'relates_to' relation between work items")

        # Create blocking relation if we have enough work items
        if len(work_items["tasks"]) > 1:
            blocking_data = CreateWorkItemRelation(
                relation_type=WorkItemRelationType.BLOCKING.value,
                issues=[work_items["tasks"][1].id],
            )
            client.work_items.relations.create(
                workspace_slug, project.id, primary_work_item.id, blocking_data
            )
            print_success("Created 'blocking' relation")

        # Create work item links
        print_step(15, "Creating work item links")
        link_data = CreateWorkItemLink(url="https://github.com/makeplane/plane")
        created_link = client.work_items.links.create(
            workspace_slug, project.id, primary_work_item.id, link_data
        )
        print_success(f"Created link: {created_link.url}")

        # Create work item comments
        print_step(16, "Creating work item comments")
        comment_data = CreateWorkItemComment(
            comment_html="<p>This is a comprehensive test comment.</p>"
        )
        created_comment = client.work_items.comments.create(
            workspace_slug, project.id, primary_work_item.id, comment_data
        )
        print_success(f"Created comment: {created_comment.id}")

        # Create second comment
        comment_data_2 = CreateWorkItemComment(
            comment_html="<p>Another comment for testing purposes.</p>"
        )
        created_comment_2 = client.work_items.comments.create(
            workspace_slug, project.id, primary_work_item.id, comment_data_2
        )
        print_success(f"Created second comment: {created_comment_2.id}")

        # Create a project page
        print_step(17, "Creating a project page")
        page_data = CreatePage(
            name=f"Test Project Page - {timestamp}",
            description_html="<p>Comprehensive test project page.</p>",
            color="#4ECDC4",
        )
        project_page = client.pages.create_project_page(workspace_slug, project.id, page_data)
        print_success(f"Created project page: {project_page.name} (ID: {project_page.id})")

        # Cleanup: Delete created resources (optional)
        print_step(18, "Cleanup (optional)")
        choice = input("Delete test resources? (y/N): ").strip().lower()
        if choice == "y":
            # Delete comments
            try:
                client.work_items.comments.delete(
                    workspace_slug, project.id, primary_work_item.id, created_comment.id
                )
                print_success("Deleted test comment")
            except Exception as e:
                print_error(f"Failed to delete comment: {e}")

            try:
                client.work_items.comments.delete(
                    workspace_slug, project.id, primary_work_item.id, created_comment_2.id
                )
                print_success("Deleted second test comment")
            except Exception as e:
                print_error(f"Failed to delete second comment: {e}")

            # Delete link
            try:
                client.work_items.links.delete(
                    workspace_slug, project.id, primary_work_item.id, created_link.id
                )
                print_success("Deleted test link")
            except Exception as e:
                print_error(f"Failed to delete link: {e}")

            # Delete module
            try:
                client.modules.delete(workspace_slug, project.id, module.id)
                print_success(f"Deleted module: {module.name}")
            except Exception as e:
                print_error(f"Failed to delete module {module.id}: {e}")

            # Delete cycle
            try:
                client.cycles.delete(workspace_slug, project.id, cycle.id)
                print_success(f"Deleted cycle: {cycle.name}")
            except Exception as e:
                print_error(f"Failed to delete cycle {cycle.id}: {e}")

            # Delete labels
            for label in labels:
                try:
                    client.labels.delete(workspace_slug, project.id, label.id)
                    print_success(f"Deleted label: {label.name}")
                except Exception as e:
                    print_error(f"Failed to delete label {label.name}: {e}")

            # Delete all work items
            all_work_items = []
            for item_list in work_items.values():
                all_work_items.extend(item_list)
            for work_item in all_work_items:
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
        print(f"✓ Project created: {project.name}")
        print("✓ All features enabled on project")
        print(f"✓ Work item types created: {len(work_item_types)} types")
        for key, wit in work_item_types.items():
            type_prop_count = len(properties.get(key, {}))
            print(f"    - {wit.name}: {type_prop_count} properties")
        print(f"✓ Total work items created: {sum(len(v) for v in work_items.values())}")
        print(f"    - Tasks: {len(work_items['tasks'])}")
        print(f"    - Bugs: {len(work_items['bugs'])}")
        print(f"    - Features: {len(work_items['features'])}")
        print("✓ Property values added to multiple work items")
        print(f"✓ Labels created: {len(labels)}")
        print("✓ Labels assigned to work items")
        print(f"✓ Module created: {module.name}")
        print(f"✓ Work items added to module: {len(module_work_item_ids)}")
        print("✓ Work item relations created (relates_to, blocking)")
        print(f"✓ Work item link created: {created_link.url}")
        print("✓ Work item comments created: 2")
        print(f"✓ Project page created: {project_page.name}")
        print(f"✓ Cycle created: {cycle.name}")
        print(f"✓ Work items added to cycle: {len(work_item_ids)}")
        print("\nAll comprehensive tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
