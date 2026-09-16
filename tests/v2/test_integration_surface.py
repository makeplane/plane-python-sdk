"""The compiler Python does not have, pointed at the live integration suite.

The runtime guard (`tests/v2/integration/_guard.py`) makes a dead suite impossible to
*misread*; this makes it impossible to *reach*. It is the half that works with no
credentials, no server and no network -- which matters, because the 385 dead tests
were dead for a whole migration precisely in the state everybody runs: dormant.

Nothing at runtime can catch `client.v2.workspace(slug)` in a body that never
executes. mypy can, from the same `py.typed` package and typed `Loaded` navigation
that `test_typing.py` already leans on -- and it catches the rest of the family too:
a method renamed, an argument dropped, a path id reordered, a navigation property
that no longer exists on a row. Every one of those is a call site that would raise on
the first live run and skip silently on every other.

Strictness is deliberately relaxed to what a *test file* should satisfy (untyped
helpers are fine); what is not relaxed is name and signature resolution against the
SDK, which is the whole point.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
import textwrap

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

LIVE_SUITES = (
    REPO_ROOT / "tests" / "v2" / "integration",
    # Same trap, outside that directory: both tests in this file were written against
    # the retired locator and had been skipping green for exactly as long.
    REPO_ROOT / "tests" / "v2" / "test_live_smoke.py",
)
"""Every suite that only executes against a live server, and so can rot unseen.

Not all of `tests/v2/` -- the offline tests construct resources directly and carry a
few hundred `Optional`-narrowing complaints under these relaxed flags. Cleaning those
up would widen this guard to the whole package, and is worth doing; it is not this
change."""

# `strict = true` in pyproject is aimed at the package; over test files it would drown
# real resolution errors in `disallow_untyped_defs` noise. These flags keep exactly the
# checks that answer "does this call site still exist on the SDK?".
_RELAXED = (
    "--follow-imports=silent",
    "--allow-untyped-defs",
    "--allow-untyped-calls",
    "--allow-incomplete-defs",
    "--allow-untyped-decorators",
)


def _mypy(*targets: str, extra: tuple[str, ...] = ()) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "mypy", *_RELAXED, *extra, *targets],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_every_integration_call_site_resolves_against_the_sdk() -> None:
    """The assertion this module exists for.

    A failure here is not a typing nit: it is a call site that would raise at runtime,
    in a suite whose default state is to skip before it could.
    """
    result = _mypy(*[str(path) for path in LIVE_SUITES])

    errors = [line for line in result.stdout.splitlines() if ": error:" in line]
    assert not errors, (
        f"{len(errors)} live call sites no longer resolve against the SDK.\n"
        "Each is a test that would raise on a live run and skip silently on every "
        "other run. Fix the call site (or the SDK), never the assertion.\n\n"
        + "\n".join(errors[:40])
        + ("\n..." if len(errors) > 40 else "")
    )


def test_the_surface_guard_catches_the_locator_that_actually_vanished(
    tmp_path: pathlib.Path,
) -> None:
    """Proof it bites, on the real historical regression.

    `client.v2.workspace(slug).project(project)` was how all 115 call sites reached a
    resource before the flat surface landed. Every one of them kept skipping green.
    """
    probe = tmp_path / "probe.py"
    probe.write_text(
        textwrap.dedent(
            """
            from plane.client import PlaneClient

            client = PlaneClient(base_url="https://x", api_key="k")
            client.v2.workspace("acme").project("ENG").states.list()
            """
        )
    )
    result = _mypy(str(probe))

    assert result.returncode != 0
    assert 'has no attribute "workspace"' in result.stdout, result.stdout


def test_the_surface_guard_catches_a_dropped_path_id(tmp_path: pathlib.Path) -> None:
    """The subtler half: the attribute chain is right, but an id the URL needs is
    missing. At runtime that is a `MissingPathId` on a line nobody runs."""
    probe = tmp_path / "probe.py"
    probe.write_text(
        textwrap.dedent(
            """
            from plane.client import PlaneClient

            client = PlaneClient(base_url="https://x", api_key="k")
            client.v2.workspaces.projects.states.list("acme")
            """
        )
    )
    result = _mypy(str(probe))

    assert result.returncode != 0
    assert "Missing positional argument" in result.stdout, result.stdout


def test_the_surface_guard_catches_a_navigation_property_that_is_gone(
    tmp_path: pathlib.Path,
) -> None:
    """Loaded-row navigation is checked too -- the half a flat-path-only refresh would
    leave unexercised, and the half no grep for `client.v2` would ever see."""
    probe = tmp_path / "probe.py"
    probe.write_text(
        textwrap.dedent(
            """
            from plane.client import PlaneClient

            client = PlaneClient(base_url="https://x", api_key="k")
            project = client.v2.workspaces.projects.retrieve("acme", "ENG")
            project.tags.list()
            """
        )
    )
    result = _mypy(str(probe))

    assert result.returncode != 0
    assert 'has no attribute "tags"' in result.stdout, result.stdout


# -- The runtime guard's other half: no skip may be undeclared -------------------


def test_no_live_test_calls_pytest_skip_directly() -> None:
    """A grep, and deliberately so.

    `_guard` converts an undeclared skip into a failure at *runtime*, which only helps
    on a run that reaches the test. This catches the same thing at rest: a bare
    `pytest.skip` in a live test is either an SDK problem being hidden or a server
    capability that has not been named, and both are supposed to be impossible here.
    """
    offenders = []
    for path in sorted((REPO_ROOT / "tests" / "v2" / "integration").glob("test_*.py")):
        for number, line in enumerate(path.read_text().splitlines(), start=1):
            if "pytest.skip(" in line:
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{number}")

    assert offenders == [], (
        "these live tests skip without declaring why. Use "
        "`_guard.skip_absent_capability(...)` when the *server* cannot do the thing "
        f"under test; anything else is a bug to fix, not to skip: {offenders}"
    )
