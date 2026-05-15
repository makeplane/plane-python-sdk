"""Test script for verifying Project and WorkItem archive methods."""
import os
import sys
import time
from datetime import datetime
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from plane.client import PlaneClient
from plane.models.projects import CreateProject
from plane.models.work_items import CreateWorkItem


def print_step(step: int, message: str) -> None:
    """Print a step message."""
    print(f"\n[{step}] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"  ✅ {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"  ❌ {message}")


def main() -> None:
    """Main test function."""
    base_url = os.getenv("PLANE_BASE_URL")
    api_key = os.getenv("PLANE_API_KEY")
    access_token = os.getenv("PLANE_ACCESS_TOKEN")
    workspace_slug = os.getenv("WORKSPACE_SLUG", "random")

    print("Starting Comprehensive Archive SDK Test")
    print(f"Base URL: {base_url}")
    print(f"Workspace: {workspace_slug}")

    try:
        print_step(1, "Initializing Plane Client")
        client = PlaneClient(
            base_url=base_url,
            api_key=api_key,
            access_token=access_token,
        )
        print_success("Client initialized successfully")

        # Create a test project
        print_step(2, "Creating a test project")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_identifier = f"ARC{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Archive Test {timestamp}",
            description="Testing project and work item archiving",
            identifier=project_identifier,
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")

        # Find a completed state
        states = client.states.list(workspace_slug, project.id)
        completed_state = next((s for s in states.results if s.group == "completed"), None)
        if not completed_state:
            print_error("Could not find a completed state in the project")
            sys.exit(1)

        # Create a test work item in a completed state
        print_step(3, "Creating a test work item in completed state")
        wi_data = CreateWorkItem(
            name="Test Work Item for Archiving",
            priority="medium",
            state=completed_state.id,
        )
        work_item = client.work_items.create(workspace_slug, project.id, wi_data)
        print_success(f"Work Item created: {work_item.name} (ID: {work_item.id})")

        # Archive work item
        print_step(4, "Archiving the work item")
        client.work_items.archive(workspace_slug, project.id, work_item.id)
        print_success("Work Item successfully archived.")

        # Unarchive work item
        print_step(5, "Unarchiving the work item")
        client.work_items.unarchive(workspace_slug, project.id, work_item.id)
        print_success("Work Item successfully unarchived.")

        # Archive project
        print_step(6, "Archiving the project")
        client.projects.archive(workspace_slug, project.id)
        print_success("Project successfully archived.")

        # Unarchive project
        print_step(7, "Unarchiving the project")
        client.projects.unarchive(workspace_slug, project.id)
        print_success("Project successfully unarchived.")

        # Delete work item
        print_step(8, "Cleaning up Work Item")
        client.work_items.delete(workspace_slug, project.id, work_item.id)
        print_success("Work Item deleted.")

        # Delete project
        print_step(9, "Cleaning up Project")
        client.projects.delete(workspace_slug, project.id)
        print_success("Project deleted.")

        print("\n🎉 All Archive API methods tested successfully!")

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
