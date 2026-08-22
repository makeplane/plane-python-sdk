"""Dummy `V2Resource` nested two packages deep; proves discovery recurses via
`pkgutil.walk_packages`, not just the top level."""

from __future__ import annotations

from plane.api.v2._kernel.resource import V2Resource
from plane.models.v2.states import CreateState, State, UpdateState


class DummyNestedResource(V2Resource[State, CreateState, UpdateState]):
    path = "/workspaces/{slug}/projects/{project_id}/states/"
    model = State
    operations = {"list": "states_list"}
