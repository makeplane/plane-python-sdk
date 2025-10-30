# Test Script Usage Guide

This guide explains how to use the standalone test scripts to test the Plane Python SDK across different API resources and features.

## Overview

The test scripts in this directory provide comprehensive testing for various Plane SDK features. Each script is self-contained and can be run independently to test specific API resources or workflows.

## Available Test Scripts

| Script                                   | Purpose                                                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `test_work_items.py`                     | Comprehensive work items testing (CRUD, relations, links, comments, activities, attachments, work logs) |
| `test_property_values.py`                | Work item property values operations (create, update, retrieve, delete)                                 |
| `test_advanced_properties.py`            | Advanced property scenarios (multiple property types, validation, complex assignments)                  |
| `test_work_item_types_and_properties.py` | Work item types and custom properties testing                                                           |
| `test_cycles.py`                         | Cycle management (create, archive, transfer work items)                                                 |
| `test_modules.py`                        | Module management (create, update, archive, work item associations)                                     |
| `test_labels.py`                         | Label CRUD operations and parent-child relationships                                                    |
| `test_epics.py`                          | Epic list and retrieve operations with query parameters                                                 |
| `test_pages.py`                          | Workspace and project pages (create, retrieve)                                                          |
| `test_customers.py`                      | Customer management (properties, customers, requests)                                                   |
| `test_intake.py`                         | Intake work items operations                                                                            |
| `test_comprehensive.py`                  | End-to-end testing across multiple features                                                             |

## Prerequisites

- Python 3.10 or higher
- Plane Python SDK installed (or run from the SDK directory)
- A Plane instance (self-hosted or cloud)
- Valid API credentials (API Key or Access Token)
- An existing workspace slug

## Setup

### 1. Set Environment Variables (REQUIRED)

**Important**: All environment variables are required. No default values are provided.

You must set the following environment variables:

```bash
export BASE_URL="https://api.plane.so"     # Your Plane instance URL (required)
export WORKSPACE_SLUG="your-workspace"     # Your workspace slug (required)
export API_KEY="your_api_key"              # Your API key (required if not using ACCESS_TOKEN)
# OR
export ACCESS_TOKEN="your_token"           # Your access token (required if not using API_KEY)
```

**Note**: You must provide either `API_KEY` or `ACCESS_TOKEN`, but not necessarily both.

### 2. Install Dependencies

**Option A: Install the SDK in editable mode (Recommended)**

This installs the SDK package so Python can find it anywhere:

```bash
cd plane-python-sdk
pip install -e .
```

**Option B: Use the scripts as-is**

The test scripts automatically add the project root to Python's path, so they will work without installation. However, installing in editable mode is recommended for a cleaner development setup.

## Running the Tests

### Basic Usage

Run any test script:

```bash
python test_work_items.py
python test_property_values.py
python test_labels.py
# ... etc
```

### Example with Inline Environment Variables

```bash
BASE_URL="https://api.plane.so" \
API_KEY="your_api_key" \
WORKSPACE_SLUG="my-workspace" \
python test_work_items.py
```

### Using a .env File

You can use a `.env` file with a tool like `python-dotenv`:

1. Create a `.env` file in the `tests/scripts/` directory:

```bash
BASE_URL=https://api.plane.so
API_KEY=your_api_key_here
WORKSPACE_SLUG=your-workspace-slug
```

2. Optionally modify the script to load from `.env`:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Expected Output

All test scripts follow a similar format with step-by-step progress messages:

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

...

======================================================================
Step N: Cleanup (optional)
======================================================================
Delete test resources? (y/N):
```

## Cleanup

All test scripts include an interactive cleanup section at the end. When the test completes, you'll be prompted:

```
Delete test resources? (y/N):
```

- **'y'**: Deletes all created test resources (projects, work items, labels, etc.)
- **'N'** (default): Keeps all resources for manual inspection

The cleanup section handles resource deletion in the correct order (child resources before parent resources) and provides clear success/error messages for each deletion operation.

**Note**: Resources are always cleaned up in reverse order of creation to avoid dependency issues.

## Troubleshooting

### Missing Environment Variables

If you see this error:

```
✗ BASE_URL environment variable is required
```

**All environment variables must be explicitly set.** The scripts no longer use default values. Make sure you have set:

- `BASE_URL`
- `WORKSPACE_SLUG`
- Either `API_KEY` or `ACCESS_TOKEN`

### Authentication Errors

If you see HTTP 401 or 403 errors:

- Verify your API key or access token is valid and not expired
- Check that you have the correct permissions in the workspace
- Ensure you're using the correct authentication method (API key vs access token)

### Connection Errors

If you see connection errors:

- Verify the `BASE_URL` is correct and includes the protocol (`https://` or `http://`)
- Check that the Plane instance is accessible from your network
- Ensure there are no network/firewall issues blocking the connection

### Cleanup Failures

If cleanup fails:

- Some resources may have dependencies that prevent deletion
- The script will report which specific resources failed to delete
- You can manually delete remaining resources through the Plane UI
- Future runs will clean up any previously created resources

## Script-Specific Information

### test_work_items.py

Comprehensive work items test:

- CRUD operations
- Relations (relates_to, blocking)
- Links
- Comments
- Activities (read-only)
- Attachments
- Work logs

### test_property_values.py

Property value operations:

- Creating property values for various types (text, boolean, decimal, datetime, option)
- Multi-value properties
- Updating property values
- Deleting property values

### test_advanced_properties.py

Advanced property scenarios:

- Multiple property types (URL, email, datetime, multi-select, relations)
- Property validation
- Complex property value assignments

### test_work_item_types_and_properties.py

Work item types and properties:

- Creating work item types (Bug, Feature, Epic)
- Creating custom properties
- Creating property options
- Assigning property values to work items

### test_cycles.py

Cycle management:

- Creating cycles
- Adding/removing work items from cycles
- Transferring work items between cycles
- Archiving/unarchiving cycles

### test_modules.py

Module management:

- Creating modules with different statuses
- Adding/removing work items from modules
- Updating module details
- Archiving/unarchiving modules

### test_comprehensive.py

End-to-end workflow:

- Multiple work item types
- Custom properties across types
- Property values
- Cycle creation and work item assignment

## Customization

All test scripts follow a consistent structure:

1. Environment variable validation
2. Client initialization
3. Resource creation and testing
4. Interactive cleanup
5. Summary

You can easily modify any script to:

- Add additional test cases
- Test different API features
- Customize resource creation parameters
- Add more comprehensive error handling

## Best Practices

1. **Run tests in a dedicated workspace** to avoid cluttering your production workspace
2. **Review cleanup prompts carefully** before confirming deletion
3. **Use environment variables** instead of hardcoding credentials
4. **Run one script at a time** to avoid conflicts between tests
5. **Check script output** for success/failure messages after each step

## Error Handling

All scripts use consistent error handling:

- Prints error messages to stderr
- Displays full traceback for debugging
- Exits with code 1 on failure
- Continues execution until an unrecoverable error occurs

If a script fails:

1. Check the error message for specific issues
2. Verify your environment variables are set correctly
3. Check your API credentials and permissions
4. Review the traceback for detailed error information
