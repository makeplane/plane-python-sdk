import json
import pathlib
import subprocess
import sys


def _write_golden(tmp_path: pathlib.Path) -> pathlib.Path:
    root = tmp_path / "openapi"
    (root / "paths").mkdir(parents=True)
    (root / "root.json").write_text(json.dumps({"info": {"version": "2.0.0"}}))
    (root / "components.json").write_text(
        json.dumps(
            {
                "schemas": {
                    "BulkDeleteRequest": {"properties": {"ids": {"maxItems": 50}}},
                    "ProblemDetail": {"properties": {"code": {"x-enum": ["not_found"]}}},
                }
            }
        )
    )
    (root / "paths" / "states.json").write_text(
        json.dumps(
            {
                "/api/v2/workspaces/{slug}/projects/{project_id}/states/": {
                    "get": {
                        "operationId": "states_list",
                        "parameters": [
                            {"name": "fields", "in": "query",
                             "schema": {"type": "string", "enum": ["all", "id", "name"]}},
                            {"name": "order_by", "in": "query",
                             "schema": {"type": "string", "enum": ["name", "-name"]}},
                        ],
                    }
                }
            }
        )
    )
    return root


def test_emits_literal_field_alias(tmp_path: pathlib.Path) -> None:
    root = _write_golden(tmp_path)
    subprocess.run([sys.executable, "scripts/generate_v2_constants.py", str(root)], check=True)
    generated = pathlib.Path("plane/api/v2/_generated/constants.py").read_text()

    assert 'StatesListField = Literal["all", "id", "name"]' in generated
    assert 'StatesListOrderBy = Literal["-name", "name"]' in generated


def test_emits_filters_typeddict(tmp_path: pathlib.Path) -> None:
    root = _write_golden(tmp_path)
    states = root / "paths" / "states.json"
    document = json.loads(states.read_text())
    operation = document["/api/v2/workspaces/{slug}/projects/{project_id}/states/"]["get"]
    operation["parameters"] += [
        {"name": "name", "in": "query", "schema": {"type": "string"}},
        {"name": "is_default", "in": "query", "schema": {"type": "boolean"}},
        {"name": "per_page", "in": "query", "schema": {"type": "integer"}},
    ]
    states.write_text(json.dumps(document))

    subprocess.run([sys.executable, "scripts/generate_v2_constants.py", str(root)], check=True)
    generated = pathlib.Path("plane/api/v2/_generated/constants.py").read_text()

    assert "class StatesListFilters(TypedDict, total=False):" in generated
    assert "    name: str" in generated
    assert "    is_default: bool" in generated
    assert "    per_page:" not in generated


def test_display_name_filter_survives_regeneration_from_the_real_golden() -> None:
    """Regression pin on the *committed* output (not a fixture): a golden regenerated from a
    stale branch can silently drop a real, shipped query parameter (`display_name` on the
    property list operations) without any fixture-based test noticing. This reads the real
    committed `constants.py` and asserts the field is still there."""
    generated = pathlib.Path("plane/api/v2/_generated/constants.py").read_text()

    marker = "class WorkItemPropertiesListFilters(TypedDict, total=False):"
    start = generated.index(marker)
    end = generated.index("\n\n", start)
    block = generated[start:end]

    assert "    display_name: str" in block, (
        "WorkItemPropertiesListFilters is missing `display_name: str` -- the golden used to "
        "regenerate constants.py is stale (predates the display_name query parameter shipping "
        "on the property list operations)."
    )
