"""
Project Setup Example - Plane Python SDK

This example demonstrates setting up a complete project with:
- Creating a project
- Creating work item types
- Creating workflow states
- Creating labels
"""

import os

from plane.client import PlaneClient
from plane.errors import HttpError
from plane.models.labels import CreateLabel
from plane.models.projects import CreateProject
from plane.models.states import CreateState
from plane.models.work_item_types import CreateWorkItemType


def main():
    """Set up a project with work item types, states, and labels."""
    # Initialize client
    client = PlaneClient(
        base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
        api_key=os.environ.get("PLANE_API_KEY"),
    )

    workspace_slug = os.environ.get("WORKSPACE_SLUG")

    print("=" * 60)
    print("Setting Up Project")
    print("=" * 60)

    # ========================================================================
    # 1. Create Project
    # ========================================================================
    print("\n1. Creating project...")
    try:
        project = client.projects.create(
            workspace_slug=workspace_slug,
            data=CreateProject(
                name="Product Development",
                identifier="PROD",
                description="Main product development project",
            ),
        )
        print(f"✓ Created project: {project.name} ({project.identifier})")
    except HttpError as e:
        print(f"✗ Failed to create project: {e}")
        return

    # ========================================================================
    # 2. Create Work Item Types
    # ========================================================================
    print("\n2. Creating work item types...")
    work_item_types = []

    type_configs = [
        {"name": "Bug", "description": "Something that needs fixing"},
        {"name": "Feature", "description": "New functionality"},
        {"name": "Task", "description": "General task"},
        {"name": "Story", "description": "User story"},
    ]

    for config in type_configs:
        try:
            wit = client.work_item_types.create(
                workspace_slug=workspace_slug,
                project_id=project.id,
                data=CreateWorkItemType(
                    name=config["name"], description=config["description"]
                ),
            )
            work_item_types.append(wit)
            print(f"✓ Created work item type: {wit.name}")
        except HttpError as e:
            print(f"  Note: {e}")

    # ========================================================================
    # 3. Create Workflow States
    # ========================================================================
    print("\n3. Creating workflow states...")
    states = []

    state_configs = [
        {"name": "Backlog", "group": "backlog", "color": "#a8a29e"},
        {"name": "To Do", "group": "unstarted", "color": "#3b82f6"},
        {"name": "In Progress", "group": "started", "color": "#f59e0b"},
        {"name": "In Review", "group": "started", "color": "#8b5cf6"},
        {"name": "Done", "group": "completed", "color": "#16a34a"},
        {"name": "Cancelled", "group": "cancelled", "color": "#ef4444"},
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
            states.append(state)
            print(f"✓ Created state: {state.name} ({state.group})")
        except HttpError as e:
            print(f"  Note: {e}")

    # ========================================================================
    # 4. Create Labels
    # ========================================================================
    print("\n4. Creating labels...")
    labels = []

    label_configs = [
        {"name": "High Priority", "color": "#ef4444"},
        {"name": "Low Priority", "color": "#22c55e"},
        {"name": "Frontend", "color": "#3b82f6"},
        {"name": "Backend", "color": "#f59e0b"},
        {"name": "Database", "color": "#8b5cf6"},
        {"name": "Documentation", "color": "#06b6d4"},
        {"name": "Testing", "color": "#ec4899"},
    ]

    for config in label_configs:
        try:
            label = client.labels.create(
                workspace_slug=workspace_slug,
                project_id=project.id,
                data=CreateLabel(name=config["name"], color=config["color"]),
            )
            labels.append(label)
            print(f"✓ Created label: {label.name}")
        except HttpError as e:
            print(f"  Note: {e}")

    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "=" * 60)
    print("Project Setup Complete!")
    print("=" * 60)
    print(f"Project: {project.name} ({project.identifier})")
    print(f"  ID: {project.id}")
    print(f"  Work Item Types: {len(work_item_types)}")
    print(f"  States: {len(states)}")
    print(f"  Labels: {len(labels)}")
    print("=" * 60)


if __name__ == "__main__":
    main()

