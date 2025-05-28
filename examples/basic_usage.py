"""Basic usage examples for the API SDK (Project info)."""

import asyncio
import os
from plane import Client, Config, SyncClient


async def async_example():
    """Example using async client for projects."""
    config = Config(
        api_key=os.getenv("MY_API_KEY", "your-api-key"),
        base_url="https://api.plane.so/api/v1",
    )

    async with Client(config) as client:
        # Check API health
        health = await client.health_check()
        print(f"API Health: {health}")

        # List workspaces
        ws_result = await client.workspaces.list(page=1, per_page=5)
        workspaces = ws_result["workspaces"]
        if not workspaces:
            print("No workspaces found.")
            return
        workspace = workspaces[0]
        print(f"Using workspace: {workspace.name} (slug: {workspace.slug})")

        # List projects in the workspace
        proj_result = await client.projects.list(workspace.slug, page=1, per_page=10)
        projects = proj_result["projects"]
        pagination = proj_result["pagination"]
        print(
            f"Found {len(projects)} projects (page {pagination.page} of {pagination.total_pages})"
        )
        for project in projects:
            print(f"- {project.name} (id: {project.id}, desc: {project.description})")

        # Get a specific project (first one)
        if projects:
            project = await client.projects.get(workspace.slug, projects[0].id)
            print(
                f"Project details: {project.name} (id: {project.id}) - {project.description}"
            )


def sync_example():
    """Example using synchronous client for projects."""
    config = Config(
        api_key=os.getenv("MY_API_KEY", "your-api-key"),
        base_url="https://api.plane.so/api/v1",
    )

    with SyncClient(config) as client:
        # Check API health
        health = client.health_check()
        print(f"API Health: {health}")

        # List workspaces
        ws_result = client.workspaces.list(page=1, per_page=5)
        workspaces = ws_result["workspaces"]
        if not workspaces:
            print("No workspaces found.")
            return
        workspace = workspaces[0]
        print(f"Using workspace: {workspace.name} (slug: {workspace.slug})")

        # List projects in the workspace
        proj_result = client.projects.list(workspace.slug, page=1, per_page=10)
        projects = proj_result["projects"]
        pagination = proj_result["pagination"]
        print(
            f"Found {len(projects)} projects (page {pagination.page} of {pagination.total_pages})"
        )
        for project in projects:
            print(f"- {project.name} (id: {project.id}, desc: {project.description})")

        # Get a specific project (first one)
        if projects:
            project = client.projects.get(workspace.slug, projects[0].id)
            print(
                f"Project details: {project.name} (id: {project.id}) - {project.description}"
            )


if __name__ == "__main__":
    print("=== Async Example ===")
    asyncio.run(async_example())

    print("\n=== Sync Example ===")
    sync_example()
