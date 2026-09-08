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
- `plane/api/v2/` — the v2 surface (`client.v2`). **Migration complete**: all 90
  `V2Resource` subclasses in the package (`tests/v2/tree_walk.py`'s
  `all_resource_classes()`) are on the flat shape and swept by the rule tests.
  `tests/v2/tree_walk.py`'s `UNMIGRATED_RESOURCES` — the opt-out list the sweeps
  excluded a class by naming it in — is now `frozenset()`; nothing is opted out
  any more, and `test_path_id_naming.py` still enforces that it can only shrink,
  never grow, so it cannot silently regain a member. Count resources, not
  grouping nodes: `wiki` and `group_sync` hold no `V2Resource` base, `path` or
  `operations` of their own — they only group children (`wiki.pages`,
  `wiki.collections`, `group_sync.config`) — so neither is in the 90.

  The whole project band is wired onto `client.v2.workspaces.projects`:
  `states`, `labels`, `work_items`, `cycles`, `milestones`, `modules`,
  `estimates`, `intakes`, `members`, `views`, `features`, `permissions`,
  `work_item_templates`, `worklogs`, `pages`, `automations`,
  `work_item_properties`, `work_item_types` and `workflows` — nineteen
  children, and a fetched project reaches every one of them that is itself
  navigable (`project.cycles.list()`, `project.permissions.me()`). Nineteen of
  the 90 classes are navigable — `workspaces`, `projects`, `work_items`,
  `cycles`, `milestones`, `modules`, `estimates`, `webhooks`, `collections`,
  `customers`, `initiatives`, `releases`, `work_item_types`,
  `work_item_properties`, `automations` and `workflows` (three of those —
  automations, work item types and work item properties — each have a separate
  project-scoped and workspace-scoped resource class, each independently
  navigable, which is where 16 families become 19 classes) — a fetched row
  reaches its child with no ids repeated. `workspaces` is the root of that set
  and the last to join it: `client.v2.workspaces.retrieve("acme")` answers a
  `LoadedWorkspace` reaching all 24 workspace-scoped families
  (`workspace.projects.list()`), and its children address it by `slug`, never
  the UUID `id`, which that path segment does not accept. `estimates`' child is
  `estimate_points`, not `points` — `Estimate.points` is itself an API field,
  returned inline by `expand=["points"]`. `webhooks` is workspace-scoped, not
  part of the project band, reached via `.logs`. A fetched work item reaches
  all seven of its children — `comments`, `attachments`, `links`, `worklogs`,
  `activities`, `relations`, `dependencies`.

  `client.v2.workspaces.roles.list("acme", role_slug="admin")` is worth flagging:
  the workspace slug is the positional argument, while the role's own slug filter
  is spelled `role_slug` because it would otherwise collide with it. The
  bound-locator chain (`client.v2.workspace(slug).project(project)`) is **gone**.
  There are two ways into a resource:
  - **The flat path.** A static tree reached by plain attribute access, e.g.
    `client.v2.workspaces.projects.states.list("acme", "ENG")`,
    `client.v2.workspaces.projects.work_items.comments.list("acme", "ENG", "ENG-12")`.
    Read it left to right: every segment that names an actual resource consumes
    one URL path id, in order; a segment that only groups children (`.wiki` on
    `Workspaces`, `plane/api/v2/wiki_node.py`, holding `.pages` and
    `.collections`, both real resources — neither is a placeholder) consumes
    none. Path ids are positional-or-keyword (`states.list(slug="acme",
    project="ENG")` works). `client.v2.users` / `.user_assets` are the only
    resources kept directly on `V2Namespace` (the 6 operations with no
    workspace in their path). A singleton with no primary key of its own
    (`workspaces.features`, `plane/api/v2/features.py`) goes through the
    kernel's `_retrieve_singleton`/`_update_singleton` pair instead of
    `_retrieve`/`_update`, which both require a `pk` to append.
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
    enforces it across every resource. **The set under test is enumerated, not
    hand-picked**: `tests/v2/tree_walk.py`'s `all_resource_classes()` returns
    every `V2Resource` subclass in the package, minus `UNMIGRATED_RESOURCES` —
    an explicit opt-out list, not a heuristic selection (wired-onto-the-tree, or
    "`list` already looks flat-shaped") the way earlier rounds picked members.
    `UNMIGRATED_RESOURCES` is `frozenset()` now — every class is swept — and
    `test_path_id_naming.py` still enforces that it can only shrink (never
    regain a name once removed), so a regression can't quietly opt a class back
    out. "Flat-shaped" is judged over *every* public method
    (`flat_shaped_resource_classes()`), not over `list` alone — a bridge, a
    singleton or a dict-shaped resource has no `list`, so a heuristic keyed on
    `list` could never have caught one of those being migrated while staying
    opted out. A hand-picked selection is what let a whole batch of violations
    ship green once — never reintroduce one.
  - **Loaded rows.** A resource with children (`projects`, `work_items`,
    `cycles`, `milestones`, `modules`, `estimates`, `webhooks`, `collections`,
    `customers`, `initiatives`, `releases`, `work_item_types`,
    `work_item_properties`, `automations`, `workflows`, `workspaces` — 19 of the
    90 classes) returns a `Loaded` row from `retrieve`/`list`/`iterate`, not a bare
    pydantic model: it carries its own data and reaches its own children with none of the
    ids repeated (`project.states.list()`, `work_item.comments.list()`,
    `cycle.work_items.add(["w1"])`).
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

    A loaded row also keeps the **forward-compatibility** guarantee the read models
    are `extra="allow"` for: `Loaded.__getattr__` shadows `BaseModel.__getattr__`,
    where pydantic serves `__pydantic_extra__`, so it falls through to it before
    raising. Without that fall-through a field the server sends and the model does
    not declare was readable on a plain row and `AttributeError` on a loaded one —
    while `model_dump()` and `_present` both still reported it.

    **A loaded row must reach every child its resource attaches.** The two sides used
    to be unrelated: `test_tree.py` compared `PROJECT_TREE_ATTACHMENTS` against
    `vars(Projects(...))`, and nothing compared either to `LoadedProject`, which is
    how `Projects` came to attach fifteen children while its rows exposed three.
    `tests/v2/test_loaded_navigation.py` sweeps it now — for every class declaring a
    `loaded_model`, the navigation properties on its `Loaded` type must be exactly
    the child resources the class attaches, and each must wrap its own child. The one
    allowed divergence is a name collision with a real API field, written down in
    that file's `NAVIGATION_ALIASES` (`Estimate.points` → `estimate_points`).

    **And having children must itself mean declaring a `loaded_model`.** Those two
    checks *select* the classes that declare one, so a resource with children and no
    `loaded_model` had nothing to compare and passed by never being looked at —
    which is how `Workspaces` came to attach 24 children and answer a bare
    `Workspace`, `workspace.projects` raising `AttributeError` on the design's
    navigable row #1 with every sweep green. The same shape as the path-id rule
    breaking across 16 classes: a rule enforced over an opportunistic subset holds
    only for the members that opted in. So the same file enumerates instead —
    `test_every_resource_with_children_declares_a_loaded_model` runs over every
    class in the package, and `test_the_child_bearing_sweep_bites` runs it against a
    synthetic class built to violate it, so the failure is a thing that has been
    seen rather than assumed. A child that is not really a per-row child — a
    workspace-level catalog hung off a family — is moved to the scope it belongs to,
    not exempted.

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
    `tests/v2/test_typing.py` runs mypy to prove it. `_loaded/` holds one module
    per `Loaded` subclass — `project.py`, `work_item.py`, `cycle.py`,
    `milestone.py`, `module.py`, `estimate.py`, `webhook.py`, `collection.py`,
    `customer.py`, `initiative.py`, `release.py`, `work_item_type.py`,
    `work_item_property.py`, `automation.py`, `workflow.py`, `workspace.py`; copy
    whichever is closest in shape (single bridge-only child vs. several plain-CRUD
    children). `workspace.py` is the `bind1` exemplar and the widest, at 24
    children; the two grouping nodes (`wiki`, `group_sync`) are deliberately not
    among them — neither holds a `V2Resource` base, so neither is a child a row can
    bind, and they are reached from the namespace instead.
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
    on the method: `tests/v2/test_expand_coverage.py` sweeps every resource class
    against the golden's `EXPAND` table and fails on any method that omits an
    `expand` the API accepts (`delete` excepted — 204, no body to shape). The same
    goes for `fields`: it is exposed wherever the golden declares `?fields=` for an
    operation, **except** an operation whose response body is one-time and
    unrecoverable — a secret shown once (`Webhooks.regenerate`), or an envelope
    richer than the golden documents whose extra data only exists in that one reply
    (`WorkItemAttachments.create`) — where a projection could silently and
    irrecoverably drop data the caller cannot get back. Those omissions must name
    the one-time-response reason in the method's own docstring, or the next reader
    "fixes" them back. That rule is a sweep too now, not just prose:
    `tests/v2/test_fields_coverage.py` is the `FIELDS` twin of the `expand` sweep,
    and the exceptions are enumerated in its `ONE_TIME_RESPONSES` with the reason —
    `Webhooks.regenerate` plus the three presigned-upload creates
    (`WorkItemAttachments.create`, `WorkspaceAssets.create`, `UserAssets.create`,
    whose `upload_data` exists only in that one reply). Where a
    resource spells filters out one by one instead of `**filters: Unpack[...]`
    (`Roles`, because the golden's `?slug=` collides with the path id `slug`), pin
    the hand-written set against the generated `TypedDict` so a regeneration cannot
    quietly add an unreachable filter — see `tests/v2/test_roles_resource.py`.
  - **Bridges.** Membership between two resources (`.../cycles/{id}/work-items/`,
    `.../releases/{id}/labels/`, `.../collections/{id}/members/`, ...) is never a
    `manage_*(add=, remove=)` method. It is a sub-resource
    (`client.v2.workspaces.projects.cycles.work_items`, and likewise for
    `milestones.work_items` / `modules.work_items` / `initiatives.projects` /
    `initiatives.work_items` / `customers.work_items` / `releases.work_items` —
    all wired and reachable through `client.v2`, and through a fetched row's own
    property: `cycle.work_items.add(["w1"])`).
    `ws.releases.labels` (verbs sit next to the CRUD since it's also the label
    catalog) is another reachable bridge, as
    `add(slug: str, release: str, label_ids: Sequence[str]) -> list[str]` /
    `remove(slug, release, label_ids)` — every leading path id the bridge's own
    URL needs, in path order, not just the parent id, then the ids to add/remove.
    Every bridge delegates to `V2Resource._bridge(key=, ids=, **path_params)`. The kernel
    POSTs `{"add": [...]}` or `{"remove": [...]}` only, rejects 0 or >100 ids with
    `ValueError` before the request, and returns the response's `added`/`removed`
    list. A class whose own `path` is not the bridge URL sets `extra_paths`, a
    `ClassVar[dict[str, str]]` mapping a method name to its own override template;
    `url_for(method, **path_params)` (called by `_bridge`, and by any other method
    that needs a non-`path` URL) fills `extra_paths.get(method, self.path)` instead
    of `self.path` unconditionally. `ReleaseLabels` is one example: its
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
