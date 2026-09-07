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


def _generate(root: pathlib.Path, output_dir: pathlib.Path) -> str:
    """Invoke the generator against `root`, writing to `output_dir` (never the real,
    committed `plane/api/v2/_generated/constants.py`) and return the generated source.

    The generator's output path is hardcoded unless an explicit second CLI argument is
    given -- always pass one here so running this file can never clobber the committed
    file as a side effect."""
    subprocess.run(
        [sys.executable, "scripts/generate_v2_constants.py", str(root), str(output_dir)],
        check=True,
    )
    return (output_dir / "constants.py").read_text()


def test_emits_literal_field_alias(tmp_path: pathlib.Path) -> None:
    root = _write_golden(tmp_path)
    generated = _generate(root, tmp_path / "out")

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

    generated = _generate(root, tmp_path / "out")

    assert "class StatesListFilters(TypedDict, total=False):" in generated
    assert "    name: str" in generated
    assert "    is_default: bool" in generated
    assert "    per_page:" not in generated


def test_emits_sequence_type_for_array_filter(tmp_path: pathlib.Path) -> None:
    """An `array`-typed query parameter (the golden's `style: form, explode: false` `__in`
    filters) must become `Sequence[<item type>]`, not fall through the type map to `str`."""
    root = _write_golden(tmp_path)
    states = root / "paths" / "states.json"
    document = json.loads(states.read_text())
    operation = document["/api/v2/workspaces/{slug}/projects/{project_id}/states/"]["get"]
    operation["parameters"] += [
        {
            "name": "group__in",
            "in": "query",
            "schema": {"type": "array", "items": {"type": "string"}},
        },
        {
            "name": "sequence__in",
            "in": "query",
            "schema": {"type": "array", "items": {"type": "integer"}},
        },
        {
            "name": "untyped_items__in",
            "in": "query",
            "schema": {"type": "array", "items": {}},
        },
    ]
    states.write_text(json.dumps(document))

    generated = _generate(root, tmp_path / "out")

    assert "    group__in: Sequence[str]" in generated
    assert "    sequence__in: Sequence[int]" in generated
    assert "    untyped_items__in: str" in generated


def test_generation_never_writes_the_real_generated_module(tmp_path: pathlib.Path) -> None:
    """The committed `plane/api/v2/_generated/constants.py` must be untouched by this file --
    a regression check on the output-dir wiring itself, since a hardcoded path here would
    silently corrupt a developer's working tree on every `pytest tests/scripts` run."""
    real_path = pathlib.Path("plane/api/v2/_generated/constants.py")
    before = real_path.read_bytes()

    root = _write_golden(tmp_path)
    _generate(root, tmp_path / "out")

    assert real_path.read_bytes() == before
