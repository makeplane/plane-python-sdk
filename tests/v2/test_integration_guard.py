"""Proof that the live suite's silent-skip guard actually fires.

`tests/v2/integration/_guard.py` exists because 385 integration tests sat dead for a
whole migration while reporting green: the bound-locator chain they all called was
removed, and the session-scoped credential fixtures skipped before any body could
raise, so every run printed `385 skipped` -- indistinguishable from an honest run
with no credentials.

A guard against that is worth exactly as much as the evidence it has been watched
fire, so each property is asserted twice here: once against a synthetic suite that
violates it (the guard must fail the session), once against one that does not (the
guard must stay out of the way). The suites are run in a subprocess, the same shape
`test_typing.py` uses to run mypy, because the thing under test *is* a pytest session
outcome -- exit code and terminal text -- which cannot be observed from inside itself.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import textwrap

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

CREDENTIALS = {
    "PLANE_BASE_URL": "https://plane.example.com",
    "PLANE_API_KEY": "plane_api_not_a_real_key",
    "WORKSPACE_SLUG": "acme",
}

# The synthetic suites install the guard exactly the way the real integration
# conftest does, so what is under test is the shipped code path, not a copy.
CONFTEST = """
from pathlib import Path

from tests.v2.integration._guard import register


def pytest_configure(config):
    register(config, Path(__file__).parent)
"""


def _run(tmp_path: pathlib.Path, body: str, *, credentials: bool) -> subprocess.CompletedProcess:
    (tmp_path / "conftest.py").write_text(textwrap.dedent(CONFTEST))
    (tmp_path / "test_probe.py").write_text(textwrap.dedent(body))

    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT)
    for name in CREDENTIALS:
        env.pop(name, None)
    if credentials:
        env.update(CREDENTIALS)

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(tmp_path),
            "--override-ini=addopts=",
            "-p",
            "no:cacheprovider",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )


# -- Property 1: executing nothing is a failure ---------------------------------


def test_a_live_session_that_executes_nothing_fails(tmp_path: pathlib.Path) -> None:
    """Every test skipped for an individually *legitimate* server-capability reason
    still adds up to "we tested nothing", which must never read as success."""
    result = _run(
        tmp_path,
        """
        from tests.v2.integration._guard import skip_absent_capability

        def test_one():
            skip_absent_capability("RELEASES not enabled on this workspace")

        def test_two():
            skip_absent_capability("IDP_GROUP_SYNC not enabled on this workspace")
        """,
        credentials=True,
    )

    assert result.returncode != 0, result.stdout
    assert "LIVE V2 INTEGRATION SUITE DID NOT RUN" in result.stdout, result.stdout
    assert "2 tests collected and 0 executed" in result.stdout, result.stdout


def test_a_live_session_that_executes_something_is_green(tmp_path: pathlib.Path) -> None:
    result = _run(
        tmp_path,
        """
        def test_one():
            assert True
        """,
        credentials=True,
    )

    assert result.returncode == 0, result.stdout
    assert "1 of 1 executed" in result.stdout, result.stdout


def test_capability_skips_alongside_real_executions_stay_green(tmp_path: pathlib.Path) -> None:
    """The guard must not punish a genuine capability skip -- only a session where
    that is *all* that happened."""
    result = _run(
        tmp_path,
        """
        from tests.v2.integration._guard import skip_absent_capability

        def test_runs():
            assert True

        def test_skips():
            skip_absent_capability("RELEASES not enabled on this workspace")
        """,
        credentials=True,
    )

    assert result.returncode == 0, result.stdout
    assert "1 of 2 executed, 1 skipped for declared server capabilities" in result.stdout


# -- Property 2: an undeclared skip is a failure ---------------------------------


def test_a_fixture_that_swallows_its_failure_into_a_skip_fails(tmp_path: pathlib.Path) -> None:
    """The failure mode the whole guard exists for, in miniature: setup breaks, the
    fixture turns the breakage into `pytest.skip`, and the run reports green."""
    result = _run(
        tmp_path,
        """
        import pytest

        @pytest.fixture
        def thing():
            try:
                raise AttributeError("'V2Namespace' object has no attribute 'workspace'")
            except AttributeError as exc:
                pytest.skip(f"setup unavailable: {exc}")

        def test_uses_it(thing):
            assert thing
        """,
        credentials=True,
    )

    assert result.returncode != 0, result.stdout
    assert "Undeclared skip" in result.stdout, result.stdout
    assert "no attribute 'workspace'" in result.stdout, result.stdout


def test_the_retired_per_fixture_credential_skip_is_now_a_failure(
    tmp_path: pathlib.Path,
) -> None:
    """The exact shape the old conftest used. It is indistinguishable from the guard's
    dormant reason to a human reading `s`, and it is made in the wrong place -- inside
    a fixture, per-test, where it can fire for reasons that have nothing to do with
    credentials. With credentials present it can now only be a bug, and reads as one."""
    result = _run(
        tmp_path,
        """
        import os

        import pytest

        @pytest.fixture
        def base_url():
            value = os.getenv("SOME_OTHER_VAR")
            if not value:
                pytest.skip("PLANE_BASE_URL not set; skipping live v2 integration tests")
            return value

        def test_uses_it(base_url):
            assert base_url
        """,
        credentials=True,
    )

    assert result.returncode != 0, result.stdout
    assert "Undeclared skip" in result.stdout, result.stdout


# -- Property 3: dormant is the one sanctioned all-skip state --------------------


def test_dormant_without_credentials_is_green_and_says_why(tmp_path: pathlib.Path) -> None:
    result = _run(
        tmp_path,
        """
        def test_one():
            raise AssertionError("must never run without credentials")

        def test_two():
            raise AssertionError("must never run without credentials")
        """,
        credentials=False,
    )

    assert result.returncode == 0, result.stdout
    assert "live v2 integration suite dormant" in result.stdout, result.stdout
    assert "2 tests skipped" in result.stdout, result.stdout
    assert "PLANE_BASE_URL, PLANE_API_KEY, WORKSPACE_SLUG not set" in result.stdout, result.stdout


def test_one_missing_credential_is_enough_to_go_dormant_and_names_it(
    tmp_path: pathlib.Path,
) -> None:
    """A partially configured environment must not half-run the suite: it would fail
    tests for a reason that has nothing to do with the code under test."""
    (tmp_path / "conftest.py").write_text(textwrap.dedent(CONFTEST))
    (tmp_path / "test_probe.py").write_text("def test_one():\n    assert True\n")

    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT)
    env.update(CREDENTIALS)
    env.pop("WORKSPACE_SLUG")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(tmp_path),
            "--override-ini=addopts=",
            "-p",
            "no:cacheprovider",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )

    assert result.returncode == 0, result.stdout
    assert "WORKSPACE_SLUG not set" in result.stdout, result.stdout
    assert "PLANE_BASE_URL" not in result.stdout.split("dormant", 1)[-1], result.stdout


# -- The guard is actually installed on the real suite ---------------------------


def test_the_real_integration_suite_reports_the_dormant_banner() -> None:
    """Wiring, not behaviour: the guard is registered by the shipped conftest, so the
    real 385-test suite cannot go back to printing a bare `385 skipped`."""
    env = dict(os.environ)
    for name in CREDENTIALS:
        env.pop(name, None)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/v2/integration",
            "--override-ini=addopts=",
            "-p",
            "no:cacheprovider",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )

    assert result.returncode == 0, result.stdout
    assert "live v2 integration suite dormant" in result.stdout, result.stdout
    assert "This is the only sanctioned all-skip state" in result.stdout, result.stdout
