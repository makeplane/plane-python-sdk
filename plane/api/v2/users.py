"""The calling principal (api_v2). Workspace-less singleton -- `path` has no
`{slug}` segment at all, unlike every other v2 resource."""

from __future__ import annotations

from ...models.v2.users import WhoAmI
from ._kernel.resource import V2Resource


class Users(V2Resource[WhoAmI, WhoAmI, WhoAmI]):
    path = "/users/me/"
    model = WhoAmI
    # No `fields=` support on this operation -- it is not in the golden's FIELDS
    # map at all.
    operations = {
        "me": "users_me_retrieve",
    }

    def me(self) -> WhoAmI:
        """The authenticated principal behind the current request. OAuth tokens
        need a read scope (API keys bypass scope checks).

        `_retrieve_singleton`, because `/users/me/` *is* the row -- there is no pk to
        append, the way there is none for a workspace or a feature-toggle set."""
        return self._retrieve_singleton(action="me")
