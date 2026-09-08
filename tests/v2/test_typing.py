"""What a type checker sees, proved by running mypy over probe scripts.

`py.typed` plus generated `Literal`/`TypedDict` aliases only pay off if a checker
actually rejects the mistakes they are meant to catch, and typed navigation on
loaded rows (spec 3.2 / 4) is invisible to the runtime test suite -- so it is
asserted here instead.
"""

import subprocess
import sys
import textwrap

_SETUP = """
from plane.api.v2 import V2Namespace
from plane.config import Configuration

v2 = V2Namespace(Configuration(base_path="https://x", api_key="k"))
project = v2.workspaces.projects.retrieve("acme", "ENG")
"""


def _mypy(tmp_path, body: str) -> subprocess.CompletedProcess:
    """Run mypy over `body`, with errors from the package itself silenced so the
    output is only about the probe."""
    script = tmp_path / "probe.py"
    script.write_text(textwrap.dedent(body))
    return subprocess.run(
        [sys.executable, "-m", "mypy", "--follow-imports=silent", str(script)],
        capture_output=True,
        text=True,
    )


def test_unknown_filter_is_a_type_error(tmp_path) -> None:
    result = _mypy(
        tmp_path,
        """
        from plane.api.v2 import V2Namespace
        from plane.config import Configuration

        v2 = V2Namespace(Configuration(base_path="https://x", api_key="k"))
        v2.workspaces.projects.states.list("acme", "ENG", not_a_filter="x")
        """,
    )
    assert result.returncode != 0
    assert "not_a_filter" in result.stdout


def test_a_migrated_workspace_resource_rejects_an_unknown_filter(tmp_path) -> None:
    """A resource wired in this plan (not the pre-existing `projects.states` case
    above) still gets real filter-keyword checking through `Unpack[...Filters]`."""
    result = _mypy(
        tmp_path,
        """
        from plane.api.v2 import V2Namespace
        from plane.config import Configuration

        v2 = V2Namespace(Configuration(base_path="https://x", api_key="k"))
        v2.workspaces.teamspaces.list("acme", not_a_filter="x")
        """,
    )
    assert result.returncode != 0
    assert "not_a_filter" in result.stdout


# -- Loaded-row navigation is typed, not `Any` (spec 3.2, 4) ---------------------


def test_navigating_a_loaded_row_is_not_any(tmp_path) -> None:
    """`project.states.list()` must carry the child resource's real return type.
    While `Owned.__getattr__` was visible to type checkers every navigation call
    collapsed to `Any`, taking half the public surface out of type checking."""
    result = _mypy(tmp_path, _SETUP + "reveal_type(project.states.list())\n")

    revealed = [line for line in result.stdout.splitlines() if "Revealed type" in line]
    assert len(revealed) == 1, result.stdout
    assert "Any" not in revealed[0], revealed[0]
    assert "OffsetPage[plane.models.v2.states.State]" in revealed[0], revealed[0]


def test_navigation_stays_typed_two_levels_deep(tmp_path) -> None:
    """The design's showcase chain: a loaded work item reached through a loaded
    project still resolves to `LoadedWorkItem`, and its comments to their own model."""
    result = _mypy(
        tmp_path,
        _SETUP + 'reveal_type(project.work_items.retrieve("ENG-12").comments.list())\n',
    )

    revealed = [line for line in result.stdout.splitlines() if "Revealed type" in line]
    assert len(revealed) == 1, result.stdout
    assert "Any" not in revealed[0], revealed[0]
    assert "WorkItemComment" in revealed[0], revealed[0]


def test_misspelled_method_on_a_loaded_rows_child_is_a_type_error(tmp_path) -> None:
    result = _mypy(tmp_path, _SETUP + "project.states.lst()\n")

    assert result.returncode != 0
    assert 'has no attribute "lst"' in result.stdout, result.stdout


def test_unknown_keyword_on_a_loaded_rows_child_is_a_type_error(tmp_path) -> None:
    """Binding the parent's ids must not throw away the child's own parameter
    checking -- `Concatenate` keeps the rest of the signature intact."""
    result = _mypy(tmp_path, _SETUP + 'project.states.list(not_a_filter="x")\n')

    assert result.returncode != 0
    assert "not_a_filter" in result.stdout, result.stdout


def test_misspelled_field_on_a_loaded_row_is_a_type_error(tmp_path) -> None:
    """`Loaded.__getattr__` is hidden from type checkers for the same reason, so a
    field read resolves against the row model rather than collapsing to `Any`."""
    result = _mypy(tmp_path, _SETUP + "print(project.nmae)\n")

    assert result.returncode != 0
    assert 'has no attribute "nmae"' in result.stdout, result.stdout


# -- A newly navigable family (cycles) gets the same typed navigation ------------

_CYCLE_SETUP = _SETUP + 'cycle = v2.workspaces.projects.cycles.retrieve("acme", "ENG", "c1")\n'


def test_a_loaded_cycles_child_navigation_is_not_any(tmp_path) -> None:
    """`cycle.work_items` must carry the bridge resource's own type, not collapse to
    `Any`, now that cycles are wired onto the tree alongside work items."""
    result = _mypy(tmp_path, _CYCLE_SETUP + "reveal_type(cycle.work_items)\n")

    revealed = [line for line in result.stdout.splitlines() if "Revealed type" in line]
    assert len(revealed) == 1, result.stdout
    assert "Any" not in revealed[0], revealed[0]
    assert "_OwnedCycleWorkItems" in revealed[0], revealed[0]


def test_misspelled_method_on_a_loaded_cycles_child_is_a_type_error(tmp_path) -> None:
    result = _mypy(tmp_path, _CYCLE_SETUP + 'cycle.work_items.ad(["w1"])\n')

    assert result.returncode != 0
    assert 'has no attribute "ad"' in result.stdout, result.stdout
