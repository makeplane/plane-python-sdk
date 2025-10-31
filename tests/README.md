# Tests

This directory contains comprehensive test cases for the Plane Python SDK.

## Test Structure

The test suite is organized into two main categories:

### Unit Tests (`tests/unit/`)

Pytest-based unit tests that make real HTTP requests (no mocking) and function as smoke tests. These tests verify that all API endpoints are accessible and return expected data structures.

**Test Files:**

- `test_users.py` - Users API (get_me, list, retrieve)
- `test_workspaces.py` - Workspaces API (get_members)
- `test_projects.py` - Projects API (CRUD operations)
- `test_labels.py` - Labels API (CRUD operations)
- `test_states.py` - States API (CRUD operations)
- `test_epics.py` - Epics API (list, retrieve)
- `test_work_items.py` - WorkItems API (CRUD + sub-resources: comments, links, activities, attachments)
- `test_modules.py` - Modules API (CRUD operations)
- `test_cycles.py` - Cycles API (CRUD operations)
- `test_pages.py` - Pages API (project/workspace page creation)
- `test_intake.py` - Intake API (CRUD operations)
- `test_work_item_types.py` - WorkItemTypes API (CRUD operations)
- `test_work_item_properties.py` - WorkItemProperties API (CRUD operations)
- `test_customers.py` - Customers API (CRUD operations)

**Shared Fixtures (`conftest.py`):**

- `client` - Initialized Plane client with authentication
- `base_url` - Base URL from environment (PLANE_BASE_URL)
- `api_key` / `access_token` - Authentication credentials (PLANE_API_KEY / PLANE_ACCESS_TOKEN)
- `workspace_slug` - Workspace identifier (WORKSPACE_SLUG)

### Integration/Script Tests (`tests/scripts/`)

Comprehensive integration tests and example scripts demonstrating complex workflows.

**Test Files:**

- `test_comprehensive.py` - End-to-end tests covering project creation, work items, properties, and cycles
- `test_modules.py` - Tests for module functionality including creation, updates, archiving, and work item management
- `test_property_values.py` - Tests for property value operations including create, update, retrieve, and delete
- `test_advanced_properties.py` - Advanced property configuration and usage tests
- `test_work_item_types_and_properties.py` - Combined tests for work item types and their properties
- Additional resource-specific test scripts

See `tests/scripts/TEST_SCRIPT_USAGE.md` for detailed usage instructions for script tests.

## Running Tests

### Prerequisites

Set the following environment variables:

```bash
export PLANE_BASE_URL="http://127.0.0.1:8000"  # or https://api.plane.so
export PLANE_API_KEY="your_api_key"              # or PLANE_ACCESS_TOKEN
export WORKSPACE_SLUG="your_workspace"
```

### Run All Tests

```bash
# Run all unit and script tests
pytest tests/

# Run only unit tests
pytest tests/unit/

# Run only script tests
pytest tests/scripts/
```

### Run Specific Test Files

```bash
# Unit tests
pytest tests/unit/test_projects.py
pytest tests/unit/test_work_items.py
pytest tests/unit/test_modules.py

# Script tests
pytest tests/scripts/test_comprehensive.py
pytest tests/scripts/test_modules.py
pytest tests/scripts/test_property_values.py
```

### Run Specific Test Classes

```bash
# Unit test classes
pytest tests/unit/test_projects.py::TestProjectsAPICRUD
pytest tests/unit/test_work_items.py::TestWorkItemsAPICRUD

# Script test classes
pytest tests/scripts/test_comprehensive.py::TestComprehensiveWorkflow
pytest tests/scripts/test_modules.py::TestModuleFunctionality
pytest tests/scripts/test_property_values.py::TestPropertyValueOperations
```

### Run Specific Test Cases

```bash
pytest tests/unit/test_projects.py::TestProjectsAPICRUD::test_create_project
pytest tests/scripts/test_comprehensive.py::TestComprehensiveWorkflow::test_create_project_with_all_features
```

### Verbose Output

```bash
pytest tests/ -v
```

### With Coverage

```bash
pytest tests/ --cov=plane --cov-report=html
```

## Test Characteristics

### Unit Tests (Smoke Tests)

- **No Mocking**: All tests make real HTTP requests to verify API connectivity
- **Smoke Test Focus**: Basic functionality verification (endpoints respond, data structures are correct)
- **Automatic Cleanup**: Resources created during tests are automatically cleaned up via pytest fixtures
- **Environment-Aware**: Tests automatically skip if required environment variables are not set
- **Fast Execution**: Lightweight tests focused on API endpoint accessibility

### Script Tests (Integration Tests)

- **Comprehensive Coverage**: End-to-end workflows and complex scenarios
- **Real API Interactions**: Full integration with Plane API
- **Detailed Examples**: Serve as both tests and usage examples
- **Resource Management**: Manual or automatic cleanup depending on test complexity

## Cleanup

All tests automatically clean up resources they create:

- **Unit Tests**: Resources are cleaned up automatically via pytest fixtures using `yield` statements
- **Script Tests**: Cleanup behavior varies by test file; most include cleanup logic
- Projects, work items, labels, states, and other resources are deleted after tests complete
- If cleanup fails (e.g., due to permissions), a warning may be printed but tests continue

## Requirements

These tests require:

1. A running Plane instance (local or hosted)
2. Valid API credentials (PLANE_API_KEY or PLANE_ACCESS_TOKEN)
3. Appropriate workspace permissions
4. Network access to the Plane API endpoint

Most tests will skip automatically if required environment variables are not set, making them safe to run in CI/CD pipelines.

## Best Practices

### For Unit Tests

- Keep tests focused on single API operations
- Use fixtures for shared setup and teardown
- Avoid creating unnecessary resources
- Test both success and expected error cases

### For Script Tests

- Document complex workflows clearly
- Include cleanup in test scripts
- Provide meaningful assertions and output
- Use as reference implementations for SDK usage
