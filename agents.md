# Plane Python SDK v1

This repository contains the development of a Python SDK for Plane, providing a comprehensive, type-annotated client for interacting with the Plane API.

## Overview

The SDK is designed to provide a clean, type-annotated interface for all Plane API operations, following modern Python development practices (packaging, typing, testing) while keeping the architecture aligned with the Node SDK: a central `PlaneClient`, resource classes extending a shared `BaseResource`, and clear models for requests and responses.

## Architecture

### Main Client Structure

```python
# plane/client.py
from .config import Configuration
from .resources.work_items import WorkItems
from .resources.work_item_types import WorkItemTypes
from .resources.work_item_properties import WorkItemProperties
from .resources.projects import Projects
from .resources.labels import Labels
from .resources.states import States
from .resources.users import Users
from .resources.members import Members
from .resources.modules import Modules
from .resources.cycles import Cycles


class PlaneClient:
  def __init__(
    self,
    *,
    base_url: str,
    api_key: str | None = None,
    access_token: str | None = None,
  ) -> None:
    self.config = Configuration(
      base_path=base_url,
      api_key=api_key,
      access_token=access_token,
    )

    self.work_items = WorkItems(self.config)
    self.work_item_types = WorkItemTypes(self.config)
    self.work_item_properties = WorkItemProperties(self.config)
    self.projects = Projects(self.config)
    self.labels = Labels(self.config)
    self.states = States(self.config)
    self.users = Users(self.config)
    self.members = Members(self.config)
    self.modules = Modules(self.config)
    self.cycles = Cycles(self.config)
```

### Folder Structure

```
plane/
    __init__.py
    config.py
    client.py
    api/
        __init__.py
        base_resource.py
    resources/
        __init__.py
        work_items.py
        work_item_types.py
        work_item_properties.py
        projects.py
        labels.py
        states.py
        users.py
        members.py
        modules.py
        cycles.py
    models/
        __init__.py
        work_item.py
        project.py
        # ... other models
    errors/
        __init__.py
        errors.py
tests/
    e2e/
        test_cycle_creation.py
```

### BaseResource Architecture

The `BaseResource` class will contain all HTTP logic and be extended by all API resources (synchronous version):

```python
# plane/api/base_resource.py
from __future__ import annotations
from typing import Any
from collections.abc import Mapping
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import Configuration
from ..errors.errors import HttpError


class BaseResource:
  def __init__(self, config: Configuration, base_path: str) -> None:
    self.config = config
    self.base_path = base_path.rstrip("/")
    self.session = requests.Session()

    if self.config.retry:
      retry = Retry(
        total=self.config.retry.total,
        backoff_factor=self.config.retry.backoff_factor,
        status_forcelist=self.config.retry.status_forcelist,
        allowed_methods=self.config.retry.allowed_methods,
        respect_retry_after_header=True,
        raise_on_status=False,
      )
      adapter = HTTPAdapter(max_retries=retry)
      self.session.mount("http://", adapter)
      self.session.mount("https://", adapter)

  # HTTP methods
  def _get(self, endpoint: str, params: Mapping[str, Any] | None = None) -> Any:
    url = self._build_url(endpoint)
    response = self.session.get(url, headers=self._headers(), params=params, timeout=self.config.timeout)
    return self._handle_response(response)

  def _post(self, endpoint: str, data: Mapping[str, Any] | None = None) -> Any:
    url = self._build_url(endpoint)
    response = self.session.post(url, headers=self._headers(), json=data, timeout=self.config.timeout)
    return self._handle_response(response)

  def _put(self, endpoint: str, data: Mapping[str, Any] | None = None) -> Any:
    url = self._build_url(endpoint)
    response = self.session.put(url, headers=self._headers(), json=data, timeout=self.config.timeout)
    return self._handle_response(response)

  def _patch(self, endpoint: str, data: Mapping[str, Any] | None = None) -> Any:
    url = self._build_url(endpoint)
    response = self.session.patch(url, headers=self._headers(), json=data, timeout=self.config.timeout)
    return self._handle_response(response)

  def _delete(self, endpoint: str) -> None:
    url = self._build_url(endpoint)
    response = self.session.delete(url, headers=self._headers(), timeout=self.config.timeout)
    self._handle_response(response)

  # Helpers
  def _build_url(self, endpoint: str) -> str:
    endpoint = endpoint.lstrip("/")
    base = f"{self.config.base_path}{self.base_path}/"
    return f"{base}{endpoint}/" if endpoint else base

  def _headers(self) -> dict[str, str]:
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if self.config.api_key:
      headers["X-Api-Key"] = self.config.api_key
    if self.config.access_token:
      headers["Authorization"] = f"Bearer {self.config.access_token}"
    return headers

  def _handle_response(self, response: requests.Response) -> Any:
    if response.status_code == 204:
      return None
    if 200 <= response.status_code < 300:
      if not response.content:
        return None
      if "application/json" in response.headers.get("content-type", "").lower():
        return response.json()
      return response.text
    try:
      payload = response.json()
    except Exception:
      payload = response.text
    raise HttpError(
      f"HTTP {response.status_code}: {response.reason}",
      response.status_code,
      payload,
    )
```

### API Resource Structure

Each resource will have 5 core functionalities by default:

1. Create
2. Update
3. Retrieve
4. List
5. Delete

For each resource, we need to implement the following functions:

```python
# plane/resources/projects.py
from __future__ import annotations
from typing import Any
from collections.abc import Mapping
from ..api.base_resource import BaseResource

class Projects(BaseResource):
  def __init__(self, config) -> None:
    super().__init__(config, "/projects")

  def create(self, data: Mapping[str, Any]) -> dict[str, Any]:
    return self._post("", data)

  def retrieve(self, project_id: str) -> dict[str, Any]:
    return self._get(f"{project_id}")

  def update(self, project_id: str, data: Mapping[str, Any]) -> dict[str, Any]:
    return self._patch(f"{project_id}", data)

  def delete(self, project_id: str) -> None:
    return self._delete(f"{project_id}")

  def list(self, params: Mapping[str, Any] | None = None) -> list[dict[str, Any]]:
    return self._get("", params=params)
```

### Benefits of BaseResource Approach

- **Centralized HTTP logic**: All HTTP requests, error handling, and response processing live in `BaseResource`.
- **Consistent API**: All resources follow the same method patterns and URL building rules.
- **Easy maintenance**: Changes to HTTP logic (timeouts, headers, retries) apply to all resources.
- **Type safety**: Type annotations across resources and models aid static analysis and IDEs.
- **Reduced duplication**: No reimplementation of HTTP logic in each resource.
- **Easy testing**: Mock `requests.Session` and verify calls at the resource level.

## Development Guidelines

### Code Standards

- Use Python 3.10+ with strict type annotations
- Format with Black; lint with Ruff (enable isort rules); enforce via pre-commit
- Consistent docstrings (Google or NumPy style)
- Synchronous SDK using `requests` with connection pooling
- All API URLs should end with `/`

### Ruff Lint Rules (must follow when adding code)

- **Line length**: Keep lines ≤ 100 characters (`tool.ruff.line-length = 100`).
- **Imports (I / isort)**:
  - Group imports: standard library, third-party, then first-party (`plane`).
  - Sort imports within groups; no unused imports; no wildcard imports.
  - Use absolute imports within the package; `known-first-party = ["plane"]`.
- **Pyflakes (F)**:
  - Remove unused variables and imports; prefix intentionally-unused with `_`.
  - Avoid undefined names; ensure symbols are imported/defined before use.
- **Pyupgrade (UP)**:
  - Prefer builtin generics: `list[str]`, `dict[str, Any]` over `typing.List/Dict`.
  - Prefer `X | Y` over `typing.Union[X, Y]` (Python 3.10+).
  - Use f-strings instead of percent-formatting or `str.format` where reasonable.
  - Typing and abstract collections:
    - Import abstract container types from `collections.abc` (e.g., `Iterable`, `Mapping`, `Sequence`, `Callable`, `Collection`, `MutableMapping`, `Set`).
    - Prefer builtin concrete containers (`list`, `dict`, `set`) where appropriate.
    - Prefer `X | None` over `Optional[X]`.
- **Bugbear (B)**:
  - Do not use mutable default arguments (use `None` and initialize inside).
  - Avoid bare `except:`; catch specific exceptions.
  - Avoid unnecessary comprehensions and complexity; keep code clear and direct.
- **Whitespace and style (E)**:
  - No trailing whitespace; keep sensible blank lines; ensure final newline.
  - Follow PEP 8 spacing around operators, commas, colons, and after commas.

Run `pre-commit` locally to auto-fix formatting and imports, and to surface Ruff issues early.

### Testing Strategy

- Use pytest
- Unit tests for resource methods (mock `requests.Session` or responses library)
- Integration tests for API interactions (guard with env flags)
- E2E tests for complete workflows
- Use fixtures for consistent test data

### Error Handling

- Custom error classes in `plane/errors/`
- HTTP status code mapping to meaningful errors where applicable
- Optional retry logic for transient failures (documented, via middleware or wrapper)

## Configuration

### Configuration Class

```python
# plane/config.py
from __future__ import annotations
from collections.abc import Iterable, FrozenSet
from dataclasses import dataclass

@dataclass(frozen=True)
class RetryConfig:
  total: int = 3
  backoff_factor: float = 0.3
  status_forcelist: Iterable[int] = (429, 500, 502, 503, 504)
  allowed_methods: FrozenSet[str] = frozenset({"GET", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"})

class Configuration:
  def __init__(
    self,
    *,
    base_path: str,
    api_key: str | None = None,
    access_token: str | None = None,
    timeout: float | tuple | None = 30.0,
    retry: RetryConfig | None = None,
  ) -> None:
    self.base_path = base_path.rstrip("/")
    self.api_key = api_key
    self.access_token = access_token
    self.timeout = timeout
    self.retry = retry
```

### Client Initialization

```python
import os
from plane.client import PlaneClient

client = PlaneClient(
  base_url=os.environ.get("PLANE_BASE_URL", "https://api.plane.so"),
  api_key=os.environ.get("PLANE_API_KEY"),
  access_token=os.environ.get("PLANE_ACCESS_TOKEN"),
)

# Example: list projects
projects = client.projects.list()
print(projects)
```

## API Resources

### Available Resources

- **WorkItems**: Core issue management
- **Projects**: Project organization
- **Labels**: Issue categorization
- **States**: Workflow management
- **Users**: User management
- **Members**: Team membership
- **Modules**: Feature organization
- **Cycles**: Sprint management
- **WorkItemTypes**: Issue type definitions
- **WorkItemProperties**: Custom properties

### Common Patterns

- All resources are synchronous and extend `BaseResource`
- Methods use `snake_case`; endpoints mirror Plane REST paths
- Pagination, filtering, and sorting via query params
- `delete` is used for removals; trailing `/` enforced by `BaseResource`
- Type-annotated request/response models

## Missing Implementation Details

### pyproject.toml (tooling)

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "plane-python-sdk"
version = "0.1.0"
description = "Python SDK for Plane API"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [{ name = "Plane", email = "dev@plane.so" }]
dependencies = ["requests>=2.31.0", "pydantic>=2.4.0"]

[tool.setuptools.packages.find]
where = ["."]
include = ["plane*"]

[tool.black]
line-length = 100
target-version = ["py310"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
ignore = []

[tool.ruff.lint.isort]
known-first-party = ["plane"]

[tool.pytest.ini_options]
addopts = "-q"
testpaths = ["tests"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_unused_ignores = true
warn_redundant_casts = true
disallow_untyped_defs = true
ignore_missing_imports = true
```

### pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
      - id: ruff-format
```

### Error Classes

```python
# plane/errors/errors.py
class PlaneError(Exception):
  def __init__(self, message: str, status_code: int | None = None) -> None:
    super().__init__(message)
    self.status_code = status_code


class HttpError(PlaneError):
  def __init__(self, message: str, status_code: int, response: object | None = None) -> None:
    super().__init__(message, status_code=status_code)
    self.response = response
```

### Model Definitions

```python
# plane/models/project.py
from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict

class Project(BaseModel):
  model_config = ConfigDict(extra="allow", populate_by_name=True)
  id: str
  name: str
  description: str | None = None
  workspace: str
  created_at: str
  updated_at: str

class CreateProject(BaseModel):
  model_config = ConfigDict(extra="ignore", populate_by_name=True)
  name: str
  description: str | None = None
  workspace: str

class UpdateProject(BaseModel):
  model_config = ConfigDict(extra="ignore", populate_by_name=True)
  name: str | None = None
  description: str | None = None

class ListProjectsParams(BaseModel):
  model_config = ConfigDict(extra="ignore", populate_by_name=True)
  workspace: str | None = None
  limit: int | None = Field(default=20, ge=1, le=100)
  offset: int | None = Field(default=0, ge=0)
```

### Main Exports

```python
# plane/__init__.py
from .client import PlaneClient
from .config import Configuration

# Resources
from .resources.projects import Projects
# from .resources.work_items import WorkItems
# ... other resources

# Models
from .models.project import Project, CreateProject, UpdateProject, ListProjectsParams
# from .models.work_item import WorkItem, ...

# Errors
from .errors.plane_error import PlaneError
from .errors.http_error import HttpError

__all__ = [
  "PlaneClient",
  "Configuration",
  "Projects",
  "Project",
  "CreateProject",
  "UpdateProject",
  "ListProjectsParams",
  "PlaneError",
  "HttpError",
]
```

## Getting Started

1. Install the package: `pip install plane-python-sdk`
2. Import and configure the client (sync)
3. Use specific API resources for operations (e.g., `client.projects.list()`)
4. Handle errors appropriately (catch `HttpError`)
5. Refer to individual resource documentation for models and parameters

## Rules for AI Agents and Models

This section defines the rules and conventions that all AI agents and models must follow when working with the Plane Python SDK v1 codebase.

### Code Quality Standards

#### Python Best Practices

- **Strict Type Annotations**: Use Python 3.10+ with precise typings; avoid `Any` where possible
- **Models**: Use Pydantic v2 with: response models `extra="allow"`; Create*/Update* DTOs `extra="ignore"` (response models use `extra="allow"` for forward compatibility with new API fields)
- **Single Responsibility**: Each class/function has one well-defined purpose
- **Base Class**: All API resources extend `BaseResource`
- **Consistent Naming**: snake_case for functions/methods, PascalCase for classes, lowercase modules

#### Code Organization

- **Synchronous HTTP**: Use `requests.Session` with connection pooling and optional `urllib3.Retry`
- **Shared HTTP Logic**: HTTP, headers, URL building, and response handling live in `BaseResource`
- **Separation of Concerns**: Resources handle endpoints; models handle data; errors under `errors/`

### API Development Rules

#### HTTP Method Conventions

- **GET**: Retrieve data (list, retrieve)
- **POST**: Create resources
- **PATCH**: Partial updates
- **PUT**: Full replacement
- **DELETE**: Remove resources

#### Endpoint Structure

- All endpoints must end with `/`
- Use RESTful URL patterns: `/resources/{id}/sub-resources`
- Each resource should have methods following these verbs
  - list
  - create
  - retrieve
  - update
  - delete
- Implement consistent parameter naming across all endpoints
- Support query parameters for filtering, sorting, and pagination
- Never use the word Issue in endpoint or parameter names. Always use the word Work Item instead.

### Model and Interface Rules

#### Data Model Conventions

- **Pydantic Models**: Use Pydantic v2 for API responses and DTOs
- **DTO Separation**: Separate `Create*` and `Update*` models with appropriate optional fields
- **Optional Fields**: Use `X | None` for non-required fields
- **Date Handling**: Use ISO 8601 string format for all date fields
- **ID Fields**: Use `str` for all ID fields

#### Validation Rules

- **Input Validation**: Validate inputs before API calls when appropriate
- **Static Checking**: Use `mypy` for compile-time checks
- **Runtime Validation**: Use Pydantic v2 for external data parsing and validation

### Testing Requirements

#### Test Coverage

- **Unit Tests**: Minimum 80% code coverage for all API methods
- **Integration Tests**: Test complete API workflows
- **E2E Tests**: Real API interactions guarded by environment flags
- **Error Scenarios**: Test all error conditions and edge cases

#### Test Structure

- **Test Files**: Use `tests/test_*.py` naming
- **Mocking**: Mock `requests.Session` (e.g., `responses`, `requests-mock`)
- **Fixtures**: Use consistent test data fixtures
- **Assertions**: Use descriptive assertion messages

### Documentation Standards

#### Code Documentation

- **Docstrings**: Document all public methods and classes (Google or NumPy style)
- **Parameter Documentation**: Document all parameters and return types
- **Example Usage**: Include usage examples in documentation
- **API Documentation**: Maintain up-to-date API documentation

#### README Requirements

- **Installation Instructions**: Clear setup and installation steps
- **Usage Examples**: Practical code examples (sync with `requests`)
- **Configuration Guide**: Detailed configuration options (timeouts, retries)
- **Troubleshooting**: Common issues and solutions
