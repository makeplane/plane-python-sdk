# Plane Python SDK

A comprehensive, type-annotated Python SDK for interacting with the Plane API. This SDK provides a clean, modern interface for all Plane API operations, following Python best practices with full type safety and Pydantic v2 integration.

## Features

- 🚀 **Type-Safe**: Full type annotations with Pydantic v2 models
- 🔧 **Modern Python**: Built for Python 3.10+ with modern typing idioms
- 🛡️ **Error Handling**: Comprehensive error types and exception handling
- 🔄 **Retry Logic**: Built-in retry mechanism with configurable backoff
- 📦 **Resource-Based**: Clean resource-based API organization
- 🎯 **Comprehensive**: Support for all major Plane API endpoints
- ⚡ **Synchronous**: Uses `requests` with connection pooling

## Breaking Changes (v0.2.0 vs v0.1.x)

This SDK (v0.2.0) replaces the v0.1.x OpenAPI-generated client and introduces intentional breaking changes for a cleaner, type-safe developer experience.

- Authentication and client

  - New `PlaneClient(base_url, api_key | access_token)` replaces OpenAPI `Configuration`/`ApiClient` usage
  - Exactly one of `api_key` or `access_token` is required; providing both raises a `ConfigurationError`
  - `base_url` should NOT include `/api/v1`; the SDK appends `/api/v1` automatically

- HTTP headers

  - API key header standardized to `X-Api-Key`; access tokens use `Authorization: Bearer <token>`

- Resource paths and naming

  - All paths use `work-items` instead of v0.1.x `issues`
  - Sub-resources are grouped under `client.work_items.<subresource>`

- Method names

  - Methods are standardized across resources: `list`, `create`, `retrieve`, `update`, `delete`
  - Replaces verbose, OpenAPI-generated method names

- Models and DTOs

  - Uses Pydantic v2 with: response models `extra="allow"`; Create*/Update* DTOs `extra="ignore"`
  - Separate DTOs for create/update: `Create*` and `Update*`
  - Field naming is normalized

- Pagination shape

  - Paginated responses now expose: `results`, `total_count`, `next_page_number`, `prev_page_number`
  - This replaces v0.1.x shapes that included different field names

- Query parameters

  - Typed query params via models like `WorkItemQueryParams` and `RetrieveQueryParams`
  - Common fields include `per_page`, `page`, `order_by`, `expand`

- Errors

  - Raises `HttpError(message, status_code, response)` on non-2xx responses
  - Configuration validation errors raise `ConfigurationError`

- Imports and organization

  - Import models from `plane.models.<resource>`
  - No OpenAPI `*Api` classes; use resource objects from `PlaneClient`

- Trailing slashes
  - All endpoints include trailing `/` by design; the SDK enforces this consistently

Migration example (v0.1.x → v0.2.0):

```python
# v0.1.x (OpenAPI-generated)
from plane import Configuration, ApiClient
from plane.apis import WorkItemsApi

cfg = Configuration(host="https://api.plane.so")
cfg.api_key['X-API-Key'] = "<api-key>"
api = WorkItemsApi(ApiClient(cfg))
api.list_work_items(slug, project_id=project_id)

# v0.2.0 (this SDK)
from plane.client import PlaneClient
from plane.models.query_params import WorkItemQueryParams

client = PlaneClient(base_url="https://api.plane.so", api_key="<api-key>")
client.work_items.list(
    workspace_slug=slug,
    project_id=project_id,
    params=WorkItemQueryParams(per_page=20, order_by="-created_at")
)
```

## Installation

```bash
pip install plane-sdk
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

### OAuth Authentication

The SDK also supports OAuth 2.0 authentication for more advanced use cases:

```python
from plane import OAuthClient

# Initialize OAuth client
oauth_client = OAuthClient(
    base_url="https://api.plane.so",
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Authorization Code Flow (for web applications)
# Step 1: Get authorization URL
auth_url = oauth_client.get_authorization_url(
    redirect_uri="https://your-app.com/callback",
    scope="read write",
    state="random_state_string"
)

# Step 2: Exchange authorization code for token
token = oauth_client.exchange_code(
    code="authorization_code_from_callback",
    redirect_uri="https://your-app.com/callback"
)

# Step 3: Use the access token
client = PlaneClient(
    base_url="https://api.plane.so",
    access_token=token.access_token
)

# Client Credentials Flow (for server-to-server)
token = oauth_client.get_client_credentials_token(
    scope="read write",
    app_installation_id="optional_workspace_app_installation_id"
)

# Refresh expired tokens
new_token = oauth_client.refresh_token(token.refresh_token)

# Revoke tokens
oauth_client.revoke_token(token.access_token)
```

For detailed OAuth examples, see [examples/oauth_example.py](examples/oauth_example.py).

### Basic Usage

```python
# List projects in a workspace
projects = client.projects.list("my-workspace")

# Create a work item
from plane.models.work_items import CreateWorkItem

work_item = client.work_items.create(
    workspace_slug="my-workspace",
    project_id="project-id",
    data=CreateWorkItem(name="New task", state_id="state-id")
)

# Retrieve a work item with parameters
from plane.models.query_params import RetrieveQueryParams

work_item = client.work_items.retrieve(
    workspace_slug="my-workspace",
    project_id="project-id",
    work_item_id="work-item-id",
    params=RetrieveQueryParams(expand="assignees,labels,state")
)

# List work items with pagination and filtering
from plane.models.query_params import WorkItemQueryParams

work_items = client.work_items.list(
    workspace_slug="my-workspace",
    project_id="project-id",
    params=WorkItemQueryParams(per_page=50, order_by="-created_at")
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
client.users              # User management
client.workspaces        # Workspace operations
client.projects          # Project management
client.work_items        # Work item operations
client.cycles            # Cycle management
client.modules           # Module management
client.labels            # Label management
client.states            # State/workflow management
client.work_item_types   # Work item type management
client.work_item_properties  # Custom properties
client.epics             # Epic management
client.intake            # Intake management
client.pages             # Page management
client.customers         # Customer management
client.teamspaces        # Teamspace management
client.stickies         # Sticky management
client.initiatives      # Initiative management
```

### Resource Organization

All API resources extend a shared `BaseResource` class that handles:

- HTTP request/response logic
- Authentication headers
- Error handling and retry logic
- URL building with proper path formatting

### Type Safety

The SDK uses Pydantic v2 models for all data structures:

- Request models
- Response models
- Query parameter models

Note: Response models are configured with `extra="allow"` to be forward-compatible with new fields. Create*/Update* DTOs and query parameter models use `extra="ignore"`.

## Available Resources

### Core Resources

#### Users

```python
# Get current user
me = client.users.get_me()

# Retrieve a specific user
user = client.users.retrieve(user_id)

# List all users
users = client.users.list()
```

#### Workspaces

```python
# Get workspace members
members = client.workspaces.get_members(workspace_slug)
```

### Project Management

#### Projects

```python
# Create a project
from plane.models.projects import CreateProject

project = client.projects.create(
    workspace_slug="my-workspace",
    data=CreateProject(
        name="My Project",
        identifier="MP",
        description="Project description"
    )
)

# List projects
projects = client.projects.list(workspace_slug="my-workspace")

# Retrieve a project
project = client.projects.retrieve(workspace_slug, project_id)

# Update a project
from plane.models.projects import UpdateProject

project = client.projects.update(
    workspace_slug, project_id,
    data=UpdateProject(name="Updated Name")
)

# Delete a project
client.projects.delete(workspace_slug, project_id)

# Get worklog summary
worklog_summary = client.projects.get_worklog_summary(workspace_slug, project_id)

# Get project members
members = client.projects.get_members(workspace_slug, project_id)
```

#### Work Items

```python
# Create a work item
from plane.models.work_items import CreateWorkItem

work_item = client.work_items.create(
    workspace_slug="my-workspace",
    project_id="project-id",
    data=CreateWorkItem(
        name="Fix login bug",
        description_html="<p>Fix the login issue</p>",
        state_id="state-id",
        priority="high"
    )
)

# Retrieve a work item
from plane.models.query_params import RetrieveQueryParams

work_item = client.work_items.retrieve(
    workspace_slug, project_id, work_item_id,
    params=RetrieveQueryParams(expand="assignees,labels,state")
)

# List work items
from plane.models.query_params import WorkItemQueryParams

work_items = client.work_items.list(
    workspace_slug, project_id,
    params=WorkItemQueryParams(per_page=50, order_by="-created_at")
)

# Update a work item
from plane.models.work_items import UpdateWorkItem

work_item = client.work_items.update(
    workspace_slug, project_id, work_item_id,
    data=UpdateWorkItem(priority="low", state_id="new-state-id")
)

# Delete a work item
client.work_items.delete(workspace_slug, project_id, work_item_id)

# Search work items
results = client.work_items.search(
    workspace_slug, project_id,
    query="bug fix"
)
```

#### Work Item Sub-Resources

```python
# Comments
comments = client.work_items.comments.list(workspace_slug, project_id, work_item_id)
comment = client.work_items.comments.create(workspace_slug, project_id, work_item_id, data)
comment = client.work_items.comments.retrieve(workspace_slug, project_id, work_item_id, comment_id)
comment = client.work_items.comments.update(workspace_slug, project_id, work_item_id, comment_id, data)
client.work_items.comments.delete(workspace_slug, project_id, work_item_id, comment_id)

# Attachments
attachments = client.work_items.attachments.list(workspace_slug, project_id, work_item_id)
attachment = client.work_items.attachments.create(workspace_slug, project_id, work_item_id, data)
attachment = client.work_items.attachments.retrieve(workspace_slug, project_id, work_item_id, attachment_id)
client.work_items.attachments.delete(workspace_slug, project_id, work_item_id, attachment_id)

# Links
links = client.work_items.links.list(workspace_slug, project_id, work_item_id)
link = client.work_items.links.create(workspace_slug, project_id, work_item_id, data)
link = client.work_items.links.retrieve(workspace_slug, project_id, work_item_id, link_id)
link = client.work_items.links.update(workspace_slug, project_id, work_item_id, link_id, data)
client.work_items.links.delete(workspace_slug, project_id, work_item_id, link_id)

# Relations
relations = client.work_items.relations.list(workspace_slug, project_id, work_item_id)
relation = client.work_items.relations.create(workspace_slug, project_id, work_item_id, data)

# Activities
activities = client.work_items.activities.list(workspace_slug, project_id, work_item_id)

# Work Logs
work_logs = client.work_items.work_logs.list(workspace_slug, project_id, work_item_id)
work_log = client.work_items.work_logs.create(workspace_slug, project_id, work_item_id, data)
work_log = client.work_items.work_logs.retrieve(workspace_slug, project_id, work_item_id, work_log_id)
work_log = client.work_items.work_logs.update(workspace_slug, project_id, work_item_id, work_log_id, data)
client.work_items.work_logs.delete(workspace_slug, project_id, work_item_id, work_log_id)
```

#### Cycles

```python
# Create a cycle
from plane.models.cycles import CreateCycle

cycle = client.cycles.create(
    workspace_slug, project_id,
    data=CreateCycle(
        name="Sprint 1",
        start_date="2024-01-01",
        end_date="2024-01-15",
        owned_by="user-id"
    )
)

# List cycles
cycles = client.cycles.list(workspace_slug, project_id)

# Retrieve a cycle
cycle = client.cycles.retrieve(workspace_slug, project_id, cycle_id)

# Update a cycle
from plane.models.cycles import UpdateCycle

cycle = client.cycles.update(
    workspace_slug, project_id, cycle_id,
    data=UpdateCycle(name="Updated Sprint")
)

# Delete a cycle
client.cycles.delete(workspace_slug, project_id, cycle_id)

# List archived cycles
archived = client.cycles.list_archived(workspace_slug, project_id)

# Add work items to cycle
from plane.models.cycles import AddWorkItemsToCycleRequest

client.cycles.add_work_items(
    workspace_slug, project_id, cycle_id,
    data=AddWorkItemsToCycleRequest(issues=[work_item_id])
)

# Remove work item from cycle
client.cycles.remove_work_item(workspace_slug, project_id, cycle_id, work_item_id)

# List work items in cycle
cycle_items = client.cycles.list_work_items(workspace_slug, project_id, cycle_id)

# Transfer work items between cycles
from plane.models.cycles import TransferCycleWorkItemsRequest

client.cycles.transfer_work_items(
    workspace_slug, project_id, cycle_id,
    data=TransferCycleWorkItemsRequest(new_cycle_id="other-cycle-id")
)

# Archive/unarchive cycles
client.cycles.archive(workspace_slug, project_id, cycle_id)
client.cycles.unarchive(workspace_slug, project_id, cycle_id)
```

#### Modules

```python
# Create a module
from plane.models.modules import CreateModule

module = client.modules.create(
    workspace_slug, project_id,
    data=CreateModule(name="Auth Module")
)

# List modules
modules = client.modules.list(workspace_slug, project_id)

# Retrieve a module
module = client.modules.retrieve(workspace_slug, project_id, module_id)

# Update a module
from plane.models.modules import UpdateModule

module = client.modules.update(
    workspace_slug, project_id, module_id,
    data=UpdateModule(name="Updated Module")
)

# Delete a module
client.modules.delete(workspace_slug, project_id, module_id)

# List archived modules
archived = client.modules.list_archived(workspace_slug, project_id)

# Add work items to module
from plane.models.modules import AddWorkItemsToModuleRequest

client.modules.add_work_items(
    workspace_slug, project_id, module_id,
    data=AddWorkItemsToModuleRequest(issues=[work_item_id])
)

# Remove work item from module
client.modules.remove_work_item(workspace_slug, project_id, module_id, work_item_id)

# List work items in module
module_items = client.modules.list_work_items(workspace_slug, project_id, module_id)

# Archive/unarchive modules
client.modules.archive(workspace_slug, project_id, module_id)
client.modules.unarchive(workspace_slug, project_id, module_id)
```

#### States

```python
# Create a state
from plane.models.states import CreateState

state = client.states.create(
    workspace_slug, project_id,
    data=CreateState(
        name="In Progress",
        color="#3b82f6",
        group="started"
    )
)

# List states
states = client.states.list(workspace_slug, project_id)

# Retrieve a state
state = client.states.retrieve(workspace_slug, project_id, state_id)

# Update a state
from plane.models.states import UpdateState

state = client.states.update(
    workspace_slug, project_id, state_id,
    data=UpdateState(name="Updated Status")
)

# Delete a state
client.states.delete(workspace_slug, project_id, state_id)
```

#### Labels

```python
# Create a label
from plane.models.labels import CreateLabel

label = client.labels.create(
    workspace_slug, project_id,
    data=CreateLabel(name="Bug", color="#ef4444")
)

# List labels
labels = client.labels.list(workspace_slug, project_id)

# Retrieve a label
label = client.labels.retrieve(workspace_slug, project_id, label_id)

# Update a label
from plane.models.labels import UpdateLabel

label = client.labels.update(
    workspace_slug, project_id, label_id,
    data=UpdateLabel(name="Updated Label")
)

# Delete a label
client.labels.delete(workspace_slug, project_id, label_id)
```

### Work Item Configuration

#### Work Item Types

```python
# Create a work item type
from plane.models.work_item_types import CreateWorkItemType

wit = client.work_item_types.create(
    workspace_slug, project_id,
    data=CreateWorkItemType(name="Story")
)

# List work item types
types = client.work_item_types.list(workspace_slug, project_id)

# Retrieve a work item type
wit = client.work_item_types.retrieve(workspace_slug, project_id, type_id)

# Update a work item type
from plane.models.work_item_types import UpdateWorkItemType

wit = client.work_item_types.update(
    workspace_slug, project_id, type_id,
    data=UpdateWorkItemType(name="Updated Type")
)

# Delete a work item type
client.work_item_types.delete(workspace_slug, project_id, type_id)
```

#### Work Item Properties

```python
# Create a property
from plane.models.work_item_properties import CreateWorkItemProperty

prop = client.work_item_properties.create(
    workspace_slug, project_id, work_item_type_id,
    data=CreateWorkItemProperty(name="Severity")
)

# List properties
properties = client.work_item_properties.list(workspace_slug, project_id, work_item_type_id)

# Retrieve a property
prop = client.work_item_properties.retrieve(workspace_slug, project_id, work_item_type_id, property_id)

# Update a property
from plane.models.work_item_properties import UpdateWorkItemProperty

prop = client.work_item_properties.update(
    workspace_slug, project_id, work_item_type_id, property_id,
    data=UpdateWorkItemProperty(name="Updated Property")
)

# Delete a property
client.work_item_properties.delete(workspace_slug, project_id, work_item_type_id, property_id)
```

### Additional Resources

#### Epics

```python
# List epics
epics = client.epics.list(workspace_slug, project_id)

# Retrieve an epic
epic = client.epics.retrieve(workspace_slug, project_id, epic_id)
```

#### Intake

```python
# Create intake issue
from plane.models.intake import CreateIntake

intake = client.intake.create(
    workspace_slug, project_id,
    data=CreateIntake(name="Customer request")
)

# List intake issues
intake_items = client.intake.list(workspace_slug, project_id)

# Retrieve intake issue
intake = client.intake.retrieve(workspace_slug, project_id, intake_id)

# Update intake issue
from plane.models.intake import UpdateIntake

intake = client.intake.update(
    workspace_slug, project_id, intake_id,
    data=UpdateIntake(status="completed")
)

# Delete intake issue
client.intake.delete(workspace_slug, project_id, intake_id)
```

#### Pages

```python
# List workspace pages
pages = client.pages.list_workspace_pages(workspace_slug)

# List project pages
pages = client.pages.list_project_pages(workspace_slug, project_id)

# Retrieve a workspace page
page = client.pages.retrieve_workspace_page(workspace_slug, page_id)

# Retrieve a project page
page = client.pages.retrieve_project_page(workspace_slug, project_id, page_id)
```

#### Customers

```python
# List customers
customers = client.customers.list(workspace_slug)

# Create a customer
from plane.models.customers import CreateCustomer

customer = client.customers.create(
    workspace_slug,
    data=CreateCustomer(name="Acme Inc")
)

# Retrieve a customer
customer = client.customers.retrieve(workspace_slug, customer_id)

# Update a customer
from plane.models.customers import UpdateCustomer

customer = client.customers.update(
    workspace_slug, customer_id,
    data=UpdateCustomer(name="Updated Name")
)

# Delete a customer
client.customers.delete(workspace_slug, customer_id)

# Customer properties
properties = client.customers.properties.list(workspace_slug, customer_id)
property = client.customers.properties.create(workspace_slug, customer_id, data)

# Customer requests
requests = client.customers.requests.list(workspace_slug, customer_id)
```

## Data Models

The SDK provides comprehensive Pydantic v2 models for all API operations.

### Query Parameters

- `BaseQueryParams` - Base query parameters
- `PaginatedQueryParams` - Pagination support (per_page, page)
- `WorkItemQueryParams` - Work item specific queries (expand, order_by, etc.)
- `RetrieveQueryParams` - Retrieve operations (expand, fields, etc.)

### Response Models

Paginated responses follow the pattern `Paginated<Resource>Response` and include:

- `results` - Array of resource objects
- `total_count` - Total number of results
- `next_page_number` - Next page number (if applicable)
- `prev_page_number` - Previous page number (if applicable)

## Error Handling

The SDK provides comprehensive error handling with specific exception types:

```python
from plane.errors import PlaneError, ConfigurationError, HttpError

# Configuration errors
try:
    client = PlaneClient(base_url="https://api.plane.so")
    # Missing both api_key and access_token
except ConfigurationError as e:
    print(f"Configuration error: {e}")

# HTTP errors
try:
    work_item = client.work_items.retrieve("workspace", "project", "invalid-id")
except HttpError as e:
    print(f"HTTP error {e.status_code}: {e}")
    print(f"Response: {e.response}")
```

### Error Types

- `PlaneError` - Base exception class with optional status_code
- `ConfigurationError` - Invalid client configuration (missing credentials or both auth methods provided)
- `HttpError` - HTTP request/response errors with status code and response body

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
    total=5,                                    # Number of retries
    backoff_factor=0.5,                         # Backoff multiplier
    status_forcelist=(429, 500, 502, 503, 504) # Retry on these status codes
)

# Create client with custom config
client = PlaneClient(
    base_url="https://api.plane.so",
    api_key="your-api-key",
    timeout=60.0,                               # Request timeout in seconds
    retry=retry_config                          # Optional retry config
)
```

### Configuration Options

| Option         | Type                           | Default  | Description                     |
| -------------- | ------------------------------ | -------- | ------------------------------- |
| `base_url`     | `str`                          | Required | API base URL                    |
| `api_key`      | `str`                          | Optional | API key for authentication      |
| `access_token` | `str`                          | Optional | Access token for authentication |
| `timeout`      | `float \| tuple[float, float]` | `30.0`   | Request timeout in seconds      |
| `retry`        | `RetryConfig`                  | None     | Retry configuration             |

**Note**: Provide exactly one of `api_key` or `access_token`.

## Examples

### Complete Workflow Example

```python
from plane.client import PlaneClient
from plane.models.projects import CreateProject
from plane.models.work_items import CreateWorkItem
from plane.models.states import CreateState
from plane.models.labels import CreateLabel
from plane.models.query_params import WorkItemQueryParams

client = PlaneClient(
    base_url="https://api.plane.so",
    api_key="your-api-key"
)

# Create a project
project = client.projects.create(
    workspace_slug="my-workspace",
    data=CreateProject(
        name="My New Project",
        identifier="MNP",
        description="A project created with the Python SDK"
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
    data=CreateLabel(name="Bug", color="#ef4444")
)

# Create a work item
work_item = client.work_items.create(
    workspace_slug="my-workspace",
    project_id=project.id,
    data=CreateWorkItem(
        name="Fix authentication bug",
        description_html="<p>Fix the authentication issue in the login flow</p>",
        priority="high",
        state_id=state.id,
        labels=[label.id]
    )
)

# List work items with filters
work_items = client.work_items.list(
    workspace_slug="my-workspace",
    project_id=project.id,
    params=WorkItemQueryParams(per_page=20, order_by="-created_at")
)

print(f"Created work item: {work_item.name}")
print(f"Total work items: {len(work_items.results)}")
```

### Working with Cycles

```python
from plane.models.cycles import CreateCycle, AddWorkItemsToCycleRequest

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

print(f"Cycle: {cycle.name}")
print(f"Work items in cycle: {len(cycle_work_items.results)}")
```

### Working with Comments and Attachments

```python
from plane.models.work_items import CreateWorkItemComment

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

print(f"Total comments: {len(comments.results)}")

# Upload an attachment
attachment = client.work_items.attachments.create(
    workspace_slug="my-workspace",
    project_id=project.id,
    work_item_id=work_item.id,
    data={
        "asset": "file",  # URL to file or file path
        "attributes": {"name": "screenshot.png"}
    }
)

print(f"Attachment ID: {attachment.id}")
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
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_work_items.py

# Run with coverage
pytest --cov=plane tests/
```

### Code Quality

The project uses:

- **Black** for code formatting
- **Ruff** for linting (rules: E, F, I, UP, B)
- **MyPy** for type checking
- **Pytest** for testing

Run pre-commit checks:

```bash
pre-commit run --all-files
```

### Project Structure

```
plane-python-sdk/
├── plane/
│   ├── __init__.py
│   ├── client.py              # Main PlaneClient
│   ├── config.py              # Configuration classes
│   ├── api/                   # API resource classes
│   │   ├── base_resource.py   # Base class for all resources
│   │   ├── work_items/        # Work item sub-resources
│   │   ├── work_item_properties/
│   │   ├── customers/
│   │   └── ...
│   ├── models/                # Pydantic models
│   │   ├── work_items.py
│   │   ├── projects.py
│   │   ├── query_params.py
│   │   ├── enums.py
│   │   └── ...
│   └── errors/                # Exception classes
│       └── errors.py
├── tests/
│   ├── unit/                  # Unit tests
│   └── scripts/               # Integration test scripts
├── pyproject.toml
├── README.md
└── requirements.txt
```

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:

- GitHub Issues: [Repository Issues]
- Documentation: [Plane Documentation](https://docs.plane.so)
- Email: dev@plane.so

---

**Note**: This SDK is designed to work with Plane's REST API. Make sure you have the appropriate API credentials and permissions for the operations you're trying to perform.
