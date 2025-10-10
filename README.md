# Plane Python SDK v1

A comprehensive, type-annotated Python SDK for interacting with the Plane API. This SDK provides a clean, modern interface for all Plane API operations, following Python best practices with full type safety and Pydantic v2 integration.

## Features

- 🚀 **Type-Safe**: Full type annotations with Pydantic v2 models
- 🔧 **Modern Python**: Built for Python 3.10+ with modern typing idioms
- 🛡️ **Error Handling**: Comprehensive error types and exception handling
- 🔄 **Retry Logic**: Built-in retry mechanism with configurable backoff
- 📦 **Resource-Based**: Clean resource-based API organization
- 🎯 **Comprehensive**: Support for all major Plane API endpoints

## Installation

```bash
pip install plane-python-sdk
```

## Quick Start

### Authentication

⚠️ **Required**: You must provide **exactly one** of `api_key` or `access_token` for authentication.

```python
import os
from plane.client import PlaneClient
from plane.errors import ConfigurationError

# Using API key
client = PlaneClient(
    base_url="https://api.plane.so",
    api_key=os.environ["PLANE_API_KEY"]
)

# OR using access token (not both)
client = PlaneClient(
    base_url="https://api.plane.so",
    access_token=os.environ["PLANE_ACCESS_TOKEN"]
)

# Raises ConfigurationError if neither or both are provided
```

### Basic Usage

```python
# List projects in a workspace
projects = client.projects.list(workspace_slug="my-workspace")

# Create a work item
from plane.models.schemas import CreateWorkItem

work_item = client.work_items.create(
    workspace_slug="my-workspace",
    project_id="project-id",
    data=CreateWorkItem(name="New task", state="state-id")
)

# Query with typed parameters
from plane.models.schemas import WorkItemQueryParams

work_items = client.work_items.list(
    workspace_slug="my-workspace",
    project_id="project-id",
    params=WorkItemQueryParams(
        expand="assignees,labels",
        order_by="-created_at",
        per_page=50
    )
)
```

## Architecture

### Client Structure

The SDK is organized around a central `PlaneClient` that provides access to various resource classes:

```python
from plane.client import PlaneClient

client = PlaneClient(
    base_url="https://api.plane.so",
    api_key="your-api-key"
)

# Access different resources
client.work_items      # Work item operations
client.projects        # Project management
client.users           # User management
client.cycles          # Cycle management
client.modules         # Module management
# ... and more
```

### Resource Organization

All API resources extend a shared `BaseResource` class that handles:

- HTTP request/response logic
- Authentication headers
- Error handling
- Retry logic
- URL building

### Type Safety

The SDK uses Pydantic v2 models for all data structures:

- Request models (e.g., `CreateWorkItem`, `UpdateProject`)
- Response models (e.g., `WorkItem`, `Project`)
- Query parameter models (e.g., `WorkItemQueryParams`)

## Available Resources

### Core Resources

#### Work Items

```python
# Create, read, update, delete work items
client.work_items.create(workspace_slug, project_id, data)
client.work_items.retrieve(workspace_slug, project_id, work_item_id)
client.work_items.update(workspace_slug, project_id, work_item_id, data)
client.work_items.delete(workspace_slug, project_id, work_item_id)
client.work_items.list(workspace_slug, project_id, params)

# Search work items
client.work_items.search(workspace_slug, query, params)

# Sub-resources
client.work_items.comments      # Work item comments
client.work_items.attachments   # Work item attachments
client.work_items.links         # Work item links
client.work_items.relations     # Work item relations
client.work_items.activities    # Work item activities
client.work_items.work_logs     # Work item work logs
```

#### Projects

```python
client.projects.create(workspace_slug, data)
client.projects.retrieve(workspace_slug, project_id)
client.projects.update(workspace_slug, project_id, data)
client.projects.delete(workspace_slug, project_id)
client.projects.list(workspace_slug, params)
client.projects.get_worklog_summary(workspace_slug, project_id)
client.projects.get_members(workspace_slug, project_id, params)
```

#### Users

```python
client.users.retrieve(user_id)
client.users.list(params)
client.users.get_me()
client.users.upload_asset(data)
```

#### Workspaces

```python
client.workspaces.get_members(workspace_slug, params)
```

### Project Management Resources

#### Cycles

```python
client.cycles.create(workspace_slug, project_id, data)
client.cycles.retrieve(workspace_slug, project_id, cycle_id)
client.cycles.update(workspace_slug, project_id, cycle_id, data)
client.cycles.delete(workspace_slug, project_id, cycle_id)
client.cycles.list(workspace_slug, project_id, params)
client.cycles.list_archived(workspace_slug, project_id, params)
client.cycles.add_work_items(workspace_slug, project_id, cycle_id, data)
client.cycles.remove_work_item(workspace_slug, project_id, cycle_id, work_item_id)
client.cycles.list_work_items(workspace_slug, project_id, cycle_id, params)
client.cycles.transfer_work_items(workspace_slug, project_id, cycle_id, data)
client.cycles.archive(workspace_slug, project_id, cycle_id)
client.cycles.unarchive(workspace_slug, project_id, cycle_id)
```

#### Modules

```python
client.modules.create(workspace_slug, project_id, data)
client.modules.retrieve(workspace_slug, project_id, module_id)
client.modules.update(workspace_slug, project_id, module_id, data)
client.modules.delete(workspace_slug, project_id, module_id)
client.modules.list(workspace_slug, project_id, params)
client.modules.list_archived(workspace_slug, project_id, params)
client.modules.add_work_items(workspace_slug, project_id, module_id, data)
client.modules.remove_work_item(workspace_slug, project_id, module_id, work_item_id)
client.modules.list_work_items(workspace_slug, project_id, module_id, params)
client.modules.archive(workspace_slug, project_id, module_id)
client.modules.unarchive(workspace_slug, project_id, module_id)
```

#### States

```python
client.states.create(workspace_slug, project_id, data)
client.states.retrieve(workspace_slug, project_id, state_id)
client.states.update(workspace_slug, project_id, state_id, data)
client.states.delete(workspace_slug, project_id, state_id)
client.states.list(workspace_slug, project_id, params)
```

#### Labels

```python
client.labels.create(workspace_slug, project_id, data)
client.labels.retrieve(workspace_slug, project_id, label_id)
client.labels.update(workspace_slug, project_id, label_id, data)
client.labels.delete(workspace_slug, project_id, label_id)
client.labels.list(workspace_slug, project_id, params)
```

### Work Item Management

#### Work Item Types

```python
client.work_item_types.create(workspace_slug, project_id, data)
client.work_item_types.retrieve(workspace_slug, project_id, work_item_type_id)
client.work_item_types.update(workspace_slug, project_id, work_item_type_id, data)
client.work_item_types.delete(workspace_slug, project_id, work_item_type_id)
client.work_item_types.list(workspace_slug, project_id, params)
```

#### Work Item Properties

```python
client.work_item_properties.create(workspace_slug, project_id, type_id, data)
client.work_item_properties.retrieve(workspace_slug, project_id, type_id, property_id)
client.work_item_properties.update(workspace_slug, project_id, type_id, property_id, data)
client.work_item_properties.delete(workspace_slug, project_id, type_id, property_id)
client.work_item_properties.list(workspace_slug, project_id, type_id, params)
```

#### Work Item Property Options

```python
client.work_item_property_options.list(workspace_slug, project_id, property_id, params)
client.work_item_property_options.retrieve(workspace_slug, project_id, property_id, option_id)
client.work_item_property_options.create(workspace_slug, project_id, property_id, data)
client.work_item_property_options.update(workspace_slug, project_id, property_id, option_id, data)
client.work_item_property_options.delete(workspace_slug, project_id, property_id, option_id)
```

#### Work Item Property Values

```python
client.work_item_property_values.list(workspace_slug, project_id, work_item_id, params)
client.work_item_property_values.retrieve(workspace_slug, project_id, work_item_id, value_id)
client.work_item_property_values.create(workspace_slug, project_id, work_item_id, property_id, data)
client.work_item_property_values.update(workspace_slug, project_id, work_item_id, value_id, data)
client.work_item_property_values.delete(workspace_slug, project_id, work_item_id, value_id)
```

### Additional Resources

#### Epics

```python
client.epics.list(workspace_slug, project_id, params)
client.epics.retrieve(workspace_slug, project_id, epic_id, params)
```

#### Intake

```python
client.intake.list(workspace_slug, project_id, params)
client.intake.retrieve(workspace_slug, project_id, intake_issue_id, params)
client.intake.create(workspace_slug, project_id, data)
client.intake.update(workspace_slug, project_id, intake_issue_id, data)
client.intake.delete(workspace_slug, project_id, intake_issue_id)
```

#### Pages

```python
client.pages.retrieve_workspace_page(workspace_slug, page_id, params)
client.pages.retrieve_project_page(workspace_slug, project_id, page_id, params)
client.pages.list_workspace_pages(workspace_slug, params)
client.pages.list_project_pages(workspace_slug, project_id, params)
```

#### Members

```python
client.members.list_project_members(workspace_slug, project_id, params)
client.members.add_to_project(workspace_slug, project_id, user_id)
client.members.remove_from_project(workspace_slug, project_id, user_id)
```

#### Customers

```python
client.customers.list(workspace_slug, params)
client.customers.retrieve(workspace_slug, customer_id, params)
client.customers.create(workspace_slug, data)
client.customers.update(workspace_slug, customer_id, data)
client.customers.delete(workspace_slug, customer_id)

# Sub-resources
client.customers.properties  # Customer properties
client.customers.requests    # Customer requests
```

## Data Models

The SDK provides comprehensive Pydantic models for all API operations:

### Core Models

- `WorkItem`, `CreateWorkItem`, `UpdateWorkItem`
- `Project`, `CreateProject`, `UpdateProject`
- `UserLite`, `UserAssetUploadRequest`
- `State`, `CreateState`, `UpdateState`
- `Label`, `CreateLabel`, `UpdateLabel`
- `Cycle`, `CreateCycle`, `UpdateCycle`
- `Module`, `CreateModule`, `UpdateModule`

### Query Parameters

- `BaseQueryParams` - Base query parameters
- `PaginatedQueryParams` - Pagination support
- `WorkItemQueryParams` - Work item specific queries
- `RetrieveQueryParams` - Retrieve operations

### Response Models

- `PaginatedWorkItemResponse`
- `PaginatedProjectResponse`
- `PaginatedCycleResponse`
- `PaginatedModuleResponse`
- And many more paginated response types

## Error Handling

The SDK provides comprehensive error handling with specific exception types:

```python
from plane.errors import PlaneError, ConfigurationError, HttpError

try:
    client = PlaneClient(base_url="https://api.plane.so", api_key="invalid")
except ConfigurationError as e:
    print(f"Configuration error: {e}")

try:
    work_item = client.work_items.retrieve("workspace", "project", "invalid-id")
except HttpError as e:
    print(f"HTTP error {e.status_code}: {e}")
    print(f"Response: {e.response}")
```

### Error Types

- `PlaneError` - Base exception class
- `ConfigurationError` - Invalid client configuration
- `HttpError` - HTTP request/response errors

## Configuration

### Basic Configuration

```python
from plane.client import PlaneClient

client = PlaneClient(
    base_url="https://api.plane.so",
    api_key="your-api-key"
)
```

### Advanced Configuration

```python
from plane.config import Configuration, RetryConfig
from plane.client import PlaneClient

# Custom retry configuration
retry_config = RetryConfig(
    total=5,
    backoff_factor=0.5,
    status_forcelist=(429, 500, 502, 503, 504)
)

# Custom configuration
config = Configuration(
    base_path="https://api.plane.so",
    api_key="your-api-key",
    timeout=60.0,
    retry=retry_config
)

client = PlaneClient(config=config)
```

### Configuration Options

- `base_path` - API base URL
- `api_key` - API key for authentication
- `access_token` - Access token for authentication
- `timeout` - Request timeout (default: 30.0 seconds)
- `retry` - Retry configuration

## Examples

### Creating a Complete Workflow

```python
from plane.client import PlaneClient
from plane.models.schemas import (
    CreateProject, CreateWorkItem, CreateState, CreateLabel,
    WorkItemQueryParams
)

client = PlaneClient(
    base_url="https://api.plane.so",
    api_key="your-api-key"
)

# Create a project
project = client.projects.create(
    workspace_slug="my-workspace",
    data=CreateProject(
        name="My New Project",
        description="A project created with the Python SDK",
        identifier="MNP"
    )
)

# Create a state
state = client.states.create(
    workspace_slug="my-workspace",
    project_id=project.id,
    data=CreateState(
        name="In Progress",
        color="#3b82f6",
        group="started"
    )
)

# Create a label
label = client.labels.create(
    workspace_slug="my-workspace",
    project_id=project.id,
    data=CreateLabel(
        name="Bug",
        color="#ef4444"
    )
)

# Create a work item
work_item = client.work_items.create(
    workspace_slug="my-workspace",
    project_id=project.id,
    data=CreateWorkItem(
        name="Fix authentication bug",
        description_html="<p>Fix the authentication issue in the login flow</p>",
        priority="high",
        state=state.id,
        labels=[label.id]
    )
)

# List work items with filtering
work_items = client.work_items.list(
    workspace_slug="my-workspace",
    project_id=project.id,
    params=WorkItemQueryParams(
        expand="assignees,labels,state",
        order_by="-created_at",
        per_page=20
    )
)

print(f"Created work item: {work_item.name}")
print(f"Total work items: {work_items.total_results}")
```

### Working with Cycles

```python
from plane.models.schemas import CreateCycle, AddWorkItemsToCycleRequest

# Create a cycle
cycle = client.cycles.create(
    workspace_slug="my-workspace",
    project_id=project.id,
    data=CreateCycle(
        name="Sprint 1",
        description="First sprint of the project",
        start_date="2024-01-01",
        end_date="2024-01-15",
        owned_by="user-id"
    )
)

# Add work items to cycle
client.cycles.add_work_items(
    workspace_slug="my-workspace",
    project_id=project.id,
    cycle_id=cycle.id,
    data=AddWorkItemsToCycleRequest(issues=[work_item.id])
)

# List cycle work items
cycle_work_items = client.cycles.list_work_items(
    workspace_slug="my-workspace",
    project_id=project.id,
    cycle_id=cycle.id
)
```

### Working with Comments and Attachments

```python
from plane.models.schemas import CreateWorkItemComment

# Add a comment
comment = client.work_items.comments.create(
    workspace_slug="my-workspace",
    project_id=project.id,
    work_item_id=work_item.id,
    data=CreateWorkItemComment(
        comment_html="<p>This is a comment on the work item</p>",
        access="INTERNAL"
    )
)

# List comments
comments = client.work_items.comments.list(
    workspace_slug="my-workspace",
    project_id=project.id,
    work_item_id=work_item.id
)

# Upload an attachment
attachment = client.work_items.attachments.create(
    workspace_slug="my-workspace",
    project_id=project.id,
    work_item_id=work_item.id,
    data={
        "name": "screenshot.png",
        "type": "image/png",
        "size": 1024
    }
)
```

## Requirements

- Python 3.10+
- requests >= 2.31.0
- pydantic >= 2.4.0

## Development

### Setup

```bash
git clone <repository-url>
cd plane-python-sdk
pip install -e .
```

### Running Tests

```bash
pytest
```

### Code Quality

The project uses:

- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking
- **Pytest** for testing

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:

- GitHub Issues: [Repository Issues]
- Documentation: [Plane Documentation]
- Email: dev@plane.so

---

**Note**: This SDK is designed to work with Plane's REST API. Make sure you have the appropriate API credentials and permissions for the operations you're trying to perform.
