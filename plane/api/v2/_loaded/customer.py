"""A fetched customer row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.customers import Customer
from .._kernel.loaded import Loaded, Owned, bind2

if TYPE_CHECKING:
    from ..customers.customers import Customers
    from ..customers.property_values import CustomerPropertyValues
    from ..customers.requests import CustomerRequests
    from ..customers.work_items import CustomerWorkItems

    # Typed views on `Owned`: the child resource's own methods with `slug` and
    # `customer` already supplied -- `bind2`, because two path ids are bound.
    # Evaluated only by a type checker -- at runtime these properties return a
    # plain `Owned`.

    class _OwnedCustomerRequests(Owned["CustomerRequests"]):
        list = staticmethod(bind2(CustomerRequests.list))
        iterate = staticmethod(bind2(CustomerRequests.iterate))
        retrieve = staticmethod(bind2(CustomerRequests.retrieve))
        create = staticmethod(bind2(CustomerRequests.create))
        update = staticmethod(bind2(CustomerRequests.update))
        delete = staticmethod(bind2(CustomerRequests.delete))

    class _OwnedCustomerPropertyValues(Owned["CustomerPropertyValues"]):
        list = staticmethod(bind2(CustomerPropertyValues.list))
        create = staticmethod(bind2(CustomerPropertyValues.create))

    class _OwnedCustomerWorkItems(Owned["CustomerWorkItems"]):
        add = staticmethod(bind2(CustomerWorkItems.add))
        remove = staticmethod(bind2(CustomerWorkItems.remove))


class LoadedCustomer(Loaded, Customer):
    """A customer row that is also the place its children live."""

    model_config = {**Customer.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Customers._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Customers

    @property
    def requests(self) -> _OwnedCustomerRequests:
        return cast(
            "_OwnedCustomerRequests", Owned(self._resources.requests, self._ids, self._id_names)
        )

    @property
    def property_values(self) -> _OwnedCustomerPropertyValues:
        return cast(
            "_OwnedCustomerPropertyValues",
            Owned(self._resources.property_values, self._ids, self._id_names),
        )

    @property
    def work_items(self) -> _OwnedCustomerWorkItems:
        return cast(
            "_OwnedCustomerWorkItems", Owned(self._resources.work_items, self._ids, self._id_names)
        )
