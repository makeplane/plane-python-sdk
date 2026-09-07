"""Generic CRUD kernel. A resource declares a path and a model; the kernel does the rest."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from typing import Any, ClassVar, Generic, TypeVar
from urllib.parse import quote

from pydantic import BaseModel

from ....models.v2.common import BulkWriteResponse
from .._generated.constants import BULK_MAX_ITEMS, EXPAND, FIELDS, ORDER_BY
from .errors import MultipleMatchesFound, NoMatchFound
from .pagination import Page, iterate, parse_page
from .transport import V2Transport

TRead = TypeVar("TRead", bound=BaseModel)
TWrite = TypeVar("TWrite", bound=BaseModel)
TPatch = TypeVar("TPatch", bound=BaseModel)

BRIDGE_MAX_IDS = 100
"""Per-call id cap on membership bridges (`.../{parent}/work-items/` and friends): the
golden's manage schemas cap `add`/`remove` at 100 ids each."""

_BRIDGE_RESULT_KEYS = {"add": "added", "remove": "removed"}


def encode_fields(operation_id: str, fields: Any) -> str:
    """`["id", "name"]` -> `"id,name"`, rejecting names the operation does not offer."""
    if isinstance(fields, str):
        requested = [part.strip() for part in fields.split(",") if part.strip()]
    else:
        requested = [str(part) for part in fields]
    allowed = FIELDS.get(operation_id)
    if allowed is not None:
        unknown = [name for name in requested if name not in allowed]
        if unknown:
            raise ValueError(
                f"Unknown field(s) for {operation_id}: {', '.join(unknown)}. "
                f"Allowed: {', '.join(sorted(allowed))}."
            )
    return ",".join(requested)


def encode_expand(operation_id: str, expand: Any) -> str:
    """`["state", "labels"]` -> `"state,labels"`, rejecting relations the operation
    does not expand (same shape as `encode_fields`, per-operation enum)."""
    if isinstance(expand, str):
        requested = [part.strip() for part in expand.split(",") if part.strip()]
    else:
        requested = [str(part) for part in expand]
    allowed = EXPAND.get(operation_id)
    if allowed is not None:
        unknown = [name for name in requested if name not in allowed]
        if unknown:
            raise ValueError(
                f"Unknown expand value(s) for {operation_id}: {', '.join(unknown)}. "
                f"Allowed: {', '.join(sorted(allowed))}."
            )
    return ",".join(requested)


class V2Resource(Generic[TRead, TWrite, TPatch]):
    """Base for every api_v2 resource; subclasses set `path`, `model`, and `operations`
    (action name -> operationId, for `?fields=`/`?expand=` validation)."""

    path: ClassVar[str]
    model: ClassVar[type[BaseModel]]
    operations: ClassVar[dict[str, str]]
    bridge_path: ClassVar[str | None] = None
    """Where `_bridge` POSTs when the membership URL is not this resource's own `path`
    (a catalog resource like release labels bridges at `.../releases/{release_id}/labels/`)."""

    def __init__(self, transport: V2Transport) -> None:
        self.transport = transport

    # URL + params
    def _format_path(self, template: str, **path_params: Any) -> str:
        """Fill `template` from `path_params`, percent-encoding each value; `safe=""`
        stops a value from injecting extra URL segments."""
        return template.format_map(
            {key: quote(str(value), safe="") for key, value in path_params.items()}
        )

    def _collection_url(self, **path_params: Any) -> str:
        """Build the collection URL, percent-encoding every path param."""
        return self._format_path(self.path, **path_params)

    def _detail_url(self, pk: Any, **path_params: Any) -> str:
        base = self._collection_url(**path_params)
        return f"{base}{quote(str(pk), safe='')}/"

    def _query(self, params: Mapping[str, Any] | None, *, action: str) -> dict[str, Any]:
        """Drop Nones, join list values, and validate `fields`/`expand`/`order_by`
        against the golden, keyed by `action`'s own operationId."""
        prepared: dict[str, Any] = {}
        operation_id = self.operations.get(action)
        for key, value in (params or {}).items():
            if value is None:
                continue
            if key == "fields":
                if operation_id is None:
                    raise ValueError(
                        f"{type(self).__name__}.operations has no entry for {action!r}; "
                        "cannot validate `fields` for this action."
                    )
                prepared[key] = encode_fields(operation_id, value)
            elif key == "expand":
                if operation_id is None:
                    raise ValueError(
                        f"{type(self).__name__}.operations has no entry for {action!r}; "
                        "cannot validate `expand` for this action."
                    )
                prepared[key] = encode_expand(operation_id, value)
            elif key == "order_by":
                allowed = ORDER_BY.get(operation_id) if operation_id is not None else None
                if isinstance(value, list | tuple | set):
                    requested = [str(item) for item in value]
                    if allowed:
                        unknown = [item for item in requested if item not in allowed]
                        if unknown:
                            raise ValueError(
                                f"Unknown order_by {', '.join(unknown)} for {operation_id}. "
                                f"Allowed: {', '.join(sorted(allowed))}."
                            )
                    prepared[key] = ",".join(requested)
                else:
                    if allowed and value not in allowed:
                        raise ValueError(
                            f"Unknown order_by {value!r} for {operation_id}. "
                            f"Allowed: {', '.join(sorted(allowed))}."
                        )
                    prepared[key] = value
            elif isinstance(value, list | tuple | set):
                prepared[key] = ",".join(str(item) for item in value)
            else:
                prepared[key] = value
        return prepared

    # Actions
    def _list(self, *, params: Mapping[str, Any] | None = None, **path_params: Any) -> Page[TRead]:
        payload = self.transport.request(
            "GET",
            self._collection_url(**path_params),
            params=self._query(params, action="list"),
        )
        return parse_page(payload, self.model)  # type: ignore[arg-type]

    def _iter(
        self, *, params: Mapping[str, Any] | None = None, **path_params: Any
    ) -> Iterator[TRead]:
        url = self._collection_url(**path_params)

        def fetch(query: dict[str, Any]) -> Page[TRead]:
            payload = self.transport.request("GET", url, params=query)
            return parse_page(payload, self.model)  # type: ignore[arg-type]

        return iterate(fetch, self._query(params, action="list"))

    def _retrieve(
        self, *, pk: Any, params: Mapping[str, Any] | None = None, **path_params: Any
    ) -> TRead:
        payload = self.transport.request(
            "GET",
            self._detail_url(pk, **path_params),
            params=self._query(params, action="retrieve"),
        )
        return self.model.model_validate(payload)  # type: ignore[return-value]

    def _create(
        self, data: TWrite, *, params: Mapping[str, Any] | None = None, **path_params: Any
    ) -> TRead:
        payload = self.transport.request(
            "POST",
            self._collection_url(**path_params),
            params=self._query(params, action="create"),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return self.model.model_validate(payload)  # type: ignore[return-value]

    def _update(
        self, data: TPatch, *, pk: Any, params: Mapping[str, Any] | None = None, **path_params: Any
    ) -> TRead:
        payload = self.transport.request(
            "PATCH",
            self._detail_url(pk, **path_params),
            params=self._query(params, action="update"),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return self.model.model_validate(payload)  # type: ignore[return-value]

    def _delete(self, *, pk: Any, **path_params: Any) -> None:
        self.transport.request("DELETE", self._detail_url(pk, **path_params))
        return None

    def _upsert(
        self, data: TWrite, *, params: Mapping[str, Any] | None = None, **path_params: Any
    ) -> TRead:
        """Create, or reconcile an existing row on (external_source, external_id)."""
        payload = self.transport.request(
            "POST",
            f"{self._collection_url(**path_params)}upsert/",
            params=self._query(params, action="upsert"),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return self.model.model_validate(payload)  # type: ignore[return-value]

    def _action(
        self,
        name: str,
        *,
        pk: Any,
        data: BaseModel | None = None,
        params: Mapping[str, Any] | None = None,
        **path_params: Any,
    ) -> TRead:
        """POST a custom single-row verb action (`{detail_url}{name}/`), parsing the
        row as `model`; `name` also keys `operations` for `fields`/`expand` validation."""
        payload = self.transport.request(
            "POST",
            f"{self._detail_url(pk, **path_params)}{name}/",
            params=self._query(params, action=name),
            json=data.model_dump(mode="json", exclude_none=True) if data is not None else None,
        )
        return self.model.model_validate(payload)  # type: ignore[return-value]

    def _batch(self, action: str, body: dict[str, Any], **path_params: Any) -> BulkWriteResponse:
        payload = self.transport.request(
            "POST", f"{self._collection_url(**path_params)}{action}/", json=body
        )
        return BulkWriteResponse.model_validate(payload)

    @staticmethod
    def _check_cap(count: int, *, empty_detail: str) -> None:
        """Reject an empty or over-cap batch before it reaches the wire.

        `empty_detail` echoes the API's own per-endpoint wording for the empty case."""
        if count == 0:
            raise ValueError(empty_detail)
        if count > BULK_MAX_ITEMS:
            raise ValueError(f"At most {BULK_MAX_ITEMS} items per call (received {count}).")

    def _bulk_create(
        self, items: list[TWrite], *, all_or_none: bool = False, **path_params: Any
    ) -> BulkWriteResponse:
        self._check_cap(len(items), empty_detail="Provide a non-empty list of write bodies.")
        return self._batch(
            "bulk-create",
            {
                "items": [item.model_dump(mode="json", exclude_none=True) for item in items],
                "all_or_none": all_or_none,
            },
            **path_params,
        )

    def _bulk_update(
        self, items: list[Mapping[str, Any]], *, all_or_none: bool = False, **path_params: Any
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`. Human keys are rejected."""
        self._check_cap(
            len(items), empty_detail="Provide a non-empty list of write bodies, each with an id."
        )
        return self._batch(
            "bulk-update",
            {"items": [dict(item) for item in items], "all_or_none": all_or_none},
            **path_params,
        )

    def _bulk_delete(
        self, ids: list[str], *, all_or_none: bool = False, **path_params: Any
    ) -> BulkWriteResponse:
        self._check_cap(len(ids), empty_detail="Provide a non-empty list of ids.")
        return self._batch(
            "bulk-delete", {"ids": list(ids), "all_or_none": all_or_none}, **path_params
        )

    def _bridge(self, *, key: str, ids: Sequence[Any], **path_params: Any) -> list[str]:
        """One side of a membership bridge: POST `{key: [...]}` (`key` is `"add"` or
        `"remove"`) to `bridge_path` (or `path`) and return the ids the server reports
        as actually changed -- `added` for `add`, `removed` for `remove`, `[]` when the
        key is absent. Entries may be plain ids or pydantic rows (serialized with
        `exclude_none`). 0 or more than `BRIDGE_MAX_IDS` entries raise `ValueError`
        before any request is sent."""
        try:
            result_key = _BRIDGE_RESULT_KEYS[key]
        except KeyError:
            raise ValueError(f"Bridge key must be 'add' or 'remove', not {key!r}.") from None
        entries = list(ids)
        if not entries:
            raise ValueError(f"Provide at least one id to {key}.")
        if len(entries) > BRIDGE_MAX_IDS:
            raise ValueError(f"At most {BRIDGE_MAX_IDS} ids per call (received {len(entries)}).")
        body = [
            (
                entry.model_dump(mode="json", exclude_none=True)
                if isinstance(entry, BaseModel)
                else entry
            )
            for entry in entries
        ]
        url = self._format_path(self.bridge_path or self.path, **path_params)
        payload = self.transport.request("POST", url, json={key: body})
        return list(payload.get(result_key) or [])

    def _find_one(self, *, filters: Mapping[str, Any], **path_params: Any) -> TRead:
        """Resolve exactly one row by identity filter, or raise.

        Requests `per_page=2` to distinguish "no match" from "ambiguous" in one call."""
        page = self._list(params={**filters, "per_page": 2, "count": False}, **path_params)
        described = ", ".join(f"{key}={value!r}" for key, value in filters.items())
        if not page.data:
            raise NoMatchFound(f"No {type(self).__name__} matched {described}.")
        if len(page.data) > 1:
            raise MultipleMatchesFound(
                f"Multiple rows matched {described}; "
                f"use the id instead, or list with the "
                f"same filter to see every match."
            )
        return page.data[0]
