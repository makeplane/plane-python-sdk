# Plane Python SDK Examples

This directory contains practical examples demonstrating how to use the Plane Python SDK.

## Prerequisites

Before running these examples, ensure you have:

1. **Installed the Plane Python SDK:**

```bash
pip install plane-sdk
```

2. **Set up your environment variables:**

```bash
export PLANE_BASE_URL="https://api.plane.so"
export PLANE_API_KEY="your-api-key"
export WORKSPACE_SLUG="your-workspace-slug"
```

See [SETUP.md](SETUP.md) for detailed setup instructions.

## Examples

### 1. Project Setup (`setup_project.py`)

Sets up a complete project with all necessary configurations:

- Creates a new project
- Creates work item types (Bug, Feature, Task, Story)
- Creates workflow states (Backlog, To Do, In Progress, In Review, Done, Cancelled)
- Creates labels for categorization

**Run:**

```bash
python examples/setup_project.py
```

**Use this when:**

- Starting a new project
- You need to configure work item types, states, and labels
- Setting up a standardized project structure

### 2. Create Work Items (`create_work_items.py`)

Creates a basic project and populates it with work items:

- Creates a simple project
- Sets up basic states (To Do, In Progress, Done)
- Creates a few labels
- Creates multiple work items with different priorities
- Lists all work items in the project

**Run:**

```bash
python examples/create_work_items.py
```

**Use this when:**

- You want a quick project setup
- You need to create and track work items
- Getting started with the SDK

## Quick Start

1. **Set up environment variables** (see [SETUP.md](SETUP.md)):

```bash
export PLANE_BASE_URL="https://api.plane.so"
export PLANE_API_KEY="your-api-key"
export WORKSPACE_SLUG="your-workspace-slug"
```

2. **Run an example:**

```bash
# Full project setup with types, states, and labels
python examples/setup_project.py

# Or create a simple project with work items
python examples/create_work_items.py
```

## Common Usage Patterns

### Initialize the Client

```python
import os
from plane.client import PlaneClient

client = PlaneClient(
    base_url=os.environ["PLANE_BASE_URL"],
    api_key=os.environ["PLANE_API_KEY"]
)
```

### Create a Project

```python
from plane.models.projects import CreateProject

project = client.projects.create(
    workspace_slug="my-workspace",
    data=CreateProject(
        name="My Project",
        identifier="MP",
        description="Project description"
    )
)
```

### Create States

```python
from plane.models.states import CreateState

state = client.states.create(
    workspace_slug="my-workspace",
    project_id=project.id,
    data=CreateState(
        name="In Progress",
        group="started",
        color="#f59e0b"
    )
)
```

### Create Work Items

```python
from plane.models.work_items import CreateWorkItem

work_item = client.work_items.create(
    workspace_slug="my-workspace",
    project_id=project.id,
    data=CreateWorkItem(
        name="Fix bug",
        description_html="<p>Description here</p>",
        state_id=state.id,
        priority="high"
    )
)
```

## Error Handling

Always handle potential errors when using the SDK:

```python
from plane.errors import HttpError, ConfigurationError

try:
    project = client.projects.create(workspace_slug, data=project_data)
except HttpError as e:
    print(f"HTTP error {e.status_code}: {e}")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

## Getting Help

- **Setup issues?** See [SETUP.md](SETUP.md)
- **SDK documentation:** [../README.md](../README.md)
- **API documentation:** https://docs.plane.so
- **Support:** dev@plane.so

## Next Steps

After running the examples:

1. Explore the [SDK documentation](../README.md) for more features
2. Check the [Plane API documentation](https://docs.plane.so) for details
3. Build your own integrations using these examples as templates
