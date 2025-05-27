# My API SDK

A comprehensive Python SDK for My API with both synchronous and asynchronous support.

## Features

- **Async/Sync Support**: Use either async/await or synchronous methods
- **Type Safety**: Full type hints and Pydantic models
- **Error Handling**: Comprehensive exception handling with specific error types
- **Retry Logic**: Built-in retry mechanisms for resilient API calls
- **Rate Limiting**: Automatic handling of rate limit responses
- **Pagination**: Easy-to-use pagination support
- **Configuration**: Flexible configuration via environment variables or direct setup

## Installation

```bash
pip install my-api-sdk
```

## Quick Start

### Async Usage

```python
import asyncio
from my_api_sdk import Client, Config

async def main():
    config = Config(api_key="your-api-key")
    
    async with Client(config) as client:
        # List users
        result = await client.users.list()
        users = result["users"]
        
        # Get a specific user
        user = await client.users.get("user-id")
        print(f"User: {user.full_name}")

asyncio.run(main())
```

### Sync Usage

```python
from my_api_sdk import SyncClient, Config

config = Config(api_key="your-api-key")

with SyncClient(config) as client:
    # List users
    result = client.users.list()
    users = result["users"]
    
    # Get a specific user
    user = client.users.get("user-id")
    print(f"User: {user.full_name}")
```

### Environment Variables

Set these environment variables to configure the SDK:

```bash
export MY_API_KEY="your-api-key"
export MY_API_BASE_URL="https://api.example.com/v1"  # optional
export MY_API_TIMEOUT="30"  # optional
export MY_API_MAX_RETRIES="3"  # optional
```

Then initialize without explicit config:

```python
from my_api_sdk import Client

# Uses environment variables
client = Client()
```

## Configuration

The SDK can be configured using the `Config` class:

```python
from my_api_sdk import Config

config = Config(
    api_key="your-api-key",
    base_url="https://api.example.com/v1",
    timeout=30,
    max_retries=3,
    retry_delay=1.0,
    user_agent="my-app/1.0.0"
)
```

## Error Handling

The SDK provides specific exception types for different error conditions:

```python
from my_api_sdk import Client
from my_api_sdk.exceptions import (
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError
)

async with Client() as client:
    try:
        user = await client.users.get("invalid-id")
    except NotFoundError:
        print("User not found")
    except AuthenticationError:
        print("Invalid API key")
    except RateLimitError as e:
        print(f"Rate limited. Retry after {e.retry_after} seconds")
    except ValidationError as e:
        print(f"Validation error: {e.message}")
    except ServerError:
        print("Server error occurred")
```

## Models

The SDK uses Pydantic models for type safety and validation:

```python
from my_api_sdk.models.user import User, UserCreate, UserUpdate

# Create a new user
user_data = UserCreate(
    email="user@example.com",
    firstName="John",
    lastName="Doe",
    password="securepassword"
)

user = await client.users.create(user_data)

# Update user
update_data = UserUpdate(firstName="Jane")
updated_user = await client.users.update(user.id, update_data)

# Access user properties
print(f"Full name: {user.full_name}")
print(f"Email: {user.email}")
print(f"Created: {user.created_at}")
```

## Pagination

List methods return paginated results:

```python
result = await client.users.list(page=1, per_page=20, search="john")

users = result["users"]  # List of User objects
pagination = result["pagination"]  # PaginatedResponse object

print(f"Page {pagination.page} of {pagination.total_pages}")
print(f"Total users: {pagination.total}")
print(f"Has next page: {pagination.has_next}")

# Iterate through all pages
page = 1
while True:
    result = await client.users.list(page=page)
    users = result["users"]
    
    if not users:
        break
        
    for user in users:
        print(f"User: {user.full_name}")
    
    if not result["pagination"].has_next:
        break
        
    page += 1
```

## Development

### Setup

```bash
git clone https://github.com/yourusername/my-api-sdk.git
cd my-api-sdk
pip install -e ".[dev]"
```

### Testing

```bash
pytest
pytest --cov=src/my_api_sdk  # With coverage
```

### Code Quality

```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.