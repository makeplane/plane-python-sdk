"""Makes it impossible for the live v2 integration suite to skip silently and look green.

This suite talks to a real server, so with no credentials it *must* skip -- and a
suite that is allowed to skip is a suite that can rot invisibly. It did: when the
bound-locator chain (`client.v2.workspace(slug)`) was removed, every one of the 385
tests here still reported `s`, because the session-scoped credential fixtures skipped
before any test body could raise `AttributeError`. The suite reported green while
testing nothing, for as long as nobody happened to run it with credentials.

Two properties close that hole, and this module enforces both at runtime. The third
-- that the call sites still *resolve* against the SDK, checkable with no server at
all -- is `tests/v2/test_integration_surface.py`, which runs mypy over this directory.

1. **There is exactly one reason the whole suite may lie dormant**: a required env
   var is absent. That decision is made once, here, at collection time, and stamped
   on every item. No fixture makes it, so no fixture can make it *by accident* --
   which is what a bare `pytest.skip` inside a fixture body is.

2. **Every other skip must be declared.** A test that skips because the server lacks
   a capability calls `skip_absent_capability`, which tags the reason. Any skip that
   is not one of those two tagged kinds is converted into a **failure**: that is what
   a fixture swallowing a setup error into `pytest.skip("...")` looks like from here.

3. **Executing nothing is a failure.** With credentials present, a session that
   collects tests and runs none of them -- every test skipped for individually
   legitimate capability reasons, say -- fails loudly, because "we tested nothing"
   is the one outcome that must never read as success.

The dormant case is the *only* green-with-zero-executions state, it is named on the
terminal every run, and it says which env vars would light the suite up.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn

import pytest

if TYPE_CHECKING:  # pragma: no cover - typing only
    from _pytest.reports import TestReport

#: Every env var the suite needs before it can talk to a server. `PLANE_ACCESS_TOKEN`
#: is deliberately not an alternative here: the suite's `client` fixture builds an
#: api-key client, so a token alone would light the suite up and then fail every test.
REQUIRED_ENV = ("PLANE_BASE_URL", "PLANE_API_KEY", "WORKSPACE_SLUG")

#: The one sanctioned reason for the whole suite to sit out a run.
DORMANT_PREFIX = "live v2 integration suite dormant -- "

#: The one sanctioned reason for a single test to sit out a run that is otherwise live.
CAPABILITY_PREFIX = "server capability absent -- "

GUARD_PLUGIN_NAME = "v2-integration-silent-skip-guard"


def missing_env() -> list[str]:
    """The required env vars that are unset or empty, in declaration order."""
    return [name for name in REQUIRED_ENV if not os.getenv(name)]


def dormant_reason() -> str | None:
    """Why the suite may not run at all, or `None` when it must."""
    missing = missing_env()
    if not missing:
        return None
    return f"{DORMANT_PREFIX}{', '.join(missing)} not set"


def skip_absent_capability(reason: str) -> NoReturn:
    """Skip one test because the *server* cannot do the thing under test.

    This is the only sanctioned way to skip inside a live run, and it exists so that
    such a skip is a deliberate, greppable statement about the server rather than an
    incidental one about the SDK. Never reach for it to get past an SDK problem: an
    untagged `pytest.skip` is converted to a failure by this guard precisely so that
    "the call site no longer exists" cannot disguise itself as "the server said no".
    """
    pytest.skip(f"{CAPABILITY_PREFIX}{reason}")


def _skip_reason(report: TestReport) -> str:
    """The human reason out of a skip report's `longrepr`, whatever shape it took."""
    longrepr = report.longrepr
    if isinstance(longrepr, tuple) and len(longrepr) == 3:
        return str(longrepr[2])
    return str(longrepr)


def _is_sanctioned(reason: str) -> bool:
    # pytest renders the reason as "Skipped: <message>"; match on the message anywhere
    # in the rendered form so both marker-driven and call-driven skips are covered.
    return DORMANT_PREFIX in reason or CAPABILITY_PREFIX in reason


class SilentSkipGuard:
    """Session plugin enforcing the three properties in this module's docstring.

    `root` scopes it to one directory so the guard can be exercised against a
    synthetic suite in a tmp dir (see `tests/v2/test_integration_guard.py`) rather
    than only against the real one -- a guard nobody has watched fire is a guard
    nobody knows works.
    """

    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self.collect_only = False
        self.collected = 0
        self.executed = 0
        self.sanctioned_skips = 0
        self.forced_failures: list[str] = []

    def _mine(self, item: pytest.Item) -> bool:
        try:
            path = Path(str(item.path)).resolve()
        except (AttributeError, OSError):  # pragma: no cover - defensive
            return False
        return path == self.root or self.root in path.parents

    # -- collection -------------------------------------------------------------

    def pytest_collection_modifyitems(
        self, config: pytest.Config, items: list[pytest.Item]
    ) -> None:
        # `--collect-only` never runs a test, so "collected N, executed 0" is the
        # correct outcome there rather than the failure this guard exists for.
        self.collect_only = bool(config.getoption("collectonly", default=False))
        mine = [item for item in items if self._mine(item)]
        self.collected = len(mine)
        reason = dormant_reason()
        if reason is None:
            return
        marker = pytest.mark.skip(reason=reason)
        for item in mine:
            item.add_marker(marker)

    # -- per-test ---------------------------------------------------------------

    @pytest.hookimpl(wrapper=True)
    def pytest_runtest_makereport(
        self, item: pytest.Item, call: Any
    ) -> Generator[None, TestReport, TestReport]:
        report = yield
        if not self._mine(item):
            return report
        if report.when == "call" and report.outcome in {"passed", "failed"}:
            self.executed += 1
        if report.outcome == "skipped" and not hasattr(report, "wasxfail"):
            reason = _skip_reason(report)
            if _is_sanctioned(reason):
                self.sanctioned_skips += 1
            else:
                report.outcome = "failed"
                report.longrepr = (
                    f"Undeclared skip: {reason}\n\n"
                    "This suite may only skip for two declared reasons: the whole suite "
                    f"lying dormant ({DORMANT_PREFIX.strip(' -')}), or a single test "
                    f"finding the server cannot do the thing under test, via "
                    "`_guard.skip_absent_capability(...)`.\n"
                    "An undeclared skip is how a broken call site hides -- a fixture "
                    "that swallows its own setup failure into `pytest.skip` reports the "
                    "same green `s` as a suite that is honestly waiting for credentials. "
                    "Fix the call site, or state the server capability explicitly."
                )
                self.forced_failures.append(item.nodeid)
        return report

    # -- session ----------------------------------------------------------------

    def verdict(self) -> str | None:
        """The session-level complaint, or `None` if the session was honest."""
        if self.collected == 0 or self.collect_only:
            return None
        if dormant_reason() is not None:
            if self.sanctioned_skips != self.collected:
                return (
                    f"{self.collected} tests collected while dormant but only "
                    f"{self.sanctioned_skips} carried the dormant reason -- the suite is "
                    "skipping for a reason it did not declare."
                )
            return None
        if self.executed == 0:
            return (
                f"{self.collected} tests collected and 0 executed, with credentials "
                f"({', '.join(REQUIRED_ENV)}) present.\n"
                "A live suite that runs nothing is not a passing suite. Every test was "
                "skipped or errored before its body ran; find out why rather than "
                "reading the green."
            )
        return None

    def pytest_terminal_summary(
        self, terminalreporter: Any, exitstatus: int, config: pytest.Config
    ) -> None:
        if self.collected == 0 or self.collect_only:
            return
        complaint = self.verdict()
        if complaint is not None:
            terminalreporter.write_sep("=", "LIVE V2 INTEGRATION SUITE DID NOT RUN", red=True)
            for line in complaint.splitlines():
                terminalreporter.write_line(line, red=True)
            return
        reason = dormant_reason()
        if reason is not None:
            terminalreporter.write_sep("=", "live v2 integration suite dormant", yellow=True)
            terminalreporter.write_line(
                f"{self.collected} tests skipped: {', '.join(missing_env())} not set. "
                "This is the only sanctioned all-skip state.",
                yellow=True,
            )
        else:
            terminalreporter.write_line(
                f"live v2 integration suite: {self.executed} of {self.collected} executed, "
                f"{self.sanctioned_skips} skipped for declared server capabilities."
            )

    def pytest_sessionfinish(self, session: pytest.Session, exitstatus: int) -> None:
        if self.verdict() is not None:
            session.exitstatus = pytest.ExitCode.TESTS_FAILED


def register(config: pytest.Config, root: Path) -> None:
    """Install the guard for the suite rooted at `root`."""
    config.pluginmanager.register(SilentSkipGuard(root), GUARD_PLUGIN_NAME)
