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

## API v2

`client.v2` reaches the v2 surface. v1 resources on the client are unchanged.

**This is a migration in progress.** Roughly 85 of the ~120 v2 resource groups are
still on an older, pre-migration shape and are not reachable through `client.v2` yet
(a later release wires them in). What follows documents only what is reachable
today: `states`, `labels`, `projects`, `work_items` (with `comments`), `workspaces`,
`wiki.pages`, `features` and `releases.labels`. Notably, `wiki.collections` is *not*
wired yet — `Collections` itself hasn't been migrated — so `client.v2.workspaces.wiki`
only has `.pages`.

The bound-locator chain from earlier releases (`client.v2.workspace(slug).project(key)`)
is **gone**. There are two ways to reach a resource now:

### 1. The flat path

A static tree, reached by plain attribute access. Read it left to right: every
segment that names an actual resource consumes one URL path id (a workspace slug,
a project key, a work item identifier, ...); a segment that only *groups* children
(`wiki`) consumes none.

```python
from plane import PlaneClient
from plane.models.v2 import CreateState

client = PlaneClient(base_url="https://api.plane.so", api_key="...")

client.v2.users.me()
client.v2.workspaces.retrieve("acme")
client.v2.workspaces.projects.states.list("acme", "ENG", fields=["id", "name"])
client.v2.workspaces.projects.work_items.comments.list("acme", "ENG", "ENG-12")
client.v2.workspaces.wiki.pages.list("acme")   # `wiki` groups, consumes no id
client.v2.workspaces.features.get("acme")      # singleton: no primary key at all

client.v2.workspaces.projects.states.create(
    "acme", "ENG", CreateState(name="In Review", color="#4ECDC4")
)
```

Path ids are plain positional-or-keyword parameters, so they can be passed by
keyword too — handy when a call's own arguments would otherwise read ambiguously:

```python
client.v2.workspaces.projects.states.list(slug="acme", project="ENG")
```

### 2. Loaded rows

A resource with children (today, that's `projects` and `work_items`) doesn't just
hand back a bare pydantic model from `retrieve`/`list`/`iterate` — it hands back a
row that carries its own data *and* already knows where it lives, so the row's own
children are reached with none of the ids repeated:

```python
p = client.v2.workspaces.projects.retrieve("acme", "ENG")
p.name
p.states.list()                                    # no "acme", "ENG" to repeat
item = p.work_items.retrieve("ENG-12")
item.comments.list()                                # same, one level deeper
```

`list` and `iterate` yield these same navigable rows, not bare pydantic models —
`for project in client.v2.workspaces.projects.iterate("acme"): project.states.list()`
works with no extra plumbing. Resources without children today (`states`, `labels`,
`workspaces`, `wiki.pages`, `features`, `releases.labels`) still return plain
pydantic models — the `Loaded` mixin (`plane/api/v2/_kernel/loaded.py`) is generic
and every migrated resource with children will pick it up the same way.

### Sparse responses raise, they don't lie

Every read field except `id` is optional at the model level, because `?fields=`
and collection deferral can both omit any field the server would otherwise send.
On a Loaded row, *reading* a field the request didn't ask for raises
`FieldNotRequested` instead of silently returning `None` — a `None` you get back is
a real null, not a sign the data was never fetched:

```python
from plane.api.v2._kernel.errors import FieldNotRequested

p = client.v2.workspaces.projects.retrieve("acme", "ENG", fields=["id"])
p.name          # raises FieldNotRequested -- "name" was not requested
```

(`FieldNotRequested` isn't re-exported from `plane.api.v2` yet, unlike the other
v2 error types below — a follow-on task will fold it into the public export list.)

### Typing is not decorative

Field names, `order_by` values and filter keyword names are all generated
`Literal`/`TypedDict` types (from `plane/api/v2/_generated/constants.py`, produced
from the api_v2 OpenAPI golden), and the package ships a `py.typed` marker so a
type checker actually reads them. A typo in a filter keyword is a `mypy` error,
not a runtime surprise:

```python
# mypy rejects this: "not_a_filter" isn't in StatesListFilters
client.v2.workspaces.projects.states.list("acme", "ENG", not_a_filter="x")
```

### What else is wired

`releases.labels` sits on `workspaces` too (`client.v2.workspaces.releases.labels`)
and, being both a catalog *and* a membership bridge, additionally exposes
`add(release_id, ids)`/`remove(release_id, ids)` to attach/detach existing labels
from a specific release — parent id first, then 1..100 ids; an empty list, or more
than 100, raises `ValueError` before any request is sent.

### Errors

Errors from `client.v2` calls raise `PlaneAPIError` (RFC 9457 problem detail —
`.status`, `.type`, `.code`, `.detail`, `.errors`), and `find_by_name` raises
`NoMatchFound` or `MultipleMatchesFound` when it can't resolve to exactly one row.
All three, plus `FieldError` (the shape of one entry in `.errors`), are re-exported
from both `plane.api.v2` and the top-level `plane` package:

```python
from plane.api.v2 import MultipleMatchesFound, NoMatchFound, PlaneAPIError

# or, equivalently:
# from plane import MultipleMatchesFound, NoMatchFound, PlaneAPIError

try:
    todo = client.v2.workspaces.projects.states.find_by_name("acme", "ENG", "Todo")
except NoMatchFound:
    ...
except MultipleMatchesFound:
    ...

try:
    client.v2.workspaces.projects.states.create("acme", "ENG", CreateState(name="", color="#fff"))
except PlaneAPIError as e:
    print(e.status, e.code, e.detail)
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

# Filter members (all filters combine with AND; role_slug is exact, text fields
# match case-insensitive contains)
from plane.models.query_params import MemberQueryParams, MemberListQueryParams

admins = client.workspaces.get_members(
    workspace_slug,
    params=MemberQueryParams(role_slug="admin", is_active=True),
)

# Paginated "lite" list — follow next_cursor until next_page_results is False
paginated_members = client.workspaces.get_members_lite(
    workspace_slug,
    params=MemberListQueryParams(per_page=1000),
)
all_members = list(paginated_members.results)
while paginated_members.next_page_results:
    paginated_members = client.workspaces.get_members_lite(
        workspace_slug,
        params=MemberListQueryParams(per_page=1000, cursor=paginated_members.next_cursor),
    )
    all_members.extend(paginated_members.results)

# Project-role distribution — member counts per role across all active
# (non-archived) projects in the workspace (built-in + custom roles)
distribution = client.workspaces.get_project_role_distribution(workspace_slug)
print(distribution.total_memberships, distribution.total_distinct_members)
for role in distribution.roles:
    print(role.slug, role.membership_count, role.distinct_member_count)
```

#### Roles

```python
# List all role definitions (workspace + project), paginated envelope
page = client.roles.list(workspace_slug)
for role in page.results:
    print(role.namespace, role.slug, role.name)

# Only workspace-level roles (Owner / Admin / Member / Guest)
workspace_roles = client.roles.list(workspace_slug, namespace="workspace")

# Only project-role definitions (Admin / Contributor / Commenter / Guest).
# These are shared across every project in the workspace — there is no
# per-project roles endpoint.
project_roles = client.roles.list(workspace_slug, namespace="project")

# Retrieve a single role by id
role = client.roles.retrieve(workspace_slug, role_id)
```

> `slug` is the stable identifier to use in code, but it is **not** globally
> unique (`admin`/`guest` exist in both namespaces) — key roles by
> `(namespace, slug)` when indexing them.

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

# Filter project members (same filters as workspace members)
from plane.models.query_params import MemberQueryParams, MemberListQueryParams

members = client.projects.get_members(
    workspace_slug, project_id,
    params=MemberQueryParams(display_name="ana", is_bot=False),
)

# Paginated "lite" list
members = client.projects.get_members_lite(
    workspace_slug, project_id,
    params=MemberListQueryParams(per_page=1000),
)

# Paginated "lite" project list (id, identifier, name, icon/emoji, description,
# cover image, archived_at) — for pickers/reference lookups.
from plane.models.query_params import ProjectLiteListQueryParams

lite = client.projects.list_lite(
    workspace_slug,
    params=ProjectLiteListQueryParams(per_page=1000, order_by="-created_at"),
)
for p in lite.results:
    print(p.identifier, p.name)

# NOTE: archived projects are now EXCLUDED by default. Pass include_archived=True
# to restore the previous behavior of listing archived projects too.
lite = client.projects.list_lite(
    workspace_slug,
    params=ProjectLiteListQueryParams(include_archived=True),
)
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

# Filter cycles by status: current | upcoming | completed | draft | incomplete.
# `status` is canonical; `cycle_view` is a deprecated alias (status wins if both set).
from plane.models.query_params import CycleListQueryParams

upcoming = client.cycles.list(
    workspace_slug, project_id,
    params=CycleListQueryParams(status="upcoming"),
)
for c in upcoming.results:  # paginated envelope
    print(c.name)

# NOTE: status="current" is a special case — the API returns a BARE LIST of cycles
# (not the paginated envelope). list() returns whichever shape the server sends.
current = client.cycles.list(
    workspace_slug, project_id,
    params=CycleListQueryParams(status="current"),
)
for c in current:  # plain list[Cycle]
    print(c.name)

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

# Paginated "lite" cycle list (full cycle fields minus issue-count metrics).
# Supports a status filter: current | upcoming | completed | draft | incomplete
# (omit for all). The lite endpoint takes only `status` (no `cycle_view` alias)
# and ALWAYS paginates — even for status="current".
from plane.models.query_params import CycleLiteListQueryParams

lite = client.cycles.list_lite(
    workspace_slug, project_id,
    params=CycleLiteListQueryParams(status="current", per_page=1000),
)
for c in lite.results:
    print(c.name)

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

# Paginated "lite" module list (full module fields minus issue-count metrics)
from plane.models.query_params import LiteListQueryParams

lite = client.modules.list_lite(
    workspace_slug, project_id,
    params=LiteListQueryParams(per_page=1000, order_by="-created_at"),
)
for m in lite.results:
    print(m.name)

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

#### Workspace States

Workspace-level work-item states. Reads are dual-mode: under workspace
governance they serve the workspace states catalog; in ungoverned workspaces
they aggregate the states of every project the caller can access. Writes
require the workspace to own states and workflows (check
`client.workspaces.get_features(workspace_slug).states_owned_by_workspace`).

```python
# List states at workspace scope (works in both modes)
states = client.workspace_states.list(workspace_slug)

# Create a workspace (catalog) state — governed workspaces only
from plane.models.states import CreateWorkspaceState

state = client.workspace_states.create(
    workspace_slug,
    data=CreateWorkspaceState(name="In Review", color="#3b82f6", group="started"),
)

# Retrieve / update / delete
state = client.workspace_states.retrieve(workspace_slug, state_id)

from plane.models.states import UpdateWorkspaceState

state = client.workspace_states.update(
    workspace_slug, state_id, data=UpdateWorkspaceState(color="#22c55e")
)
client.workspace_states.delete(workspace_slug, state_id)
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

#### Workspace Workflows

The workspace workflow catalog (workspace governance). `list` is dual-mode;
all writes require the workspace to own states and workflows.

```python
# List workspace workflows
workflows = client.workspace_workflows.list(workspace_slug)

# Create a workflow draft, then configure its chain from catalog states
from plane.models.states import CreateWorkspaceState
from plane.models.workspace_workflows import (
    AddWorkspaceWorkflowStates,
    CreateWorkspaceWorkflow,
    CreateWorkspaceWorkflowTransition,
)

state_a = client.workspace_states.create(
    workspace_slug, data=CreateWorkspaceState(name="Todo", color="#94a3b8", group="unstarted")
)
state_b = client.workspace_states.create(
    workspace_slug, data=CreateWorkspaceState(name="Doing", color="#3b82f6", group="started")
)
workflow = client.workspace_workflows.create(
    workspace_slug, data=CreateWorkspaceWorkflow(name="Engineering")
)
client.workspace_workflows.states.add(
    workspace_slug,
    workflow.id,
    data=AddWorkspaceWorkflowStates(state_ids=[state_a.id, state_b.id]),
)
client.workspace_workflows.states.mark_default(workspace_slug, workflow.id, state_a.id)

# Transitions
transition = client.workspace_workflows.transitions.create(
    workspace_slug,
    workflow.id,
    data=CreateWorkspaceWorkflowTransition(state_id=state_a.id, transition_state_id=state_b.id),
)

# Full chain, usage report, and activity log
workflow = client.workspace_workflows.retrieve(workspace_slug, workflow.id)
usage = client.workspace_workflows.usage(workspace_slug, workflow.id)
activities = client.workspace_workflows.activities(workspace_slug, workflow.id)

# Transition hooks (validation/action hooks, webhook secrets, executions)
hooks = client.workspace_workflows.hooks.list(workspace_slug, workflow.id, transition.id)
```

#### Work Item Type Governance

Governs which workflows a workspace-level work item type may use
(`any` / `constrained` / `required` modes, allowlists, and per-project pins).
Workspace governance only.

```python
# type_id: UUID of a workspace work item type; workflow_id: UUID of a
# workspace workflow (e.g. workflow.id from the example above)

# Read and change a type's governance
governance = client.work_item_type_governance.retrieve(workspace_slug, type_id)

from plane.models.work_item_type_governance import UpdateTypeGovernance

governance = client.work_item_type_governance.update(
    workspace_slug,
    type_id,
    data=UpdateTypeGovernance(mode="constrained", workflow_ids=[workflow_id]),
)

# Dry-run the impact first
from plane.models.work_item_type_governance import TypeGovernancePreviewRequest

preview = client.work_item_type_governance.preview(
    workspace_slug,
    type_id,
    data=TypeGovernancePreviewRequest(mode="required", required_workflow_id=workflow_id),
)

# Per-project pins
pins = client.work_item_type_governance.pins.list(workspace_slug, type_id)

# Project-side view: each type's effective workflow, and the project's pick
entries = client.work_item_type_governance.project_workflows.list(workspace_slug, project_id)

from plane.models.work_item_type_governance import SetProjectWorkflowPick

client.work_item_type_governance.project_workflows.update_pick(
    workspace_slug, project_id, type_id, data=SetProjectWorkflowPick(workflow_id=workflow_id)
)
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
- `PaginatedQueryParams` - Cursor-based pagination support (cursor, per_page)
- `WorkItemQueryParams` - Work item specific queries (expand, order_by, `filters`, `pql`, etc.)
- `RetrieveQueryParams` - Retrieve operations (expand, fields, etc.)

#### Filtering work items

`WorkItemQueryParams` accepts two filter inputs that map to the same backend filter engine:

- **`filters`** — a structured filter expression (dict). Supports nested
  `and` / `or` / `not` groups and field operators (`__in`, `__gte`,
  `__range`, `__icontains`, etc.). The SDK JSON-encodes this into the
  `filters=` query parameter.
- **`pql`** — a Plane Query Language string. Human-readable alternative
  with the same expressive power.

```python
from plane.models.query_params import WorkItemQueryParams

# Project-scoped, structured filters
client.work_items.list(
    "my-workspace",
    "project-id",
    params=WorkItemQueryParams(
        filters={"and": [
            {"priority": "urgent"},
            {"state_group__in": ["unstarted", "started"]},
        ]},
        order_by="-created_at",
        per_page=50,
    ),
)

# Project-scoped, PQL
client.work_items.list(
    "my-workspace",
    "project-id",
    params=WorkItemQueryParams(pql='priority = "urgent" AND assignee = currentUser()'),
)

# Workspace-scoped — spans every project the caller can view, with
# per-project authorization honored server-side
client.work_items.list_workspace(
    "my-workspace",
    params=WorkItemQueryParams(filters={"priority": "urgent"}),
)
```

The same `filters` and `pql` query parameters also work on `list_archived`,
`cycles.list_work_items`, and `modules.list_work_items`.

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
