"""Dummy `V2Resource` under an underscore-prefixed subpackage; must stay excluded from discovery
even when the walk recurses."""

from __future__ import annotations

from plane.api.v2._kernel.resource import V2Resource
from plane.models.v2.states import CreateState, State, UpdateState


class ShouldNotBeDiscovered(V2Resource[State, CreateState, UpdateState]):
    path = "/workspaces/{slug}/projects/{project_id}/states/"
    model = State
    operations = {"list": "not_a_real_operation_id"}
