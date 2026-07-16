"""Unit tests for Customers API resource (smoke tests with real HTTP requests)."""

import re
import time
import unicodedata
import uuid

import pytest

from plane.client import PlaneClient
from plane.errors.errors import HttpError
from plane.models.customers import (
    CreateCustomer,
    CreateCustomerProperty,
    CreateCustomerPropertyOption,
    CreateCustomerRequest,
    LinkCustomerWorkItems,
    SetCustomerPropertyValue,
    SetCustomerPropertyValues,
    UpdateCustomer,
    UpdateCustomerProperty,
    UpdateCustomerPropertyOption,
    UpdateCustomerRequest,
)
from plane.models.enums import PropertyType
from plane.models.projects import Project
from plane.models.work_item_property_configurations import TextAttributeSettings
from plane.models.work_items import CreateWorkItem


def _unique(prefix: str) -> str:
    """Build a name that will not collide with other runs."""
    return f"{prefix} {int(time.time() * 1000)}_{uuid.uuid4().hex[:6]}"


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


class TestCustomersAPI:
    """Test Customers API resource."""

    def test_list_customers(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing customers."""
        response = client.customers.list(workspace_slug)
        assert response is not None
        assert hasattr(response, "results")
        assert hasattr(response, "count")
        assert isinstance(response.results, list)

    def test_list_customers_with_params(self, client: PlaneClient, workspace_slug: str) -> None:
        """The page size is honoured. The paginator reads `per_page`, not `limit`."""
        response = client.customers.list(workspace_slug, params={"per_page": 2})
        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) <= 2

    def test_list_customers_paginates(self, client: PlaneClient, workspace_slug: str) -> None:
        """A workspace holding more customers than a page reports the rest."""
        response = client.customers.list(workspace_slug, params={"per_page": 1})
        if response.total_count > 1:
            assert len(response.results) == 1
            assert response.next_page_results is True


class TestCustomersAPICRUD:
    """Test Customers API CRUD operations."""

    @pytest.fixture
    def customer_data(self) -> CreateCustomer:
        """Create test customer data."""
        return CreateCustomer(
            name=_unique("Test Customer"),
            email=f"test{int(time.time())}@example.com",
        )

    @pytest.fixture
    def customer(self, client: PlaneClient, workspace_slug: str, customer_data: CreateCustomer):
        """Create a test customer and yield it, then delete it."""
        customer = client.customers.create(workspace_slug, customer_data)
        yield customer
        try:
            client.customers.delete(workspace_slug, customer.id)
        except Exception:
            pass

    def test_create_customer(
        self, client: PlaneClient, workspace_slug: str, customer_data: CreateCustomer
    ) -> None:
        """Test creating a customer."""
        customer = client.customers.create(workspace_slug, customer_data)
        assert customer is not None
        assert customer.id is not None
        assert customer.name == customer_data.name

        # Cleanup
        try:
            client.customers.delete(workspace_slug, customer.id)
        except Exception:
            pass

    def test_retrieve_customer(self, client: PlaneClient, workspace_slug: str, customer) -> None:
        """Test retrieving a customer."""
        retrieved = client.customers.retrieve(workspace_slug, customer.id)
        assert retrieved is not None
        assert retrieved.id == customer.id
        assert retrieved.name == customer.name

    def test_update_customer(self, client: PlaneClient, workspace_slug: str, customer) -> None:
        """Test updating a customer."""
        new_name = _unique("Updated Customer")
        update_data = UpdateCustomer(name=new_name)
        updated = client.customers.update(workspace_slug, customer.id, update_data)
        assert updated is not None
        assert updated.id == customer.id
        assert updated.name == new_name

    def test_create_customer_with_full_payload(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Every field the create endpoint accepts survives the round trip."""
        data = CreateCustomer(
            name=_unique("Full Customer"),
            description_html="<p>A customer</p>",
            email="full@example.com",
            website_url="https://example.com",
            domain="example.com",
            employees=42,
            stage="lead",
            contract_status="active",
            revenue="1000000",
        )
        customer = client.customers.create(workspace_slug, data)
        try:
            assert customer.name == data.name
            assert customer.email == data.email
            assert customer.domain == data.domain
            assert customer.employees == 42
            assert customer.revenue == "1000000"
        finally:
            try:
                client.customers.delete(workspace_slug, customer.id)
            except Exception:
                pass

    def test_delete_customer(self, client: PlaneClient, workspace_slug: str) -> None:
        """A deleted customer is gone."""
        customer = client.customers.create(workspace_slug, CreateCustomer(name=_unique("Doomed")))
        client.customers.delete(workspace_slug, customer.id)

        with pytest.raises(HttpError):
            client.customers.retrieve(workspace_slug, customer.id)


class TestCustomersUpsert:
    """The create endpoint upserts rather than always creating."""

    def test_create_with_same_name_updates_existing(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Creating twice under one name returns the same customer, updated."""
        name = _unique("Upsert By Name")
        first = client.customers.create(workspace_slug, CreateCustomer(name=name, employees=1))
        try:
            second = client.customers.create(
                workspace_slug, CreateCustomer(name=name, employees=99)
            )
            assert second.id == first.id
            assert second.employees == 99
        finally:
            try:
                client.customers.delete(workspace_slug, first.id)
            except Exception:
                pass

    def test_create_with_same_external_ref_updates_existing(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """An external reference matches an existing customer even under a new name."""
        external_id = uuid.uuid4().hex
        first = client.customers.create(
            workspace_slug,
            CreateCustomer(
                name=_unique("External A"),
                external_source="pytest",
                external_id=external_id,
            ),
        )
        try:
            renamed = _unique("External B")
            second = client.customers.create(
                workspace_slug,
                CreateCustomer(
                    name=renamed,
                    external_source="pytest",
                    external_id=external_id,
                ),
            )
            assert second.id == first.id
            assert second.name == renamed
        finally:
            try:
                client.customers.delete(workspace_slug, first.id)
            except Exception:
                pass

    def test_delete_by_external_id(self, client: PlaneClient, workspace_slug: str) -> None:
        """A customer can be deleted through its external reference."""
        external_id = uuid.uuid4().hex
        customer = client.customers.create(
            workspace_slug,
            CreateCustomer(
                name=_unique("External Delete"),
                external_source="pytest",
                external_id=external_id,
            ),
        )
        client.customers.delete_by_external_id(workspace_slug, "pytest", external_id)

        with pytest.raises(HttpError):
            client.customers.retrieve(workspace_slug, customer.id)

    def test_delete_by_unknown_external_id_is_silent(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Deleting an external reference that matches nothing does not raise."""
        client.customers.delete_by_external_id(workspace_slug, "pytest", uuid.uuid4().hex)


@pytest.fixture
def customer(client: PlaneClient, workspace_slug: str):
    """A customer shared by the request, issue and property-value tests."""
    customer = client.customers.create(workspace_slug, CreateCustomer(name=_unique("Customer")))
    yield customer
    try:
        client.customers.delete(workspace_slug, customer.id)
    except Exception:
        pass


class TestCustomerProperties:
    """Test customer property operations."""

    @pytest.fixture
    def text_property(self, client: PlaneClient, workspace_slug: str):
        """A workspace-level TEXT property, torn down after the test."""
        prop = client.customers.properties.create(
            workspace_slug,
            CreateCustomerProperty(
                name="ignored",
                display_name=_unique("Tier"),
                property_type=PropertyType.TEXT,
                settings=TextAttributeSettings(display_format="single-line"),
            ),
        )
        yield prop
        try:
            client.customers.properties.delete(workspace_slug, prop.id)
        except Exception:
            pass

    def test_list_properties(self, client: PlaneClient, workspace_slug: str) -> None:
        """Listing properties returns a paginated response."""
        response = client.customers.properties.list(workspace_slug)
        assert hasattr(response, "results")
        assert isinstance(response.results, list)

    def test_create_text_property(self, client: PlaneClient, workspace_slug: str, text_property):
        """A TEXT property carries its settings."""
        assert text_property.id is not None
        assert text_property.property_type == PropertyType.TEXT
        assert text_property.display_name.startswith("Tier")

    def test_name_is_slugified_display_name(
        self, client: PlaneClient, workspace_slug: str, text_property
    ) -> None:
        """The stored name is the slug of display_name, not the name that was sent."""
        assert text_property.name == slugify(text_property.display_name)
        assert text_property.name != "ignored"

    def test_created_property_appears_in_list(
        self, client: PlaneClient, workspace_slug: str, text_property
    ) -> None:
        """A created property is listed."""
        response = client.customers.properties.list(workspace_slug)
        assert text_property.id in [p.id for p in response.results]

    def test_retrieve_property(self, client: PlaneClient, workspace_slug: str, text_property):
        """A property can be fetched by id."""
        retrieved = client.customers.properties.retrieve(workspace_slug, text_property.id)
        assert retrieved.id == text_property.id

    def test_update_property(self, client: PlaneClient, workspace_slug: str, text_property):
        """display_name is updatable, and re-slugs the stored name with it."""
        new_display_name = _unique("Updated Tier")
        updated = client.customers.properties.update(
            workspace_slug,
            text_property.id,
            UpdateCustomerProperty(display_name=new_display_name),
        )
        assert updated.display_name == new_display_name
        assert updated.name == slugify(new_display_name)

    def test_create_option_property_with_options(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """An OPTION property is created together with its options."""
        prop = client.customers.properties.create(
            workspace_slug,
            CreateCustomerProperty(
                name="ignored",
                display_name=_unique("Segment"),
                property_type=PropertyType.OPTION,
                options=[
                    CreateCustomerPropertyOption(name="SMB", is_default=True),
                    CreateCustomerPropertyOption(name="Enterprise"),
                ],
            ),
        )
        try:
            assert prop.options is not None
            assert {o.name for o in prop.options} == {"SMB", "Enterprise"}
        finally:
            try:
                client.customers.properties.delete(workspace_slug, prop.id)
            except Exception:
                pass

    def test_update_option_property_adds_option(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """An option can be appended to an existing OPTION property."""
        prop = client.customers.properties.create(
            workspace_slug,
            CreateCustomerProperty(
                name="ignored",
                display_name=_unique("Segment"),
                property_type=PropertyType.OPTION,
                options=[CreateCustomerPropertyOption(name="SMB")],
            ),
        )
        try:
            updated = client.customers.properties.update(
                workspace_slug,
                prop.id,
                UpdateCustomerProperty(options=[UpdateCustomerPropertyOption(name="Mid-Market")]),
            )
            assert "Mid-Market" in {o.name for o in (updated.options or [])}
        finally:
            try:
                client.customers.properties.delete(workspace_slug, prop.id)
            except Exception:
                pass

    def test_delete_property(self, client: PlaneClient, workspace_slug: str) -> None:
        """A deleted property is gone."""
        prop = client.customers.properties.create(
            workspace_slug,
            CreateCustomerProperty(
                name="ignored",
                display_name=_unique("Doomed"),
                property_type=PropertyType.TEXT,
                settings=TextAttributeSettings(display_format="single-line"),
            ),
        )
        client.customers.properties.delete(workspace_slug, prop.id)

        with pytest.raises(HttpError):
            client.customers.properties.retrieve(workspace_slug, prop.id)

    def test_text_property_requires_settings(self) -> None:
        """A TEXT property without settings is rejected before it reaches the API."""
        with pytest.raises(ValueError, match="TextAttributeSettings is required"):
            CreateCustomerProperty(
                name="no_settings",
                display_name="No Settings",
                property_type=PropertyType.TEXT,
            )

    def test_relation_property_requires_relation_type(self) -> None:
        """A RELATION property without relation_type is rejected before it reaches the API."""
        with pytest.raises(ValueError, match="relation_type is required"):
            CreateCustomerProperty(
                name="no_relation",
                display_name="No Relation",
                property_type=PropertyType.RELATION,
            )

    def test_update_model_keeps_immutable_fields(self) -> None:
        """The update model keeps fields the API refuses to change."""
        fields = set(UpdateCustomerProperty.model_fields)
        assert {"property_type", "is_multi", "settings"} <= fields


class TestCustomerPropertyValues:
    """Test customer property value operations."""

    @pytest.fixture
    def text_property(self, client: PlaneClient, workspace_slug: str):
        """A TEXT property to hold values against."""
        prop = client.customers.properties.create(
            workspace_slug,
            CreateCustomerProperty(
                name="ignored",
                display_name=_unique("Notes"),
                property_type=PropertyType.TEXT,
                settings=TextAttributeSettings(display_format="single-line"),
            ),
        )
        yield prop
        try:
            client.customers.properties.delete(workspace_slug, prop.id)
        except Exception:
            pass

    def test_list_values_empty(self, client: PlaneClient, workspace_slug: str, customer) -> None:
        """A customer with no values set reads back a mapping without them."""
        values = client.customers.property_values.list(workspace_slug, customer.id)
        assert isinstance(values, dict)

    def test_set_and_list_values(
        self, client: PlaneClient, workspace_slug: str, customer, text_property
    ) -> None:
        """Values set in bulk read back."""
        client.customers.property_values.set(
            workspace_slug,
            customer.id,
            SetCustomerPropertyValues(customer_property_values={text_property.id: ["hello"]}),
        )
        values = client.customers.property_values.list(workspace_slug, customer.id)
        assert values.get(text_property.id) == ["hello"]

    def test_update_and_retrieve_single_value(
        self, client: PlaneClient, workspace_slug: str, customer, text_property
    ) -> None:
        """A single property's values can be replaced and read back."""
        client.customers.property_values.update(
            workspace_slug,
            customer.id,
            text_property.id,
            SetCustomerPropertyValue(values=["first"]),
        )
        assert client.customers.property_values.retrieve(
            workspace_slug, customer.id, text_property.id
        ) == ["first"]

        client.customers.property_values.update(
            workspace_slug,
            customer.id,
            text_property.id,
            SetCustomerPropertyValue(values=["second"]),
        )
        assert client.customers.property_values.retrieve(
            workspace_slug, customer.id, text_property.id
        ) == ["second"]

    def test_retrieve_unset_value_is_empty(
        self, client: PlaneClient, workspace_slug: str, customer, text_property
    ) -> None:
        """A property with no value reads back as an empty list, not an error."""
        assert (
            client.customers.property_values.retrieve(workspace_slug, customer.id, text_property.id)
            == []
        )


class TestCustomerRequests:
    """Test customer request operations."""

    @pytest.fixture
    def customer_request(self, client: PlaneClient, workspace_slug: str, customer):
        """A request on the shared customer."""
        req = client.customers.requests.create(
            workspace_slug,
            customer.id,
            CreateCustomerRequest(
                name=_unique("Request"),
                description_html="<p>Please build this</p>",
            ),
        )
        yield req
        try:
            client.customers.requests.delete(workspace_slug, customer.id, req.id)
        except Exception:
            pass

    def test_create_request(self, customer_request) -> None:
        """A request comes back with an id."""
        assert customer_request.id is not None
        assert customer_request.name is not None

    def test_retrieve_request(
        self, client: PlaneClient, workspace_slug: str, customer, customer_request
    ) -> None:
        """A request can be fetched by id."""
        retrieved = client.customers.requests.retrieve(
            workspace_slug, customer.id, customer_request.id
        )
        assert retrieved.id == customer_request.id

    def test_update_request(
        self, client: PlaneClient, workspace_slug: str, customer, customer_request
    ) -> None:
        """A request's name is updatable."""
        new_name = _unique("Updated Request")
        updated = client.customers.requests.update(
            workspace_slug,
            customer.id,
            customer_request.id,
            UpdateCustomerRequest(name=new_name),
        )
        assert updated.name == new_name

    def test_delete_request(self, client: PlaneClient, workspace_slug: str, customer) -> None:
        """A deleted request is gone."""
        req = client.customers.requests.create(
            workspace_slug, customer.id, CreateCustomerRequest(name=_unique("Doomed Request"))
        )
        client.customers.requests.delete(workspace_slug, customer.id, req.id)

        with pytest.raises(HttpError):
            client.customers.requests.retrieve(workspace_slug, customer.id, req.id)

    def test_update_model_keeps_work_item_ids(self) -> None:
        """The update model keeps work_item_ids even though the API discards it.

        Removing it would break callers that already set it. The docstring warns
        that it does nothing and points at customers.work_items instead.
        """
        assert "work_item_ids" in UpdateCustomerRequest.model_fields

    def test_list_returns_a_plain_list(
        self, client: PlaneClient, workspace_slug: str, customer, customer_request
    ) -> None:
        """list() returns a list, as it always claimed to.

        It used to return [] unconditionally by testing a paginated dict with
        isinstance(response, list). Callers keep the list; list_paginated()
        carries the envelope.
        """
        requests = client.customers.requests.list(workspace_slug, customer.id)
        assert isinstance(requests, list)
        assert customer_request.id in [r.id for r in requests]

    def test_list_paginated_returns_envelope(
        self, client: PlaneClient, workspace_slug: str, customer, customer_request
    ) -> None:
        """list_paginated() exposes the cursors and total count."""
        response = client.customers.requests.list_paginated(workspace_slug, customer.id)
        assert isinstance(response.results, list)
        assert isinstance(response.total_count, int)
        assert customer_request.id in [r.id for r in response.results]


class TestCustomerWorkItems:
    """Test linking work items to customers."""

    @pytest.fixture
    def work_item(self, client: PlaneClient, workspace_slug: str, project: Project):
        """A work item to link."""
        item = client.work_items.create(
            workspace_slug, project.id, CreateWorkItem(name=_unique("Linked Work Item"))
        )
        yield item
        try:
            client.work_items.delete(workspace_slug, project.id, item.id)
        except Exception:
            pass

    def test_list_issues_empty(self, client: PlaneClient, workspace_slug: str, customer) -> None:
        """A customer with nothing linked lists no work items."""
        assert client.customers.work_items.list(workspace_slug, customer.id) == []

    def test_link_and_list_issue(
        self, client: PlaneClient, workspace_slug: str, customer, work_item
    ) -> None:
        """A linked work item is listed against the customer."""
        response = client.customers.work_items.link(
            workspace_slug, customer.id, LinkCustomerWorkItems(work_item_ids=[work_item.id])
        )
        assert work_item.id in [i.id for i in response.linked_work_items]

        linked = client.customers.work_items.list(workspace_slug, customer.id)
        assert work_item.id in [i.id for i in linked]

    def test_linked_issue_carries_project_identifier(
        self, client: PlaneClient, workspace_slug: str, customer, work_item
    ) -> None:
        """The project__identifier key is surfaced as project_identifier."""
        client.customers.work_items.link(
            workspace_slug, customer.id, LinkCustomerWorkItems(work_item_ids=[work_item.id])
        )
        linked = client.customers.work_items.list(workspace_slug, customer.id)
        issue = next(i for i in linked if i.id == work_item.id)
        assert issue.project_identifier is not None

    def test_unlink_issue(
        self, client: PlaneClient, workspace_slug: str, customer, work_item
    ) -> None:
        """An unlinked work item drops off the customer."""
        client.customers.work_items.link(
            workspace_slug, customer.id, LinkCustomerWorkItems(work_item_ids=[work_item.id])
        )
        client.customers.work_items.unlink(workspace_slug, customer.id, work_item.id)

        linked = client.customers.work_items.list(workspace_slug, customer.id)
        assert work_item.id not in [i.id for i in linked]

    def test_unlink_unlinked_issue_raises(
        self, client: PlaneClient, workspace_slug: str, customer, work_item
    ) -> None:
        """Unlinking a work item that is not linked is a 404."""
        with pytest.raises(HttpError):
            client.customers.work_items.unlink(workspace_slug, customer.id, work_item.id)

    def test_link_unknown_issue_raises(
        self, client: PlaneClient, workspace_slug: str, customer
    ) -> None:
        """Linking a work item that does not exist is rejected."""
        with pytest.raises(HttpError):
            client.customers.work_items.link(
                workspace_slug,
                customer.id,
                LinkCustomerWorkItems(work_item_ids=[str(uuid.uuid4())]),
            )

    def test_link_via_request_and_filter(
        self, client: PlaneClient, workspace_slug: str, customer, work_item
    ) -> None:
        """Links made through a request are filterable by that request."""
        req = client.customers.requests.create(
            workspace_slug, customer.id, CreateCustomerRequest(name=_unique("Scoped Request"))
        )
        try:
            client.customers.work_items.link(
                workspace_slug,
                customer.id,
                LinkCustomerWorkItems(work_item_ids=[work_item.id]),
                customer_request_id=req.id,
            )
            scoped = client.customers.work_items.list(
                workspace_slug, customer.id, customer_request_id=req.id
            )
            assert work_item.id in [i.id for i in scoped]
        finally:
            try:
                client.customers.requests.delete(workspace_slug, customer.id, req.id)
            except Exception:
                pass

    def test_create_request_with_work_item_ids_links_them(
        self, client: PlaneClient, workspace_slug: str, customer, work_item
    ) -> None:
        """work_item_ids on create links the work items to the customer."""
        req = client.customers.requests.create(
            workspace_slug,
            customer.id,
            CreateCustomerRequest(name=_unique("Linking Request"), work_item_ids=[work_item.id]),
        )
        try:
            linked = client.customers.work_items.list(workspace_slug, customer.id)
            assert work_item.id in [i.id for i in linked]
        finally:
            try:
                client.customers.requests.delete(workspace_slug, customer.id, req.id)
            except Exception:
                pass
