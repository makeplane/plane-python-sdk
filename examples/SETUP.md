# Examples Setup Guide

This guide will help you set up your environment to run the Plane Python SDK examples.

## Prerequisites

1. **Python 3.10 or higher** installed on your system
2. **Plane SDK** installed
3. **Plane API credentials** (API key or access token)
4. **Workspace access** to a Plane workspace

## Installation

### 1. Install the Plane SDK

If you haven't already installed the SDK:

```bash
pip install plane-sdk
```

Or if you're developing locally:

```bash
cd plane-python-sdk
pip install -e .
```

### 2. Set Up Environment Variables

You need to configure authentication and workspace information via environment variables.

#### Option A: Export directly in your shell

**macOS/Linux (bash/zsh):**

```bash
export PLANE_BASE_URL="https://api.plane.so"
export PLANE_API_KEY="your-api-key-here"
export WORKSPACE_SLUG="your-workspace-slug"
```

**Windows (PowerShell):**

```powershell
$env:PLANE_BASE_URL = "https://api.plane.so"
$env:PLANE_API_KEY = "your-api-key-here"
$env:WORKSPACE_SLUG = "your-workspace-slug"
```

**Windows (Command Prompt):**

```cmd
set PLANE_BASE_URL=https://api.plane.so
set PLANE_API_KEY=your-api-key-here
set WORKSPACE_SLUG=your-workspace-slug
```

#### Option B: Create a shell script

Create a file named `setup_env.sh` (macOS/Linux) or `setup_env.bat` (Windows):

**macOS/Linux (`setup_env.sh`):**

```bash
#!/bin/bash
export PLANE_BASE_URL="https://api.plane.so"
export PLANE_API_KEY="your-api-key-here"
export WORKSPACE_SLUG="your-workspace-slug"
```

Then source it:

```bash
chmod +x setup_env.sh
source setup_env.sh
```

**Windows (`setup_env.bat`):**

```batch
@echo off
set PLANE_BASE_URL=https://api.plane.so
set PLANE_API_KEY=your-api-key-here
set WORKSPACE_SLUG=your-workspace-slug
```

Then run it:

```cmd
setup_env.bat
```

## Getting Your Credentials

### API Key

1. Log in to your Plane instance
2. Go to **Settings** → **API Tokens**
3. Create a new API token
4. Copy the token and use it as your `PLANE_API_KEY`

### Access Token (Alternative)

If you're using OAuth or need to use an access token instead:

1. Obtain your access token from your OAuth flow
2. Set `PLANE_ACCESS_TOKEN` instead of `PLANE_API_KEY`

```bash
export PLANE_ACCESS_TOKEN="your-access-token-here"
```

**Important:** Only use ONE authentication method - either API key or access token, not both.

### Workspace Slug

The workspace slug is the identifier for your workspace. You can find it in the URL when you're viewing your workspace:

```
https://app.plane.so/<workspace-slug>/projects
                      ^^^^^^^^^^^^^^^^^
                      This is your workspace slug
```

## Running the Examples

Once your environment is configured, you can run the examples:

```bash
# Set up a complete project with work item types, states, and labels
python examples/setup_project.py

# Create a basic project with work items
python examples/create_work_items.py
```

## Verifying Your Setup

Create a simple test script to verify your setup:

```python
# test_setup.py
import os
from plane.client import PlaneClient

try:
    client = PlaneClient(
        base_url=os.environ.get("PLANE_BASE_URL"),
        api_key=os.environ.get("PLANE_API_KEY"),
    )

    # Try to fetch user info
    me = client.users.get_me()
    print(f"✓ Successfully connected as: {me.email}")
    print("✓ Your environment is set up correctly!")

except Exception as e:
    print(f"✗ Setup verification failed: {e}")
    print("\nPlease check:")
    print("1. PLANE_BASE_URL is set correctly")
    print("2. PLANE_API_KEY is valid")
    print("3. You have network access to the Plane API")
```

Run it:

```bash
python test_setup.py
```

## Troubleshooting

### "ConfigurationError: Either 'api_key' or 'access_token' must be provided"

- Make sure you've set either `PLANE_API_KEY` or `PLANE_ACCESS_TOKEN`
- Check that the environment variable is exported in your current shell session
- Try printing the environment variable: `echo $PLANE_API_KEY` (macOS/Linux) or `echo %PLANE_API_KEY%` (Windows)

### "HttpError 401: Unauthorized"

- Your API key or access token is invalid or expired
- Generate a new API token from Plane settings
- Make sure there are no extra spaces in your environment variable

### "HttpError 404: Not Found"

- Your `WORKSPACE_SLUG` might be incorrect
- Verify the workspace slug from your Plane URL
- Make sure you have access to the workspace

### Import errors

- Make sure you've installed the SDK: `pip install plane-sdk`
- Or if developing locally: `pip install -e .` from the root directory
- Verify your Python version: `python --version` (should be 3.10+)

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate API keys** regularly
4. **Use separate credentials** for development and production
5. **Limit API key permissions** to only what's needed

## Next Steps

- Review the [examples README](README.md) for an overview
- Run `setup_project.py` to see full project configuration
- Run `create_work_items.py` to create a project with work items
- Check the [main SDK documentation](../README.md) for more features

## Additional Resources

- [Plane Python SDK Documentation](../README.md)
- [Plane API Documentation](https://docs.plane.so)
- [Plane Website](https://plane.so)

## Getting Help

If you encounter issues:

1. Check this SETUP.md guide
2. Review the examples README.md
3. Check the main SDK README.md
4. File an issue on GitHub
5. Contact support at dev@plane.so
