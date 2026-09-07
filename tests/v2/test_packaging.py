import pathlib

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_py_typed_marker_exists() -> None:
    assert (ROOT / "plane" / "py.typed").is_file()


def test_py_typed_is_packaged() -> None:
    tomllib = pytest.importorskip("tomllib")
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    package_data = config["tool"]["setuptools"]["package-data"]
    assert "py.typed" in package_data["plane"]


def test_typing_extensions_is_a_runtime_dependency() -> None:
    tomllib = pytest.importorskip("tomllib")
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert any(dep.startswith("typing_extensions") for dep in config["project"]["dependencies"])
