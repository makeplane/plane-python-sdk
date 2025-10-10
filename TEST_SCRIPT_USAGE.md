# Test Script Usage Guide

This guide explains how to use the standalone test script (`test_sdk.py`) to quickly test the Plane Python SDK.

## Overview

The `test_sdk.py` script performs the following operations:

1. Initializes the Plane client
2. Creates a new project in an existing workspace
3. Creates multiple labels (Bug, Feature, Documentation)
4. Creates a work item
5. Assigns the labels to the work item
6. Verifies the work item was created successfully

## Prerequisites

- Python 3.10 or higher
- Plane Python SDK installed (or run from the SDK directory)
- A Plane instance (self-hosted or cloud)
- Valid API credentials (API Key or Access Token)
- An existing workspace slug

## Setup

### 1. Set Environment Variables

You need to set the following environment variables:

```bash
export BASE_URL="https://api.plane.so"  # Your Plane instance URL
export WORKSPACE_SLUG="your-workspace"   # Your workspace slug
export API_KEY="your_api_key"            # Your API key (or use ACCESS_TOKEN)
# OR
export ACCESS_TOKEN="your_token"         # Your access token (alternative to API_KEY)
```

### 2. Install Dependencies

If not already installed:

```bash
cd plane-python-sdk
pip install -r requirements.txt
```

## Running the Test

### Basic Usage

Simply run the script:

```bash
python test_sdk.py
```

### Example with Inline Environment Variables

```bash
BASE_URL="https://api.plane.so" \
API_KEY="your_api_key" \
WORKSPACE_SLUG="my-workspace" \
python test_sdk.py
```

### Using a .env File

You can also use a `.env` file with a tool like `python-dotenv`:

1. Create a `.env` file:

```bash
BASE_URL=https://api.plane.so
API_KEY=your_api_key_here
WORKSPACE_SLUG=your-workspace-slug
```

2. Modify the script to load from `.env`:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Expected Output

The script will print progress messages for each step:

```
Starting Plane Python SDK Test
Base URL: https://api.plane.so
Workspace: my-workspace
Authentication: API Key

======================================================================
Step 1: Initializing Plane Client
======================================================================
✓ Client initialized successfully

======================================================================
Step 2: Creating a new project
======================================================================
✓ Project created: Test Project 20250109_143025 (ID: abc-123-def)
  Identifier: TEST143025
  Emoji: 🧪

======================================================================
Step 3: Creating labels
======================================================================
✓ Label created: Bug (ID: label-1, Color: #FF0000)
✓ Label created: Feature (ID: label-2, Color: #00FF00)
✓ Label created: Documentation (ID: label-3, Color: #0000FF)

======================================================================
Step 4: Creating a work item
======================================================================
✓ Work item created: Test Work Item - SDK Testing (ID: work-item-1)
  Priority: medium
  Sequence ID: 1

======================================================================
Step 5: Assigning labels to work item
======================================================================
✓ Labels assigned to work item: 3 labels

======================================================================
Step 6: Verifying work item
======================================================================
✓ Work item retrieved: Test Work Item - SDK Testing
  ID: work-item-1
  State: state-id
  Priority: medium

======================================================================
Step 7: Test Summary
======================================================================
✓ Project created: Test Project 20250109_143025
✓ Labels created: 3
✓ Work item created: Test Work Item - SDK Testing
✓ Labels assigned to work item

All tests completed successfully!

View your project at: https://api.plane.so/w/my-workspace/p/abc-123-def
```

## Troubleshooting

### Missing Environment Variables

If you see this error:

```
✗ BASE_URL environment variable is required
```

Make sure all required environment variables are set.

### Authentication Errors

If you see HTTP 401 or 403 errors, check that:

- Your API key or access token is valid
- You have the correct permissions in the workspace

### Connection Errors

If you see connection errors:

- Verify the `BASE_URL` is correct
- Check that the Plane instance is accessible
- Ensure there are no network/firewall issues

## Cleanup

The script creates test resources with timestamped names. You can manually delete them from your workspace if needed:

- Projects will have names like "Test Project 20250109_143025"
- Work items will be named "Test Work Item - SDK Testing"

## Customization

You can easily modify the script to test other SDK features:

- Add more labels
- Create multiple work items
- Test other resources (modules, cycles, etc.)
- Add custom properties to work items

Simply edit `test_sdk.py` and add your test cases.
