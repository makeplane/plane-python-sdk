#!/usr/bin/env python3
"""
Comprehensive test script for testing all pages resources end-to-end.

This script demonstrates:
1. Creating a test project
2. Testing workspace page create and retrieve operations
3. Testing project page create and retrieve operations
4. Testing query parameters

Usage:
    python test_pages.py

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
from plane.models.pages import CreatePage, Page  # noqa: E402
from plane.models.projects import CreateProject  # noqa: E402
from plane.models.query_params import RetrieveQueryParams  # noqa: E402


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

    print("Starting Comprehensive Pages SDK Test")
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

        # Create a test project (needed for project pages)
        print_step(2, "Creating a test project")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_identifier = f"PG{timestamp[-6:]}"

        project_data = CreateProject(
            name=f"Pages Test {timestamp}",
            description="Testing all pages resources",
            identifier=project_identifier,
            emoji="📄",
            page_view=True,  # Enable page view for the project
        )

        project = client.projects.create(workspace_slug, project_data)
        print_success(f"Project created: {project.name} (ID: {project.id})")

        workspace_page_data = CreatePage(
            name=f"Test Workspace Page - {timestamp}",
            description_html="<p>This is a test workspace page created via SDK.</p>",
            color="#FF6B6B",
        )
        created_workspace_page = client.pages.create_workspace_page(
            workspace_slug, workspace_page_data
        )
        print_success(f"Created workspace page: {created_workspace_page.name}")
        print_success(f"  Page ID: {created_workspace_page.id}")

        # Test retrieving workspace page
        print_step(4, "Testing retrieve workspace page")
        if not created_workspace_page.id:
            raise AssertionError("Created workspace page ID is missing")

        retrieved_workspace_page = client.pages.retrieve_workspace_page(
            workspace_slug, created_workspace_page.id
        )
        if retrieved_workspace_page.id != created_workspace_page.id:
            raise AssertionError(
                "Retrieved workspace page ID does not match created page ID"
            )
        page_name = retrieved_workspace_page.name or "unnamed"
        print_success(f"Retrieved workspace page: {page_name}")
        print_success(f"  Page ID: {retrieved_workspace_page.id}")

        # Test retrieve with query parameters
        print_step(5, "Testing retrieve workspace page with parameters")
        retrieve_params = RetrieveQueryParams(expand="workspace")
        client.pages.retrieve_workspace_page(
            workspace_slug, created_workspace_page.id, params=retrieve_params
        )
        print_success("Retrieved workspace page with expand parameter")

        # Test creating project page
        print_step(6, "Testing create project page")
        project_page_data = CreatePage(
            name=f"Test Project Page - {timestamp}",
            description_html="<p>This is a test project page created via SDK.</p>",
            color="#4ECDC4",
        )
        created_project_page = client.pages.create_project_page(
            workspace_slug, project.id, project_page_data
        )
        print_success(f"Created project page: {created_project_page.name}")
        print_success(f"  Page ID: {created_project_page.id}")

        # Test retrieving project page
        print_step(7, "Testing retrieve project page")
        if not created_project_page.id:
            raise AssertionError("Created project page ID is missing")

        retrieved_project_page = client.pages.retrieve_project_page(
            workspace_slug, project.id, created_project_page.id
        )
        if retrieved_project_page.id != created_project_page.id:
            raise AssertionError(
                "Retrieved project page ID does not match created page ID"
            )
        page_name = retrieved_project_page.name or "unnamed"
        print_success(f"Retrieved project page: {page_name}")
        print_success(f"  Page ID: {retrieved_project_page.id}")

        # Test retrieve with query parameters
        print_step(8, "Testing retrieve project page with parameters")
        retrieve_params = RetrieveQueryParams(expand="project,workspace")
        client.pages.retrieve_project_page(
            workspace_slug,
            project.id,
            created_project_page.id,
            params=retrieve_params,
        )
        print_success("Retrieved project page with expand parameter")

        # Verify API response structures
        print_step(9, "Verifying API response structures")
        if not isinstance(retrieved_workspace_page, Page):
            raise AssertionError(
                f"Expected Page from retrieve_workspace_page, "
                f"got {type(retrieved_workspace_page)}"
            )
        print_success("Workspace page retrieve returns Page model")

        if not isinstance(retrieved_project_page, Page):
            raise AssertionError(
                f"Expected Page from retrieve_project_page, "
                f"got {type(retrieved_project_page)}"
            )
        print_success("Project page retrieve returns Page model")

        # Cleanup: Delete created resources (optional)
        print_step(10, "Cleanup (optional)")
        choice = input("Delete test project? (y/N): ").strip().lower()
        if choice == "y":
            try:
                client.projects.delete(workspace_slug, project.id)
                print_success("Deleted test project")
            except Exception as e:
                print_error(f"Failed to delete project: {e}")
        else:
            print_success("Keeping test project for inspection")
            print_success(
                f"You can view the project at: {base_url}/w/{workspace_slug}/p/{project.id}"
            )

        # Summary
        print_step(11, "Test Summary")
        print("✓ Workspace page operations tested")
        print("  - Create workspace page, retrieve workspace page")
        print("✓ Project page operations tested")
        print("  - Create project page, retrieve project page")
        print("✓ Query parameters tested")
        print("  - Retrieve with expand parameter")
        print("✓ API response structure verified")
        print("  - All operations return proper Pydantic models")
        print(f"✓ Project created: {project.name}")
        print("✓ Created 1 workspace page")
        print("✓ Created 1 project page")
        print("\nAll pages resource tests completed successfully!")
        print(f"\nView your project at: {base_url}/w/{workspace_slug}/p/{project.id}")

    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

