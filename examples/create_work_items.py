"""
Create Work Items Example - Plane Python SDK

This example demonstrates:
- Creating a basic project
- Creating initial states
- Creating multiple work items
- Assigning labels and priorities
"""

import os

from plane.client import PlaneClient
from plane.errors import HttpError
from plane.models.labels import CreateLabel
from plane.models.projects import CreateProject
from plane.models.states import CreateState
from plane.models.work_items import CreateWorkItem


def main():
    """Create a project and add work items."""
    # Initialize client
    client = PlaneClient(
        base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
        api_key=os.environ.get("PLANE_API_KEY"),
    )

    workspace_slug = os.environ.get("WORKSPACE_SLUG")

    print("=" * 60)
    print("Creating Project with Work Items")
    print("=" * 60)

    # ========================================================================
    # 1. Create Project
    # ========================================================================
    print("\n1. Creating project...")
    try:
        project = client.projects.create(
            workspace_slug=workspace_slug,
            data=CreateProject(
                name="Website Redesign",
                identifier="WEB",
                description="Company website redesign project",
            ),
        )
        print(f"✓ Created project: {project.name}")
    except HttpError as e:
        print(f"✗ Failed to create project: {e}")
        return

    # ========================================================================
    # 2. Create Basic States
    # ========================================================================
    print("\n2. Creating states...")
    states = {}

    state_configs = [
        {"name": "To Do", "group": "unstarted", "color": "#3b82f6"},
        {"name": "In Progress", "group": "started", "color": "#f59e0b"},
        {"name": "Done", "group": "completed", "color": "#16a34a"},
    ]

    for config in state_configs:
        try:
            state = client.states.create(
                workspace_slug=workspace_slug,
                project_id=project.id,
                data=CreateState(
                    name=config["name"], group=config["group"], color=config["color"]
                ),
            )
            states[config["name"]] = state
            print(f"✓ Created state: {state.name}")
        except HttpError as e:
            print(f"  Note: {e}")

    if not states:
        print("✗ No states created")
        return

    # ========================================================================
    # 3. Create Labels
    # ========================================================================
    print("\n3. Creating labels...")
    labels = {}

    label_configs = [
        {"name": "Bug", "color": "#ef4444"},
        {"name": "Enhancement", "color": "#8b5cf6"},
    ]

    for config in label_configs:
        try:
            label = client.labels.create(
                workspace_slug=workspace_slug,
                project_id=project.id,
                data=CreateLabel(name=config["name"], color=config["color"]),
            )
            labels[config["name"]] = label
            print(f"✓ Created label: {label.name}")
        except HttpError as e:
            print(f"  Note: {e}")

    # ========================================================================
    # 4. Create Work Items
    # ========================================================================
    print("\n4. Creating work items...")

    todo_state = states.get("To Do")
    bug_label = labels.get("Bug")
    enhancement_label = labels.get("Enhancement")

    work_items_data = [
        {
            "name": "Update homepage design",
            "description": "<p>Redesign the homepage with new branding</p>",
            "priority": "high",
            "labels": [enhancement_label.id] if enhancement_label else [],
        },
        {
            "name": "Fix mobile navigation menu",
            "description": "<p>Navigation menu not working on mobile devices</p>",
            "priority": "urgent",
            "labels": [bug_label.id] if bug_label else [],
        },
        {
            "name": "Add contact form",
            "description": "<p>Create new contact form on contact page</p>",
            "priority": "medium",
            "labels": [enhancement_label.id] if enhancement_label else [],
        },
        {
            "name": "Optimize images for web",
            "description": "<p>Compress and optimize all images</p>",
            "priority": "low",
            "labels": [],
        },
        {
            "name": "Update footer links",
            "description": "<p>Add new social media links to footer</p>",
            "priority": "low",
            "labels": [enhancement_label.id] if enhancement_label else [],
        },
    ]

    created_items = []

    for item_data in work_items_data:
        try:
            work_item = client.work_items.create(
                workspace_slug=workspace_slug,
                project_id=project.id,
                data=CreateWorkItem(
                    name=item_data["name"],
                    description_html=item_data["description"],
                    state_id=todo_state.id,
                    priority=item_data["priority"],
                    labels=item_data["labels"],
                ),
            )
            created_items.append(work_item)
            print(f"✓ Created: {work_item.name} (Priority: {work_item.priority})")
        except HttpError as e:
            print(f"✗ Failed to create work item: {e}")

    # ========================================================================
    # 5. List All Work Items
    # ========================================================================
    print("\n5. Listing all work items in project...")
    try:
        all_items = client.work_items.list(
            workspace_slug=workspace_slug, project_id=project.id
        )
        print(f"\n✓ Total work items: {all_items.total_count}")
        for item in all_items.results:
            print(f"  • {item.name} [{item.priority}]")
    except HttpError as e:
        print(f"✗ Failed to list work items: {e}")

    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "=" * 60)
    print("Project Setup Complete!")
    print("=" * 60)
    print(f"Project: {project.name} ({project.identifier})")
    print(f"  States: {len(states)}")
    print(f"  Labels: {len(labels)}")
    print(f"  Work Items Created: {len(created_items)}")
    print("=" * 60)


if __name__ == "__main__":
    main()

