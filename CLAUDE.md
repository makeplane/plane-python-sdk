# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Plane Python SDK (`plane-sdk` on PyPI, v0.2.4) — a synchronous, type-annotated Python client for the Plane API. Built on `requests` + `pydantic` v2, targeting Python 3.10+.

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
