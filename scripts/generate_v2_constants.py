"""Regenerates `plane/api/v2/_generated/constants.py` from the api_v2 OpenAPI golden; rerun via
`python scripts/generate_v2_constants.py <path-to-openapi-dir>`."""

import json
import pathlib
import sys
from typing import Any

HEADER_TEMPLATE = '''\
"""Generated from the api_v2 OpenAPI golden (version {api_version}) -- never hand-edited.
Source: {source_dir}
Regenerate: python scripts/generate_v2_constants.py <path-to>/api_v2/core/schema/openapi"""

from typing import Literal

from typing_extensions import TypedDict
'''

LINE_LENGTH = 100

_RESERVED_QUERY_PARAMS = frozenset(
    {"fields", "expand", "order_by", "offset", "per_page", "paginate", "count"}
)

_JSON_TO_PYTHON = {"string": "str", "integer": "int", "boolean": "bool", "number": "float"}


def _camel(operation_id: str) -> str:
    """`states_list` -> `StatesList`."""
    return "".join(part.title() for part in operation_id.split("_"))


def _literal_aliases(fields: dict[str, list[str]], order_by: dict[str, list[str]]) -> str:
    lines: list[str] = []
    for operation_id in sorted(fields):
        values = ", ".join(json.dumps(value) for value in sorted(fields[operation_id]))
        lines.append(f"{_camel(operation_id)}Field = Literal[{values}]")
    for operation_id in sorted(order_by):
        values = ", ".join(json.dumps(value) for value in sorted(order_by[operation_id]))
        lines.append(f"{_camel(operation_id)}OrderBy = Literal[{values}]")
    return "\n".join(lines)


def _filters_typeddicts(operations: dict[str, list[dict[str, Any]]]) -> str:
    """One `TypedDict(total=False)` per list operation, from its non-reserved query params."""
    blocks: list[str] = []
    for operation_id in sorted(operations):
        entries = []
        for parameter in operations[operation_id]:
            name = parameter.get("name")
            if parameter.get("in") != "query" or name in _RESERVED_QUERY_PARAMS:
                continue
            hint = _JSON_TO_PYTHON.get(parameter.get("schema", {}).get("type", "string"), "str")
            entries.append(f"    {name}: {hint}")
        if not entries:
            continue
        body = "\n".join(sorted(entries))
        blocks.append(f"class {_camel(operation_id)}Filters(TypedDict, total=False):\n{body}")
    return "\n\n\n".join(blocks)


def _format(source: str) -> str:
    """Format generated source with Black so the committed file matches what this
    command alone produces — no separate formatting step for a maintainer to forget.
    """
    try:
        import black
    except ImportError as exc:
        raise SystemExit(
            "generate_v2_constants: black is required to format the generated file "
            "but is not installed in this interpreter. Run `pip install -r requirements.txt` "
            "and retry."
        ) from exc

    mode = black.Mode(line_length=LINE_LENGTH)
    try:
        return black.format_str(source, mode=mode)
    except Exception as exc:
        raise SystemExit(f"generate_v2_constants: black failed to format output: {exc}") from exc


def main(openapi_dir: str) -> None:
    root = pathlib.Path(openapi_dir)

    root_document = json.loads((root / "root.json").read_text())
    api_version = root_document.get("info", {}).get("version")
    if not api_version:
        raise SystemExit(
            "generate_v2_constants: root.json has no info.version — "
            "the golden's shape changed, update this generator before trusting its output."
        )

    paths: dict[str, dict[str, Any]] = {}
    for shard in sorted((root / "paths").glob("*.json")):
        document = json.loads(shard.read_text())
        paths.update(document.get("paths", document))

    operation_ids: set[str] = set()
    fields: dict[str, list[str]] = {}
    order_by: dict[str, list[str]] = {}
    expand: dict[str, list[str]] = {}
    operation_parameters: dict[str, list[dict[str, Any]]] = {}
    for operations in paths.values():
        for method, operation in operations.items():
            if method not in {"get", "post", "patch", "delete", "put"}:
                continue
            operation_id = operation.get("operationId")
            if not operation_id:
                continue
            operation_ids.add(operation_id)
            operation_parameters[operation_id] = operation.get("parameters", [])
            for parameter in operation.get("parameters", []):
                enum = parameter.get("schema", {}).get("enum")
                if not enum:
                    continue
                if parameter["name"] == "fields":
                    fields[operation_id] = sorted(enum)
                elif parameter["name"] == "order_by":
                    order_by[operation_id] = sorted(enum)
                elif parameter["name"] == "expand":
                    expand[operation_id] = sorted(enum)

    components = json.loads((root / "components.json").read_text())["schemas"]

    delete_request = components.get("BulkDeleteRequest")
    if delete_request is None:
        raise SystemExit(
            "generate_v2_constants: components.json has no 'BulkDeleteRequest' schema — "
            "the golden's shape changed, update this generator before trusting its output."
        )
    bulk_max = delete_request.get("properties", {}).get("ids", {}).get("maxItems")
    if bulk_max is None:
        raise SystemExit(
            "generate_v2_constants: BulkDeleteRequest.properties.ids.maxItems is missing — "
            "the golden's shape changed, update this generator before trusting its output."
        )

    problem_detail = components.get("ProblemDetail")
    if problem_detail is None:
        raise SystemExit(
            "generate_v2_constants: components.json has no 'ProblemDetail' schema — "
            "the golden's shape changed, update this generator before trusting its output."
        )
    codes = sorted(problem_detail.get("properties", {}).get("code", {}).get("x-enum", []))
    if not codes:
        raise SystemExit(
            "generate_v2_constants: ProblemDetail.properties.code.x-enum is empty — "
            "the golden's shape changed, update this generator before trusting its output."
        )

    # Record the argument as passed, not resolved to an absolute path: this keeps
    # regeneration byte-identical regardless of the caller's cwd, and matches the
    # relative form the module's own usage example recommends.
    header = HEADER_TEMPLATE.format(source_dir=openapi_dir, api_version=api_version)
    lines = [
        header,
        f"API_VERSION = {api_version!r}\n\n",
        f"BULK_MAX_ITEMS = {bulk_max}\n\n",
        "OPERATION_IDS: frozenset[str] = frozenset(\n",
        f"    {sorted(operation_ids)!r}\n",
        ")\n\n",
        "FIELDS: dict[str, frozenset[str]] = {\n",
    ]
    for operation_id, values in sorted(fields.items()):
        lines.append(f"    {operation_id!r}: frozenset({values!r}),\n")
    lines.append("}\n\nORDER_BY: dict[str, frozenset[str]] = {\n")
    for operation_id, values in sorted(order_by.items()):
        lines.append(f"    {operation_id!r}: frozenset({values!r}),\n")
    lines.append("}\n\nEXPAND: dict[str, frozenset[str]] = {\n")
    for operation_id, values in sorted(expand.items()):
        lines.append(f"    {operation_id!r}: frozenset({values!r}),\n")
    lines.append("}\n\n")
    lines.append(f"ERROR_CODES: frozenset[str] = frozenset({codes!r})\n\n")
    lines.append(_literal_aliases(fields, order_by))
    lines.append("\n\n")
    lines.append(_filters_typeddicts(operation_parameters))
    lines.append("\n")

    content = _format("".join(lines))

    target = pathlib.Path(__file__).parent.parent / "plane" / "api" / "v2" / "_generated"
    target.mkdir(parents=True, exist_ok=True)
    (target / "__init__.py").write_text("")
    (target / "constants.py").write_text(content)
    print(
        f"wrote {len(operation_ids)} operation ids, {len(fields)} field enums, "
        f"{len(order_by)} order_by enums, {len(expand)} expand enums, bulk_max={bulk_max}, "
        f"{len(codes)} error codes, api_version={api_version}"
    )


if __name__ == "__main__":
    main(sys.argv[1])
