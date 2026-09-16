"""Live coverage for the `.work_items` bridge (api_v2): add/remove link-management
between a module and its work items; offline coverage lives in `tests/v2`.

Reached off the loaded module, which is where a bridge belongs -- including the
client-side `maxItems` rejection, which must happen before the request either way."""

from __future__ import annotations

from typing import Any

import pytest

from plane.api.v2 import LoadedProject
from plane.models.v2.modules import CreateModule

from .helpers import unique_name


@pytest.fixture
def module(project: LoadedProject) -> Any:
    """The loaded row, not a `model_dump()` of it -- dumping it threw away the very
    navigation this file is about."""
    return project.modules.create(CreateModule(name=unique_name("module")))


class TestModuleWorkItems:
    def test_work_items_add_then_remove(
        self,
        module: Any,
        work_item: Any,
    ) -> None:
        added = module.work_items.add([work_item.id])
        assert work_item.id in added

        removed = module.work_items.remove([work_item.id])
        assert work_item.id in removed

    def test_work_items_add_over_100_ids_is_rejected_client_side(
        self,
        module: Any,
    ) -> None:
        """The bridge kernel enforces the golden's `maxItems: 100` before the
        request is ever sent -- this never reaches the server."""
        with pytest.raises(ValueError):
            module.work_items.add([f"00000000-0000-0000-0000-{i:012d}" for i in range(101)])
