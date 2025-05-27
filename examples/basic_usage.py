"""Basic usage examples for the API SDK."""

import asyncio
import os
from plane import Client, Config, SyncClient
from plane.models.user import UserCreate, UserUpdate


async def async_example():
    """Example using async client."""
    # Initialize client with config
    config = Config(
        api_key=os.getenv("MY_API_KEY", "your-api-key"),
        base_url="https://api.plane.so/api/v1",
    )

    # Or initialize from environment variables
    # client = Client()  # Uses MY_API_KEY env var

    async with Client(config) as client:
        # Check API health
        health = await client.health_check()
        print(f"API Health: {health}")

        # List users
        result = await client.users.list(page=1, per_page=10)
        users = result["users"]
        pagination = result["pagination"]

        print(
            f"Found {len(users)} users (page {pagination.page} of {pagination.total_pages})"
        )

        # Get a specific user
        if users:
            user = await client.users.get(users[0].id)
            print(f"User: {user.full_name} ({user.email})")

        # Create a new user
        new_user_data = UserCreate(
            email="newuser@example.com",
            firstName="New",
            lastName="User",
            password="securepassword123",
        )

        try:
            new_user = await client.users.create(new_user_data)
            print(f"Created user: {new_user.id}")

            # Update the user
            update_data = UserUpdate(firstName="Updated")
            updated_user = await client.users.update(new_user.id, update_data)
            print(f"Updated user: {updated_user.full_name}")

            # Search users
            search_results = await client.users.search("Updated", limit=5)
            print(f"Search found {len(search_results)} users")

            # Delete the user
            await client.users.delete(new_user.id)
            print("User deleted")

        except Exception as e:
            print(f"Error: {e}")


def sync_example():
    """Example using synchronous client."""
    config = Config(
        api_key=os.getenv("MY_API_KEY", "your-api-key"),
        base_url="https://api.example.com/v1",
    )

    with SyncClient(config) as client:
        # Check API health
        health = client.health_check()
        print(f"API Health: {health}")

        # List users
        result = client.users.list(page=1, per_page=5)
        users = result["users"]

        print(f"Found {len(users)} users")

        # Create and manage a user
        new_user_data = UserCreate(
            email="syncuser@example.com",
            firstName="Sync",
            lastName="User",
            password="securepassword123",
        )

        try:
            new_user = client.users.create(new_user_data)
            print(f"Created user: {new_user.full_name}")

            # Clean up
            client.users.delete(new_user.id)
            print("User deleted")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("=== Async Example ===")
    asyncio.run(async_example())

    print("\n=== Sync Example ===")
    sync_example()
