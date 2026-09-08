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

**Scoping a migration plan's gates to its own diff:** when a task gate needs "the files
this plan touched" (e.g. a `black --check`/`mypy` pass limited to one v2 migration plan's
work), anchor the `git diff` to the plan's own base commit — the parent of its first
commit — not to `HEAD~N`. A fixed commit count silently under-counts as soon as a plan
gains more commits than the window (verified during the v2 workspace-resources plan:
a `HEAD~5` window missed 4 already-migrated files that landed earlier in the same plan).
Anchoring to the base commit is stable regardless of how many commits the plan ends up
taking.

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
- `plane/api/v2/` — the v2 surface (`client.v2`), **migration in progress**: of the
  roughly 78 resource classes still on the retired pre-flat shape when this round
  began, 19 are now migrated and wired onto the tree, leaving roughly 59 not wired
  below (`Collections`, most of `work_items/` beyond `.comments`, etc. — see each
  file's own docstring for whether it's wired). Count resources, not grouping
  nodes: `group_sync` itself has no `V2Resource` base, `path` or `operations` (it
  only groups children, exactly like `wiki`), so the 19 are 15 direct workspace
  resources — `artifacts`, `assets`, `audit_logs`, `customer_properties`,
  `invitations`, `members`, `permission_schemes`, `permissions`, `roles`,
  `stickies`, `teamspaces`, `views`, `work_item_relation_definitions`,
  `work_item_templates`, and `work_items` (a distinct, workspace-wide, list-only
  resource, not the project-scoped `workspaces.projects.work_items` whose own
  children are still mostly `PendingMigration`) — plus `group_sync`'s 3 children
  (`.config`, `.project_mappings`, `.workspace_mappings`, none of which consume a
  project id despite `project_mappings`' name) plus `releases.tags`.
  `client.v2.workspaces.roles.list("acme", role_slug="admin")` is worth flagging:
  the workspace slug is the positional argument, while the role's own slug filter
  is spelled `role_slug` because it would otherwise collide with it. The
  bound-locator chain (`client.v2.workspace(slug).project(project)`) is **gone**.
  There are two ways into a resource now:
  - **The flat path.** A static tree reached by plain attribute access, e.g.
    `client.v2.workspaces.projects.states.list("acme", "ENG")`,
    `client.v2.workspaces.projects.work_items.comments.list("acme", "ENG", "ENG-12")`.
    Read it left to right: every segment that names an actual resource consumes
    one URL path id, in order; a segment that only groups children (`.wiki` on
    `Workspaces`, `plane/api/v2/wiki_node.py`, holding `.pages` plus a
    `.collections` placeholder — `Collections` isn't migrated) consumes none. Path
    ids are positional-or-keyword (`states.list(slug="acme", project="ENG")`
    works). `client.v2.users` / `.user_assets` are the only resources kept
    directly on `V2Namespace` (the 6 operations with no workspace in their path).
    A singleton with no primary key of its own (`workspaces.features`,
    `plane/api/v2/features.py`) goes through the kernel's
    `_retrieve_singleton`/`_update_singleton` pair instead of `_retrieve`/`_update`,
    which both require a `pk` to append.
  - **Path ids — the naming rule (one rule, no exceptions).** *A path-id parameter
    is named after the resource it identifies, singular, with **no `_id` suffix**.*
    So `slug` (the workspace), `project`, `work_item`, `state`, `label`, `page`,
    `comment`, `release` — the same name whether it is the method's own primary key
    (`work_items.retrieve(slug, project, work_item)`) or an ancestor's
    (`work_items.comments.list(slug, project, work_item)`). This is not cosmetic:
    `Owned` compares a child method's leading parameter names against the parent's
    `loaded_names` *literally* and refuses the call on a mismatch, so a resource that
    suffixes its own pk breaks navigation from its parent. Two things keep their
    golden-derived names and are **not** covered by this rule: the URL templates
    (`path = ".../projects/{project_id}/work-items/{work_item_id}/comments/"`) and
    model field names (`WorkItem.state_id`). `tests/v2/test_path_id_naming.py`
    enforces it across the migrated resources, and derives that set rather than
    listing it: `tests/v2/tree_walk.py` walks the live tree from `V2Namespace` and
    also picks up any class whose `list` already consumes every path id its template
    names, so a newly migrated resource is swept the moment it exists. A hand-written
    list of what to check is what let a whole batch of violations ship green once —
    never reintroduce one.
  - **Loaded rows.** A resource with children today (`projects`, `work_items`)
    returns a `Loaded` row from `retrieve`/`list`/`iterate`, not a bare pydantic
    model: it carries its own data and reaches its own children with none of the
    ids repeated (`project.states.list()`, `work_item.comments.list()`).
    `Loaded.build(row, ids, fields)` (`_kernel/loaded.py`) is the mixin; reading a
    field the row does not carry raises `FieldNotRequested` instead of reading as
    `None` — a `None` you get back is a real null. **Presence is computed from the
    response** (`row.model_fields_set`), narrowed by `fields=` when the caller passed
    one — never from the request alone, because the API defers fields on collection
    reads even when no `fields=` is in play. `Owned(resource, ids, names)` is the
    other half: it prepends a parent's already-bound ids ahead of a child method's own
    arguments, and raises `TypeError` up front if the child's leading parameters
    aren't ordered the way `names` expects, rather than silently sending values into
    the wrong parameter.

    A navigable resource mixes in `LoadsNavigableRows[LoadedX]`, declares
    `loaded_model` / `loaded_names`, overrides `_row_id` only where a child URL uses
    something other than `id` (projects use `identifier`), and then every method that
    answers with a row returns `self._load(row, *parent_ids, fields=fields)` —
    including `find_by_name` and verb actions like `archive`. **Any method returning a
    row of a navigable type returns the loaded form**; mixing plain and loaded returns
    on one class silently drops navigation.

    **Navigation must be typed, not `Any`.** `Owned.__getattr__` and
    `Loaded.__getattr__` are hidden behind `if not TYPE_CHECKING`, so each `Loaded`
    subclass declares an `if TYPE_CHECKING` view class per child built from the
    kernel's `bind1`/`bind2`/`bind3` helpers — one `staticmethod(bindN(Child.method))`
    line per method, `N` being how many ids the parent binds. `Concatenate` strips
    exactly those leading parameters, so `project.states.list()` types as
    `Page[State]`, unknown keywords are rejected and misspelled methods are errors.
    `tests/v2/test_typing.py` runs mypy to prove it. `_loaded/project.py` and
    `_loaded/work_item.py` are today's two `Loaded` subclasses; copy either.
  - **Wired but not migrated.** Roughly 59 resource classes still use the retired
    pre-flat shape (down from ~78 before the 19 resources listed above were
    migrated). Where one is reachable on the tree anyway (`ws.releases`
    exists for `releases.labels` and `releases.tags`; `work_items` wires seven
    children of which only `.comments` is migrated), it is a `PendingMigration`
    placeholder or a
    `@pending_flat_migration`-decorated method from `_kernel/pending.py`, which raises
    `NotImplementedError` naming the resource. Never leave the real unmigrated class
    wired — it fails with a `MissingPathId` from deep inside the kernel — and never
    just drop the attribute, which reads as a typo.
  - `_kernel/` holds the shared machinery beyond `loaded.py`:
    `V2Resource.__init__(transport)` takes no bound scope any more —
    `_collection_url`/`_detail_url` build straight from whatever path params a
    call passes — so a resource's methods work identically whether reached
    through the flat tree or constructed directly (most offline tests do the
    latter). A path id the call never supplied raises `MissingPathId` (exported from
    `plane.api.v2`) naming the resource, method, template and missing id, not a bare
    `KeyError`. No public v2 method takes `workspace_slug`/`project` parameters as
    such; the path segment's own leading positional-or-keyword parameters carry
    them, in path order. A custom verb whose *response envelope* is not a row of
    the resource's own `model` (`artifacts.publish`, `invitations.bulk`,
    `members.remove`, `work_items.retrieve_by_identifier`) goes through
    `_custom_request` / `_custom_action` / `_custom_action_list` — never a
    hand-rolled `transport.request`, which silently skips `_query`'s
    `fields`/`expand` validation. They take the response `model` explicitly and
    build either URL shape: with `pk` the verb hangs off a row
    (`{detail}/{action}/`, `_action`'s URL), without one it goes through `url_for`
    and its `extra_paths` override. Where the response *is* a row of `model`, keep
    using `_action`/`_void_action`. `_generated/constants.py` is produced by
    `scripts/generate_v2_constants.py` from the api_v2 OpenAPI golden and must
    never be hand-edited — it is also what makes field names, `order_by` values
    and filter keyword names real generated `Literal`/`TypedDict` types instead
    of loose strings, which is why the package ships a `py.typed` marker
    (`tests/v2/test_typing.py` proves a type checker actually rejects an unknown
    filter keyword). Every option the golden offers an operation must be reachable
    on the method: `tests/v2/test_expand_coverage.py` sweeps the migrated resources
    against the golden's `EXPAND` table and fails on any method that omits an
    `expand` the API accepts (`delete` excepted — 204, no body to shape). The same
    goes for `fields`: it is exposed wherever the golden declares `?fields=` for an
    operation, **except** an operation whose response body is one-time and
    unrecoverable — a secret shown once (`Webhooks.regenerate`), or an envelope
    richer than the golden documents whose extra data only exists in that one reply
    (`WorkItemAttachments.create`) — where a projection could silently and
    irrecoverably drop data the caller cannot get back. Those omissions must name
    the one-time-response reason in the method's own docstring, or the next reader
    "fixes" them back. Where a
    resource spells filters out one by one instead of `**filters: Unpack[...]`
    (`Roles`, because the golden's `?slug=` collides with the path id `slug`), pin
    the hand-written set against the generated `TypedDict` so a regeneration cannot
    quietly add an unreachable filter — see `tests/v2/test_roles_resource.py`.
  - **Bridges.** Membership between two resources (`.../cycles/{id}/work-items/`,
    `.../releases/{id}/labels/`, `.../collections/{id}/members/`, ...) is never a
    `manage_*(add=, remove=)` method. It is a sub-resource (`proj.cycles.work_items`,
    `ws.initiatives.projects` — both design-intent today, since `cycles`/`initiatives`
    aren't wired onto the flat tree yet; `ws.releases.labels` (wired, verbs sit next
    to the CRUD since it's also the label catalog) is the one bridge reachable
    through `client.v2` right now, as
    `add(slug: str, release: str, label_ids: Sequence[str]) -> list[str]` /
    `remove(slug, release, label_ids)` — every leading path id the bridge's own
    URL needs, in path order, not just the parent id, then the ids to add/remove),
    both delegating to `V2Resource._bridge(key=, ids=, **path_params)`. The kernel
    POSTs `{"add": [...]}` or `{"remove": [...]}` only, rejects 0 or >100 ids with
    `ValueError` before the request, and returns the response's `added`/`removed`
    list. A class whose own `path` is not the bridge URL sets `extra_paths`, a
    `ClassVar[dict[str, str]]` mapping a method name to its own override template;
    `url_for(method, **path_params)` (called by `_bridge`, and by any other method
    that needs a non-`path` URL) fills `extra_paths.get(method, self.path)` instead
    of `self.path` unconditionally. `ReleaseLabels` is the one migrated example: its
    catalog CRUD hits `path` (`.../releases/labels/`), while

    ```python
    extra_paths = {
        "add": "/workspaces/{slug}/releases/{release_id}/labels/",
        "remove": "/workspaces/{slug}/releases/{release_id}/labels/",
    }
    ```

    sends `add`/`remove` to the per-release URL instead. The retired `bridge_path`
    (a single override for the whole class) is gone; `url_for` raises `TypeError` if
    a class still declares it. The bridge class declares the golden's single manage
    operationId under the `"bridge"` key of `operations`. The `*Manage*`
    request/response models stay in `plane/models/v2/*` as the bridge's `model`, but
    are not exported from `plane.models.v2`.
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
