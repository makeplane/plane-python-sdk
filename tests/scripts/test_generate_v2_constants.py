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
