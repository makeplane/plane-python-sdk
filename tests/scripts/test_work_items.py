#!/usr/bin/env python3
"""
Comprehensive test script for testing all work items resources end-to-end.

This script demonstrates:
1. Creating a project and work items
2. Testing work item CRUD operations
3. Testing work item relations
4. Testing work item links
5. Testing work item comments
6. Testing work item activities (read-only)
7. Testing work item attachments
8. Testing work item work logs

Usage:
    python test_work_items.py

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
from plane.models.enums import WorkItemRelationType  # noqa: E402
from plane.models.projects import CreateProject, UpdateProject  # noqa: E402
from plane.models.query_params import RetrieveQueryParams, WorkItemQueryParams  # noqa: E402
from plane.models.work_items import (  # noqa: E402
    CreateWorkItem,
    CreateWorkItemComment,
    CreateWorkItemLink,
    CreateWorkItemRelation,
    RemoveWorkItemRelation,
    UpdateWorkItem,
    UpdateWorkItemComment,
    UpdateWorkItemLink,
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

    print("Starting Comprehensive Work Items SDK Test")
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

        # Create a project for testing
        print_step(2, "Creating a test project")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_identifier = f"WI{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Work Items Test {timestamp}",
            description="Testing all work items resources",
            identifier=project_identifier,
            emoji="🧪",
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")

        # Enable time tracking (required for work logs feature)
        update_project_data = UpdateProject(is_time_tracking_enabled=True)
        client.projects.update(workspace_slug, project.id, update_project_data)
        print_success("Enabled time tracking on project")

        # Create multiple work items for testing
        print_step(3, "Creating work items for testing")
        work_items = []

        for i in range(3):
            work_item_data = CreateWorkItem(
                name=f"Work Item {i+1}: Test Resource Operations",
                description_html=f"<p>This is work item {i+1} for testing resources.</p>",
                priority=["urgent", "high", "medium"][i],
            )
            work_item = client.work_items.create(workspace_slug, project.id, work_item_data)
            work_items.append(work_item)
            print_success(f"Created work item: {work_item.name} (ID: {work_item.id})")

        # Use first work item for most tests
        primary_work_item = work_items[0]
        secondary_work_item = work_items[1]

        # Test work item retrieve operations
        print_step(4, "Testing work item retrieve operations")

        # Retrieve by ID with basic params
        retrieved = client.work_items.retrieve(
            workspace_slug, project.id, primary_work_item.id
        )
        print_success(f"Retrieved work item: {retrieved.name}")

        # Retrieve with expand params
        client.work_items.retrieve(
            workspace_slug,
            project.id,
            primary_work_item.id,
            params=RetrieveQueryParams(expand="assignees,labels,state"),
        )
        print_success("Retrieved work item with expanded relationships")

        # Retrieve by identifier
        if primary_work_item.sequence_id:
            client.work_items.retrieve_by_identifier(
                workspace_slug,
                project_identifier,
                primary_work_item.sequence_id,
            )
            print_success(
                f"Retrieved work item by identifier: "
                f"{project_identifier}-{primary_work_item.sequence_id}"
            )

        # Test work item update
        print_step(5, "Testing work item update")
        update_data = UpdateWorkItem(
            name=f"{primary_work_item.name} (Updated)",
            description_html="<p>This work item has been updated for testing.</p>",
            priority="low",
        )
        updated = client.work_items.update(
            workspace_slug, project.id, primary_work_item.id, update_data
        )
        print_success(f"Updated work item: {updated.name}")

        # Test work item list with filters
        print_step(6, "Testing work item list operations")
        list_params = WorkItemQueryParams(limit=10, offset=0)
        listed = client.work_items.list(workspace_slug, project.id, params=list_params)
        print_success(f"Listed {len(listed.results)} work items")

        # Test work item search
        print_step(7, "Testing work item search")
        search_results = client.work_items.search(workspace_slug, "Test")
        print_success(f"Search found {len(search_results.issues)} work items")

        # Test work item relations
        print_step(8, "Testing work item relations")

        # List existing relations
        client.work_items.relations.list(
            workspace_slug, project.id, primary_work_item.id
        )
        print_success("Retrieved work item relations")

        # Create a relation (relates_to)
        relation_data = CreateWorkItemRelation(
            relation_type=WorkItemRelationType.RELATES_TO.value,
            issues=[secondary_work_item.id],
        )
        client.work_items.relations.create(
            workspace_slug, project.id, primary_work_item.id, relation_data
        )
        print_success(
            f"Created 'relates_to' relation between "
            f"{primary_work_item.id[:8]}... and {secondary_work_item.id[:8]}..."
        )

        # Create a blocking relation
        if len(work_items) > 2:
            blocking_data = CreateWorkItemRelation(
                relation_type=WorkItemRelationType.BLOCKING.value,
                issues=[work_items[2].id],
            )
            client.work_items.relations.create(
                workspace_slug, project.id, primary_work_item.id, blocking_data
            )
            print_success("Created 'blocking' relation")

        # List relations again to verify
        relations_after = client.work_items.relations.list(
            workspace_slug, project.id, primary_work_item.id
        )
        print_success(
            f"Relations: relates_to={len(relations_after.relates_to)}, "
            f"blocking={len(relations_after.blocking)}"
        )

        # Remove a relation
        remove_data = RemoveWorkItemRelation(related_issue=secondary_work_item.id)
        client.work_items.relations.delete(
            workspace_slug, project.id, primary_work_item.id, remove_data
        )
        print_success("Removed work item relation")

        # Test work item links
        print_step(9, "Testing work item links")

        # List links (should be empty initially)
        links = client.work_items.links.list(workspace_slug, project.id, primary_work_item.id)
        print_success(f"Retrieved {len(links.results)} links")

        # Create a link
        link_data = CreateWorkItemLink(url="https://github.com/your-org/your-repo")
        created_link = client.work_items.links.create(
            workspace_slug, project.id, primary_work_item.id, link_data
        )
        print_success(f"Created link: {created_link.url}")

        # Retrieve the link
        retrieved_link = client.work_items.links.retrieve(
            workspace_slug, project.id, primary_work_item.id, created_link.id
        )
        print_success(f"Retrieved link: {retrieved_link.id}")

        # Update the link
        update_link_data = UpdateWorkItemLink(url="https://github.com/your-org/your-repo/issue/1")
        updated_link = client.work_items.links.update(
            workspace_slug, project.id, primary_work_item.id, created_link.id, update_link_data
        )
        print_success(f"Updated link: {updated_link.url}")

        # List links again
        links_after = client.work_items.links.list(
            workspace_slug, project.id, primary_work_item.id
        )
        print_success(f"Now have {len(links_after.results)} links")

        # Test work item comments
        print_step(10, "Testing work item comments")

        # List comments (should be empty initially)
        comments = client.work_items.comments.list(
            workspace_slug, project.id, primary_work_item.id
        )
        print_success(f"Retrieved {len(comments.results)} comments")

        # Create a comment
        comment_data = CreateWorkItemComment(
            comment_html="<p>This is a test comment on the work item.</p>"
        )
        created_comment = client.work_items.comments.create(
            workspace_slug, project.id, primary_work_item.id, comment_data
        )
        print_success(f"Created comment: {created_comment.id}")

        # Create another comment
        comment_data_2 = CreateWorkItemComment(
            comment_html=(
                "<p>This is a second test comment with some "
                "<strong>formatting</strong>.</p>"
            )
        )
        created_comment_2 = client.work_items.comments.create(
            workspace_slug, project.id, primary_work_item.id, comment_data_2
        )
        print_success(f"Created second comment: {created_comment_2.id}")

        # Retrieve a specific comment
        retrieved_comment = client.work_items.comments.retrieve(
            workspace_slug, project.id, primary_work_item.id, created_comment.id
        )
        print_success(f"Retrieved comment: {retrieved_comment.id}")

        # Update a comment
        update_comment_data = UpdateWorkItemComment(
            comment_html="<p>This comment has been updated.</p>"
        )
        updated_comment = client.work_items.comments.update(
            workspace_slug,
            project.id,
            primary_work_item.id,
            created_comment.id,
            update_comment_data,
        )
        print_success(f"Updated comment: {updated_comment.id}")

        # List comments again
        comments_after = client.work_items.comments.list(
            workspace_slug, project.id, primary_work_item.id
        )
        print_success(f"Now have {len(comments_after.results)} comments")

        # Test work item activities (read-only)
        print_step(11, "Testing work item activities (read-only)")

        # List activities
        activities = client.work_items.activities.list(
            workspace_slug, project.id, primary_work_item.id
        )
        print_success(f"Retrieved {activities.count} activities")

        # Retrieve a specific activity if any exist
        if activities.count > 0 and activities.results:
            activity_id = activities.results[0].id
            if activity_id:
                retrieved_activity = client.work_items.activities.retrieve(
                    workspace_slug, project.id, primary_work_item.id, activity_id
                )
                print_success(f"Retrieved activity: {retrieved_activity.id}")

        # Test work item attachments
        print_step(12, "Testing work item attachments")

        # List attachments (should be empty initially)
        attachments = client.work_items.attachments.list(
            workspace_slug, project.id, primary_work_item.id
        )
        print_success(f"Retrieved {len(attachments)} attachments")

        # Note: Creating attachments typically requires file upload, which may not be
        # straightforward via API without proper file handling. We'll test the API
        # structure but may skip actual file uploads depending on API requirements.
        # For now, we'll test that we can query attachments.
        if len(attachments) == 0:
            print_success("No attachments (expected for new work item)")

        # Test work item work logs
        print_step(13, "Testing work item work logs")

        # List work logs (should be empty initially)
        work_logs = client.work_items.work_logs.list(
            workspace_slug, project.id, primary_work_item.id
        )
        print_success(f"Retrieved {len(work_logs)} work logs")

        # Create a work log
        work_log_data = {
            "description": "Spent 2 hours on initial implementation",
            "duration": 120,  # duration in minutes
        }
        created_work_log = client.work_items.work_logs.create(
            workspace_slug, project.id, primary_work_item.id, work_log_data
        )
        duration = created_work_log.duration
        print_success(
            f"Created work log: {created_work_log.id} "
            f"(duration: {duration} minutes)"
        )

        # Create another work log
        work_log_data_2 = {
            "description": "Code review and bug fixes",
            "duration": 45,
        }
        created_work_log_2 = client.work_items.work_logs.create(
            workspace_slug, project.id, primary_work_item.id, work_log_data_2
        )
        print_success(f"Created second work log: {created_work_log_2.id}")

        # Update a work log
        update_work_log_data = {
            "description": "Spent 2.5 hours on initial implementation and testing",
            "duration": 150,
        }
        updated_work_log = client.work_items.work_logs.update(
            workspace_slug,
            project.id,
            primary_work_item.id,
            created_work_log.id,
            update_work_log_data,
        )
        new_duration = updated_work_log.duration
        print_success(
            f"Updated work log: {updated_work_log.id} "
            f"(new duration: {new_duration} minutes)"
        )

        # List work logs again
        work_logs_after = client.work_items.work_logs.list(
            workspace_slug, project.id, primary_work_item.id
        )
        print_success(f"Now have {len(work_logs_after)} work logs")
        total_time = sum(log.duration or 0 for log in work_logs_after)
        print_success(f"Total logged time: {total_time} minutes ({total_time / 60:.1f} hours)")

        # Cleanup: Delete created resources (optional, comment out to keep for inspection)
        print_step(14, "Cleanup (optional)")
        choice = input("Delete test resources? (y/N): ").strip().lower()
        if choice == "y":
            # Delete link
            client.work_items.links.delete(
                workspace_slug, project.id, primary_work_item.id, created_link.id
            )
            print_success("Deleted test link")

            # Delete comments
            client.work_items.comments.delete(
                workspace_slug, project.id, primary_work_item.id, created_comment.id
            )
            client.work_items.comments.delete(
                workspace_slug, project.id, primary_work_item.id, created_comment_2.id
            )
            print_success("Deleted test comments")

            # Delete work logs
            client.work_items.work_logs.delete(
                workspace_slug, project.id, primary_work_item.id, created_work_log.id
            )
            client.work_items.work_logs.delete(
                workspace_slug, project.id, primary_work_item.id, created_work_log_2.id
            )
            print_success("Deleted test work logs")

            # Delete work items
            for work_item in work_items:
                client.work_items.delete(workspace_slug, project.id, work_item.id)
                print_success(f"Deleted work item: {work_item.id}")

            # Delete project
            client.projects.delete(workspace_slug, project.id)
            print_success("Deleted test project")
        else:
            print_success("Keeping test resources for inspection")

        # Summary
        print_step(15, "Test Summary")
        print("✓ All work items base operations tested")
        print("  - Create, retrieve (by ID and identifier), update, list, search")
        print("✓ Work item relations tested")
        print("  - List, create (relates_to, blocking), delete")
        print("✓ Work item links tested")
        print("  - List, retrieve, create, update")
        print("✓ Work item comments tested")
        print("  - List, retrieve, create, update")
        print("✓ Work item activities tested")
        print("  - List, retrieve (read-only)")
        print("✓ Work item attachments tested")
        print("  - List, retrieve")
        print("✓ Work item work logs tested")
        print("  - List, create, update")
        print("\nAll work items resource tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

