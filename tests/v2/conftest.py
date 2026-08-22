import pytest

from plane.config import Configuration


@pytest.fixture
def config() -> Configuration:
    return Configuration(base_path="https://api.example.com", api_key="secret")
