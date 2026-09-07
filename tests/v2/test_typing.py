import subprocess
import sys
import textwrap


def test_unknown_filter_is_a_type_error(tmp_path) -> None:
    script = tmp_path / "probe.py"
    script.write_text(
        textwrap.dedent(
            """
            from plane.api.v2 import V2Namespace
            from plane.config import Configuration

            v2 = V2Namespace(Configuration(base_path="https://x", api_key="k"))
            v2.workspaces.projects.states.list("acme", "ENG", not_a_filter="x")
            """
        )
    )
    result = subprocess.run(
        [sys.executable, "-m", "mypy", str(script)], capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "not_a_filter" in result.stdout
