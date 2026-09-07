# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Plane Python SDK (`plane-sdk` on PyPI, v0.3.0) — a synchronous, type-annotated Python client for the Plane API. Built on `requests` + `pydantic` v2, targeting Python 3.10+.

## Common Commands

```bash
# Install for development
pip install -e .
pip install -r requirements.txt

# Run all unit tests (requires env vars, see below)
pytest tests/unit/

# Run a specific test file or test
pytest tests/unit/test_projects.py
pytest tests/unit/test_projects.py::TestProjectsAPICRUD::test_create_project

# Integration/script tests (excluded by default via addopts)
pytest tests/scripts/ --override-ini="addopts="

# Formatting & linting
black plane tests
ruff check plane tests
ruff check --fix plane tests

# Type checking
mypy plane
```

### Required Environment Variables for Tests

Tests make real HTTP requests (no mocking). Set these before running:

- `PLANE_BASE_URL` — API base URL
- `PLANE_API_KEY` or `PLANE_ACCESS_TOKEN` — authentication (exactly one)
- `WORKSPACE_SLUG` — test workspace
- `AGENT_SLUG` — (optional) needed only for agent run tests

## Architecture

### Client → Resource → Model pattern

`PlaneClient` is the single entry point. It holds a `Configuration` and exposes resource objects as attributes:

```
PlaneClient
  ├── .projects      → Projects(BaseResource)
  ├── .work_items    → WorkItems(BaseResource)
  │     ├── .comments
  │     ├── .attachments
  │     ├── .links
  │     └── ...sub-resources
  ├── .cycles        → Cycles(BaseResource)
  └── ...15+ resources
```

### Key directories

- `plane/api/` — Resource classes. Every resource extends `BaseResource` which handles HTTP methods, auth headers, URL building (`/api/v1/...`), retry via `urllib3.Retry`, and response parsing.
- `plane/models/` — Pydantic v2 models. Three kinds per resource:
  - **Response models** (e.g. `Project`): `extra="allow"` for forward compatibility with new API fields.
  - **Request DTOs** (e.g. `CreateProject`, `UpdateProject`): `extra="ignore"` to be strict about inputs.
  - **Query param models** (e.g. `PaginatedQueryParams`): `extra="ignore"`.
- `plane/client/` — `PlaneClient` (API key / access token auth) and `OAuthClient` (OAuth 2.0 flows).
- `plane/errors/` — `PlaneError` → `HttpError`, `ConfigurationError`.
- `plane/config.py` — `Configuration` and `RetryConfig` dataclasses.
- `plane/api/v2/` — the v2 surface (`client.v2`), **migration in progress**: roughly
  85 of the ~120 resource groups are still on the retired pre-flat shape and are
  not wired onto the tree below (`Collections`, most of `work_items/` beyond
  `.comments`, etc. — see each file's own docstring for whether it's wired). The
  bound-locator chain (`client.v2.workspace(slug).project(project)`) is **gone**.
  There are two ways into a resource now:
  - **The flat path.** A static tree reached by plain attribute access, e.g.
    `client.v2.workspaces.projects.states.list("acme", "ENG")`,
    `client.v2.workspaces.projects.work_items.comments.list("acme", "ENG", "ENG-12")`.
    Read it left to right: every segment that names an actual resource consumes
    one URL path id, in order; a segment that only groups children (`.wiki` on
    `Workspaces`, `plane/api/v2/wiki_node.py`, holding just `.pages` today —
    `.collections` isn't wired, `Collections` isn't migrated) consumes none. Path
    ids are positional-or-keyword (`states.list(slug="acme", project="ENG")`
    works). `client.v2.users` / `.user_assets` are the only resources kept
    directly on `V2Namespace` (the 6 operations with no workspace in their path).
    A singleton with no primary key of its own (`workspaces.features`,
    `plane/api/v2/features.py`) hits `url_for`/`_collection_url` directly instead
    of `_retrieve`/`_update`, which both require a `pk` to append.
  - **Loaded rows.** A resource with children today (`projects`, `work_items`)
    returns a `Loaded` row from `retrieve`/`list`/`iterate`, not a bare pydantic
    model: it carries its own data and reaches its own children with none of the
    ids repeated (`project.states.list()`, `work_item.comments.list()`).
    `Loaded.build(row, ids, fields)` (`_kernel/loaded.py`) is the mixin; a
    `Loaded.__getattr__` on a field the request's `fields=` excluded raises
    `FieldNotRequested` instead of reading as `None` — a `None` you get back is a
    real null. `Owned(resource, ids, names)` is the other half: it prepends a
    parent's already-bound ids ahead of a child method's own arguments, and
    raises `TypeError` up front if the child's leading parameters aren't ordered
    the way `names` expects, rather than silently sending values into the wrong
    parameter. `_loaded/project.py` and `_loaded/work_item.py` are today's two
    `Loaded` subclasses; every migrated resource with children will get one the
    same way.
  - `_kernel/` holds the shared machinery beyond `loaded.py`:
    `V2Resource.__init__(transport)` takes no bound scope any more —
    `_collection_url`/`_detail_url` build straight from whatever path params a
    call passes — so a resource's methods work identically whether reached
    through the flat tree or constructed directly (most offline tests do the
    latter). No public v2 method takes `workspace_slug`/`project` parameters as
    such; the path segment's own leading positional-or-keyword parameters carry
    them, in path order. `_generated/constants.py` is produced by
    `scripts/generate_v2_constants.py` from the api_v2 OpenAPI golden and must
    never be hand-edited — it is also what makes field names, `order_by` values
    and filter keyword names real generated `Literal`/`TypedDict` types instead
    of loose strings, which is why the package ships a `py.typed` marker
    (`tests/v2/test_typing.py` proves a type checker actually rejects an unknown
    filter keyword).
  - **Bridges.** Membership between two resources (`.../cycles/{id}/work-items/`,
    `.../releases/{id}/labels/`, `.../collections/{id}/members/`, ...) is never a
    `manage_*(add=, remove=)` method. It is a sub-resource (`proj.cycles.work_items`,
    `ws.initiatives.projects` — both design-intent today, since `cycles`/`initiatives`
    aren't wired onto the flat tree yet; `ws.releases.labels` (wired, verbs sit next
    to the CRUD since it's also the label catalog) is the one bridge reachable
    through `client.v2` right now) exposing exactly `add(parent_id, ids) -> list[str]`
    and `remove(parent_id, ids) -> list[str]`, both delegating to
    `V2Resource._bridge(key=, ids=, **path_params)`. The kernel POSTs `{"add": [...]}`
    or `{"remove": [...]}` only, rejects 0 or >100 ids with `ValueError` before the
    request, and returns the response's `added`/`removed` list. A class whose own
    `path` is not the bridge URL sets `bridge_path`. The bridge class declares the
    golden's single manage operationId under the `"bridge"` key of `operations`. The
    `*Manage*` request/response models stay in `plane/models/v2/*` as the bridge's
    `model`, but are not exported from `plane.models.v2`.
  - **Bridge verbs copy the web app CTA.** Properties on a work item type:
    `link`/`unlink` (unlink deletes the property's values on every work item of the
    type). Members of anything else: `add`/`remove`. `workflows.states.attach` is a
    different bridge (POST `{state_ids}`) and keeps its name.
  - **Lookups.** `find_by_<key>` is server-side via `_find_one` only where the golden
    list op has that filter (`roles.find_by_slug`, `estimates.points.find_by_key`,
    `find_by_name` on properties/options/contexts); property `name` is the machine
    key, not the `display_name` label.
- `plane/models/v2/` — v2 pydantic models. Read models mark every field except `id`
  optional, because `?fields=` and collection deferral can omit any of them.

### Sub-resource pattern

Resources with children (work_items, customers, initiatives, teamspaces) instantiate sub-resource objects in `__init__`:

```python
class WorkItems(BaseResource):
    def __init__(self, config):
        super().__init__(config, "/workspaces/")
        self.comments = WorkItemComments(config)
        self.attachments = WorkItemAttachments(config)
```

### URL convention

All API endpoints end with a trailing `/`. URLs are built as `{base_path}/api/v1{resource_base_path}/{endpoint}/`.

## Coding Conventions

- Line length: 100 (Black + Ruff)
- Use `X | None` not `Optional[X]`; use `list[str]` not `List[str]` (Python 3.10+ builtins)
- Import abstract types from `collections.abc` (e.g. `Mapping`, `Iterable`)
- Ruff rules: E, F, I (isort), UP (pyupgrade), B (bugbear)
- Never use "Issue" in endpoint or parameter names — always use "Work Item"
- Auth is mutually exclusive: `api_key` XOR `access_token` (raises `ConfigurationError` if both/neither)
- Resource methods accept Pydantic DTOs, serialize with `model_dump(exclude_none=True)`, and validate responses with `Model.model_validate()`
- All resources follow CRUD verbs: `create`, `retrieve`, `update`, `delete`, `list`
