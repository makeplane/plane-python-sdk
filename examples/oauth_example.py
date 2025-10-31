"""
OAuth Example for Plane Python SDK

This example demonstrates how to use the OAuthClient for different OAuth flows.
"""

import os

from plane import OAuthClient, OAuthToken, PlaneClient

# ============================================================================
# Example 1: Authorization Code Flow (Web Applications)
# ============================================================================


def authorization_code_flow_example():
    """
    Example of OAuth authorization code flow.

    This is typically used for web applications where users authorize
    your application to access their Plane data.
    """
    # Initialize OAuth client
    oauth_client = OAuthClient(
        base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
    )

    # Step 1: Generate authorization URL
    redirect_uri = "https://your-app.com/oauth/callback"
    state = "random_state_string_for_csrf_protection"

    auth_url = oauth_client.get_authorization_url(
        redirect_uri=redirect_uri,
        scope="read write",
        state=state,
    )

    print(f"Redirect user to: {auth_url}")

    # Step 2: After user authorizes, you'll receive a callback with code and state
    # Verify state matches, then exchange code for token
    authorization_code = "code_from_callback_query_param"

    token = oauth_client.exchange_code(
        code=authorization_code,
        redirect_uri=redirect_uri,
    )

    print(f"Access Token: {token.access_token}")
    print(f"Refresh Token: {token.refresh_token}")
    print(f"Expires In: {token.expires_in} seconds")

    # Step 3: Use the access token with PlaneClient
    workspace_slug = os.environ.get("WORKSPACE_SLUG", "your-workspace-slug")
    plane_client = PlaneClient(
        base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
        access_token=token.access_token,
    )

    # Now you can use the plane_client to make API calls
    projects = plane_client.projects.list(workspace_slug)
    print(f"Found {len(projects.results)} projects")

    # Step 4: Refresh token when it expires
    if token.refresh_token:
        new_token = oauth_client.refresh_token(token.refresh_token)
        print(f"New Access Token: {new_token.access_token}")


# ============================================================================
# Example 2: Client Credentials Flow (Server-to-Server)
# ============================================================================


def client_credentials_flow_example():
    """
    Example of OAuth client credentials flow.

    This is used for server-to-server authentication where your application
    needs to access Plane API without user interaction.
    """
    # Initialize OAuth client
    oauth_client = OAuthClient(
        base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
    )

    # Get access token using client credentials
    token = oauth_client.get_client_credentials_token(
        scope="read write",
    )

    print(f"Access Token: {token.access_token}")
    print(f"Expires In: {token.expires_in} seconds")

    # Use the access token with PlaneClient
    workspace_slug = os.environ.get("WORKSPACE_SLUG", "your-workspace-slug")
    plane_client = PlaneClient(
        base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
        access_token=token.access_token,
    )

    # Make API calls
    projects = plane_client.projects.list(workspace_slug)
    print(f"Found {len(projects.results)} projects")


# ============================================================================
# Example 3: Client Credentials Flow with App Installation (Bot Token)
# ============================================================================


def bot_token_example():
    """
    Example of getting a bot token for workspace app installation.

    Use this when you need a bot token for a specific workspace app installation.
    """
    oauth_client = OAuthClient(
        base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
    )

    # Get bot token for specific app installation
    token = oauth_client.get_client_credentials_token(
        scope="read write",
        app_installation_id=os.environ["APP_INSTALLATION_ID"],
    )

    print(f"Bot Access Token: {token.access_token}")

    # Use bot token with PlaneClient
    workspace_slug = os.environ.get("WORKSPACE_SLUG", "your-workspace-slug")
    plane_client = PlaneClient(
        base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
        access_token=token.access_token,
    )

    # Bot can now perform actions on behalf of the workspace app
    projects = plane_client.projects.list(workspace_slug)
    print(f"Bot can access {len(projects.results)} projects")


# ============================================================================
# Example 4: Token Management
# ============================================================================


def token_management_example():
    """
    Example of managing OAuth tokens (refresh, revoke).
    """
    oauth_client = OAuthClient(
        base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
    )

    # Assume we have a token from previous authorization
    existing_token = OAuthToken(
        access_token="existing_access_token",
        refresh_token="existing_refresh_token",
        token_type="Bearer",
        expires_in=3600,
    )

    # Refresh the token before it expires
    if existing_token.refresh_token:
        new_token = oauth_client.refresh_token(existing_token.refresh_token)
        print(f"Refreshed token: {new_token.access_token}")

    # Revoke token when user logs out or app is uninstalled
    try:
        oauth_client.revoke_token(existing_token.access_token)
        print("Token revoked successfully")
    except Exception as e:
        print(f"Failed to revoke token: {e}")


# ============================================================================
# Example 5: Using Context Manager
# ============================================================================


def context_manager_example():
    """
    Example of using OAuthClient with context manager for automatic cleanup.
    """
    with OAuthClient(
        base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
    ) as oauth_client:
        # Get token
        token = oauth_client.get_client_credentials_token()

        # Use token
        workspace_slug = os.environ.get("WORKSPACE_SLUG", "your-workspace-slug")
        plane_client = PlaneClient(
            base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
            access_token=token.access_token,
        )

        projects = plane_client.projects.list(workspace_slug)
        print(f"Found {len(projects.results)} projects")

    # Session is automatically closed when exiting context


# ============================================================================
# Example 6: Error Handling
# ============================================================================


def error_handling_example():
    """
    Example of handling OAuth errors properly.
    """
    from plane import ConfigurationError, HttpError

    try:
        oauth_client = OAuthClient(
            base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
            client_id=os.environ.get("OAUTH_CLIENT_ID", ""),
            client_secret=os.environ.get("OAUTH_CLIENT_SECRET", ""),
        )

        token = oauth_client.get_client_credentials_token()
        print(f"Token obtained: {token.access_token}")

    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        # Handle missing or invalid configuration

    except HttpError as e:
        print(f"HTTP error: {e}")
        print(f"Status code: {e.status_code}")
        print(f"Response: {e.response}")
        # Handle API errors (invalid credentials, network issues, etc.)

    except Exception as e:
        print(f"Unexpected error: {e}")
        # Handle other errors


if __name__ == "__main__":
    print("OAuth Examples for Plane Python SDK")
    print("=" * 50)

    # Uncomment the example you want to run:
    # authorization_code_flow_example()
    # client_credentials_flow_example()
    # bot_token_example()
    # token_management_example()
    # context_manager_example()
    # error_handling_example()

    print("\nRemember to set the following environment variables:")
    print("  - PLANE_BASE_URL (optional, defaults to https://api.plane.so)")
    print("  - OAUTH_CLIENT_ID")
    print("  - OAUTH_CLIENT_SECRET")
    print("  - WORKSPACE_SLUG (required for API calls)")
    print("  - APP_INSTALLATION_ID (for bot token example)")

