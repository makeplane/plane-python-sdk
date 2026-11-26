"""Unit tests for WorkItemProperties API resource (smoke tests with real HTTP requests)."""

import pytest
from pydantic import ValidationError

from plane.client import PlaneClient
from plane.models.enums import PropertyType, RelationType
from plane.models.projects import Project
from plane.models.work_item_properties import (
    CreateWorkItemProperty,
    CreateWorkItemPropertyOption,
    CreateWorkItemPropertyValue,
    RichTextValue,
    UpdateWorkItemProperty,
    WorkItemProperty,
    WorkItemPropertyValueDetail,
)
from plane.models.work_item_property_configurations import (
    CurrencyNumberAttributeSettings,
    DateAttributeSettings,
    PercentageNumberAttributeSettings,
    StandardNumberAttributeSettings,
    TextAttributeSettings,
)

# One of each number display format, as sent and as Plane returns it
NUMBER_SETTINGS = [
    StandardNumberAttributeSettings(
        display_format="standard", decimal_places=3, thousand_separator=False
    ),
    PercentageNumberAttributeSettings(display_format="percentage", decimal_places=1),
    CurrencyNumberAttributeSettings(
        display_format="currency", currency_code="EUR", decimal_places=2
    ),
]


class TestWorkItemPropertiesAPI:
    """Test WorkItemProperties API resource."""

    @pytest.fixture
    def work_item_type(self, client: PlaneClient, workspace_slug: str, project: Project):
        """Get or create a work item type."""
        import time

        from plane.models.work_item_types import CreateWorkItemType

        # Try to get an existing work item type
        types = client.work_item_types.list(workspace_slug, project.id)
        if types:
            work_item_type = types[0]
            yield work_item_type
            return

        # Create a new work item type
        type_data = CreateWorkItemType(
            name=f"Test Type {int(time.time())}",
            description="Test type",
            is_epic=False,
            is_active=True,
        )
        work_item_type = client.work_item_types.create(workspace_slug, project.id, type_data)
        yield work_item_type
        try:
            client.work_item_types.delete(workspace_slug, project.id, work_item_type.id)
        except Exception:
            pass

    def test_list_work_item_properties(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test listing work item properties."""
        properties = client.work_item_properties.list(workspace_slug, project.id, work_item_type.id)
        assert isinstance(properties, list)

    def test_list_work_item_properties_includes_options(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test that listing work item properties includes options in the response."""
        import time

        # Create a property with inline options
        property_data = CreateWorkItemProperty(
            display_name=f"List Test Property {int(time.time())}",
            description="Property to test list includes options",
            property_type=PropertyType.OPTION,
            is_required=False,
            is_active=True,
            options=[
                CreateWorkItemPropertyOption(name="Option A"),
                CreateWorkItemPropertyOption(name="Option B"),
                CreateWorkItemPropertyOption(name="Option C"),
            ],
        )
        created_prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )

        try:
            # List all properties
            properties = client.work_item_properties.list(
                workspace_slug, project.id, work_item_type.id
            )
            assert isinstance(properties, list)

            # Find the created property in the list
            found_prop = next((p for p in properties if p.id == created_prop.id), None)
            assert found_prop is not None, "Created property should be in the list"

            # Verify options are included in the list response
            assert found_prop.options is not None, "Options should be included in list response"
            assert len(found_prop.options) == 3, "Should have 3 options"
            option_names = [opt.name for opt in found_prop.options]
            assert "Option A" in option_names
            assert "Option B" in option_names
            assert "Option C" in option_names
        finally:
            # Cleanup
            try:
                client.work_item_properties.delete(
                    workspace_slug, project.id, work_item_type.id, created_prop.id
                )
            except Exception:
                pass


class TestWorkItemPropertiesAPICRUD:
    """Test WorkItemProperties API CRUD operations."""

    @pytest.fixture
    def work_item_type(self, client: PlaneClient, workspace_slug: str, project: Project):
        """Get or create a work item type."""
        import time

        from plane.models.work_item_types import CreateWorkItemType

        types = client.work_item_types.list(workspace_slug, project.id)
        if types:
            work_item_type = types[0]
            yield work_item_type
            return

        type_data = CreateWorkItemType(
            name=f"Test Type {int(time.time())}",
            description="Test type",
            is_epic=False,
            is_active=True,
        )
        work_item_type = client.work_item_types.create(workspace_slug, project.id, type_data)
        yield work_item_type
        try:
            client.work_item_types.delete(workspace_slug, project.id, work_item_type.id)
        except Exception:
            pass

    @pytest.fixture
    def property_data(self) -> CreateWorkItemProperty:
        """Create test property data."""
        import time

        return CreateWorkItemProperty(
            display_name=f"Test Property {int(time.time())}",
            description="Test property",
            property_type=PropertyType.TEXT.value,
            is_required=False,
            is_active=True,
            settings=TextAttributeSettings(display_format="multi-line"),
        )

    @pytest.fixture
    def work_item_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project,
        work_item_type,
        property_data: CreateWorkItemProperty,
    ):
        """Create a test property and yield it, then delete it."""
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        yield prop
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    def test_create_work_item_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project,
        work_item_type,
        property_data: CreateWorkItemProperty,
    ) -> None:
        """Test creating a work item property."""
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.id is not None
        assert prop.display_name == property_data.display_name

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    def test_retrieve_work_item_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
        work_item_property,
    ) -> None:
        """Test retrieving a work item property."""
        retrieved = client.work_item_properties.retrieve(
            workspace_slug, project.id, work_item_type.id, work_item_property.id
        )
        assert retrieved is not None
        assert retrieved.id == work_item_property.id
        assert retrieved.display_name == work_item_property.display_name

    def test_retrieve_work_item_property_includes_options(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test that retrieving a work item property includes options in the response."""
        import time

        # Create a property with inline options
        property_data = CreateWorkItemProperty(
            display_name=f"Retrieve Test Property {int(time.time())}",
            description="Property to test retrieve includes options",
            property_type=PropertyType.OPTION,
            is_required=False,
            is_active=True,
            options=[
                CreateWorkItemPropertyOption(name="Choice 1", is_default=True),
                CreateWorkItemPropertyOption(name="Choice 2"),
            ],
        )
        created_prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )

        try:
            # Retrieve the property
            retrieved = client.work_item_properties.retrieve(
                workspace_slug, project.id, work_item_type.id, created_prop.id
            )
            assert retrieved is not None
            assert retrieved.id == created_prop.id

            # Verify options are included in the retrieve response
            assert retrieved.options is not None, "Options should be in retrieve response"
            assert len(retrieved.options) == 2, "Should have 2 options"
            option_names = [opt.name for opt in retrieved.options]
            assert "Choice 1" in option_names
            assert "Choice 2" in option_names
        finally:
            # Cleanup
            try:
                client.work_item_properties.delete(
                    workspace_slug, project.id, work_item_type.id, created_prop.id
                )
            except Exception:
                pass

    def test_update_work_item_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
        work_item_property,
    ) -> None:
        """Test updating a work item property."""
        update_data = UpdateWorkItemProperty(description="Updated description")
        updated = client.work_item_properties.update(
            workspace_slug, project.id, work_item_type.id, work_item_property.id, update_data
        )
        assert updated is not None
        assert updated.id == work_item_property.id
        assert updated.description == "Updated description"


class TestWorkItemPropertyTypes:
    """Test creating work item properties of different types."""

    @pytest.fixture
    def work_item_type(self, client: PlaneClient, workspace_slug: str, project: Project):
        """Create a work item type."""
        import time

        from plane.models.work_item_types import CreateWorkItemType

        type_data = CreateWorkItemType(
            name=f"Test Type {int(time.time())}",
            description="Test type",
            is_epic=False,
            is_active=True,
        )
        work_item_type = client.work_item_types.create(workspace_slug, project.id, type_data)
        yield work_item_type
        try:
            client.work_item_types.delete(workspace_slug, project.id, work_item_type.id)
        except Exception:
            pass

    def test_create_text_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test creating a TEXT property."""
        import time

        property_data = CreateWorkItemProperty(
            display_name=f"Text Property {int(time.time())}",
            description="Test text property",
            property_type=PropertyType.TEXT,
            is_required=False,
            is_active=True,
            settings=TextAttributeSettings(display_format="multi-line"),
        )
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.property_type == PropertyType.TEXT
        assert prop.display_name == property_data.display_name

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    def test_create_datetime_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test creating a DATETIME property."""
        import time

        property_data = CreateWorkItemProperty(
            display_name=f"Date Property {int(time.time())}",
            description="Test datetime property",
            property_type=PropertyType.DATETIME,
            is_required=False,
            is_active=True,
            settings=DateAttributeSettings(display_format="MM/dd/yyyy"),
        )
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.property_type == PropertyType.DATETIME
        assert prop.display_name == property_data.display_name

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    def test_create_decimal_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test creating a DECIMAL property."""
        import time

        property_data = CreateWorkItemProperty(
            display_name=f"Decimal Property {int(time.time())}",
            description="Test decimal property",
            property_type=PropertyType.DECIMAL,
            is_required=False,
            is_active=True,
        )
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.property_type == PropertyType.DECIMAL
        assert prop.display_name == property_data.display_name
        # Without settings, Plane fills in the standard format
        assert prop.settings == StandardNumberAttributeSettings(
            display_format="standard", decimal_places=2, thousand_separator=True
        )

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    @pytest.mark.parametrize("settings", NUMBER_SETTINGS, ids=lambda s: s.display_format)
    def test_create_update_decimal_property_with_display_format(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
        settings,
    ) -> None:
        """Create a DECIMAL property in each display format, then switch it to another."""
        import time

        prop = client.work_item_properties.create(
            workspace_slug,
            project.id,
            work_item_type.id,
            CreateWorkItemProperty(
                display_name=f"Number {settings.display_format} {int(time.time())}",
                property_type=PropertyType.DECIMAL,
                settings=settings,
            ),
        )
        try:
            assert prop.settings == settings

            retrieved = client.work_item_properties.retrieve(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
            assert retrieved.settings == settings

            other = NUMBER_SETTINGS[(NUMBER_SETTINGS.index(settings) + 1) % len(NUMBER_SETTINGS)]
            updated = client.work_item_properties.update(
                workspace_slug,
                project.id,
                work_item_type.id,
                prop.id,
                UpdateWorkItemProperty(property_type=PropertyType.DECIMAL, settings=other),
            )
            assert updated.settings == other
        finally:
            try:
                client.work_item_properties.delete(
                    workspace_slug, project.id, work_item_type.id, prop.id
                )
            except Exception:
                pass

    def test_create_currency_property_without_decimal_places(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Plane fills decimal_places from the currency when it is left out."""
        import time

        prop = client.work_item_properties.create(
            workspace_slug,
            project.id,
            work_item_type.id,
            CreateWorkItemProperty(
                display_name=f"Yen {int(time.time())}",
                property_type=PropertyType.DECIMAL,
                settings=CurrencyNumberAttributeSettings(
                    display_format="currency", currency_code="JPY"
                ),
            ),
        )
        try:
            assert prop.settings == CurrencyNumberAttributeSettings(
                display_format="currency", currency_code="JPY", decimal_places=0
            )
        finally:
            try:
                client.work_item_properties.delete(
                    workspace_slug, project.id, work_item_type.id, prop.id
                )
            except Exception:
                pass

    def test_create_boolean_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test creating a BOOLEAN property."""
        import time

        property_data = CreateWorkItemProperty(
            display_name=f"Boolean Property {int(time.time())}",
            description="Test boolean property",
            property_type=PropertyType.BOOLEAN,
            is_required=False,
            is_active=True,
        )
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.property_type == PropertyType.BOOLEAN
        assert prop.display_name == property_data.display_name

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    def test_create_url_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test creating a URL property."""
        import time

        property_data = CreateWorkItemProperty(
            display_name=f"URL Property {int(time.time())}",
            description="Test URL property",
            property_type=PropertyType.URL,
            is_required=False,
            is_active=True,
        )
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.property_type == PropertyType.URL
        assert prop.display_name == property_data.display_name

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    def test_create_email_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test creating an EMAIL property."""
        import time

        property_data = CreateWorkItemProperty(
            display_name=f"Email Property {int(time.time())}",
            description="Test email property",
            property_type=PropertyType.EMAIL,
            is_required=False,
            is_active=True,
        )
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.property_type == PropertyType.EMAIL
        assert prop.display_name == property_data.display_name

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    def test_create_relation_user_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test creating a RELATION property with USER relation type."""
        import time

        property_data = CreateWorkItemProperty(
            display_name=f"Relation User Property {int(time.time())}",
            description="Test relation property for users",
            property_type=PropertyType.RELATION,
            relation_type=RelationType.USER,
            is_required=False,
            is_active=True,
        )
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.property_type == PropertyType.RELATION
        assert prop.relation_type == RelationType.USER
        assert prop.display_name == property_data.display_name

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    def test_create_option_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test creating an OPTION property."""
        import time

        property_data = CreateWorkItemProperty(
            display_name=f"Option Property {int(time.time())}",
            description="Test option property",
            property_type=PropertyType.OPTION,
            is_required=False,
            is_active=True,
        )
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.property_type == PropertyType.OPTION
        assert prop.display_name == property_data.display_name

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    def test_create_option_property_with_inline_options(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test creating an OPTION property with inline options."""
        import time

        property_data = CreateWorkItemProperty(
            display_name=f"Priority Property {int(time.time())}",
            description="Test option property with inline options",
            property_type=PropertyType.OPTION,
            is_required=False,
            is_active=True,
            options=[
                CreateWorkItemPropertyOption(name="Low", is_default=False),
                CreateWorkItemPropertyOption(name="Medium", is_default=True),
                CreateWorkItemPropertyOption(name="High", is_default=False),
                CreateWorkItemPropertyOption(name="Critical", is_default=False),
            ],
        )
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.property_type == PropertyType.OPTION
        assert prop.display_name == property_data.display_name
        # Verify options were created
        assert prop.options is not None
        assert len(prop.options) == 4
        option_names = [opt.name for opt in prop.options]
        assert "Low" in option_names
        assert "Medium" in option_names
        assert "High" in option_names
        assert "Critical" in option_names

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass

    def test_create_file_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_type,
    ) -> None:
        """Test creating a FILE property."""
        import time

        property_data = CreateWorkItemProperty(
            display_name=f"File Property {int(time.time())}",
            description="Test file property",
            property_type=PropertyType.FILE,
            is_required=False,
            is_active=True,
        )
        prop = client.work_item_properties.create(
            workspace_slug, project.id, work_item_type.id, property_data
        )
        assert prop is not None
        assert prop.property_type == PropertyType.FILE
        assert prop.display_name == property_data.display_name

        # Cleanup
        try:
            client.work_item_properties.delete(
                workspace_slug, project.id, work_item_type.id, prop.id
            )
        except Exception:
            pass


class TestProjectLevelWorkItemPropertiesAPI:
    """Test project-level (type-agnostic) work item property endpoints."""

    def test_list_project_work_item_properties(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
    ) -> None:
        """Test listing all work item properties for a project regardless of type."""
        properties = client.work_item_properties.list_project(workspace_slug, project.id)
        assert isinstance(properties, list)

    def test_create_retrieve_update_delete_project_property(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
    ) -> None:
        """Test full CRUD for a project-level work item property."""
        import time

        from plane.errors.errors import HttpError
        from plane.models.work_item_property_configurations import TextAttributeSettings

        display_name = f"Project Prop {int(time.time())}"
        data = CreateWorkItemProperty(
            display_name=display_name,
            description="Project-level property",
            property_type=PropertyType.TEXT,
            is_required=False,
            is_active=True,
            settings=TextAttributeSettings(display_format="multi-line"),
        )
        try:
            created = client.work_item_properties.create_project(workspace_slug, project.id, data)
        except HttpError as e:
            if e.status_code == 400:
                pytest.skip(
                    "Workspace has IS_WORK_ITEM_TYPES_ENABLED — project-level property creation blocked"
                )
            raise
        assert created is not None
        assert created.id is not None
        assert created.display_name == display_name

        try:
            retrieved = client.work_item_properties.retrieve_project(
                workspace_slug, project.id, created.id
            )
            assert retrieved.id == created.id
            assert retrieved.display_name == display_name

            updated = client.work_item_properties.update_project(
                workspace_slug,
                project.id,
                created.id,
                UpdateWorkItemProperty(description="Updated project property"),
            )
            assert updated.id == created.id
            assert updated.description == "Updated project property"
        finally:
            try:
                client.work_item_properties.delete_project(workspace_slug, project.id, created.id)
            except Exception:
                pass

    def test_attach_detach_property_to_type(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
    ) -> None:
        """Test attaching and detaching a project-level property to/from a work item type."""
        import time

        from plane.models.work_item_property_configurations import TextAttributeSettings
        from plane.models.work_item_types import CreateWorkItemType

        from plane.errors.errors import HttpError

        type_data = CreateWorkItemType(
            name=f"Attach Test Type {int(time.time())}",
            is_active=True,
        )
        try:
            wit = client.work_item_types.create(workspace_slug, project.id, type_data)
        except HttpError as e:
            if e.status_code == 400:
                pytest.skip(
                    "Workspace has IS_WORK_ITEM_TYPES_ENABLED — project-level type creation blocked"
                )
            raise

        prop_data = CreateWorkItemProperty(
            display_name=f"Attach Test Prop {int(time.time())}",
            property_type=PropertyType.TEXT,
            is_active=True,
            settings=TextAttributeSettings(display_format="multi-line"),
        )
        try:
            prop = client.work_item_properties.create_project(workspace_slug, project.id, prop_data)
        except HttpError as e:
            if e.status_code == 400:
                client.work_item_types.delete(workspace_slug, project.id, wit.id)
                pytest.skip(
                    "Workspace has IS_WORK_ITEM_TYPES_ENABLED — project-level property creation blocked"
                )
            raise

        try:
            result = client.work_item_properties.attach_to_type(
                workspace_slug, project.id, wit.id, [prop.id]
            )
            assert isinstance(result, list)

            client.work_item_properties.detach_from_type(
                workspace_slug, project.id, wit.id, prop.id
            )
        finally:
            try:
                client.work_item_properties.delete_project(workspace_slug, project.id, prop.id)
            except Exception:
                pass
            try:
                client.work_item_types.delete(workspace_slug, project.id, wit.id)
            except Exception:
                pass


class TestWorkItemPropertyTypesOffline:
    """What the models accept and send. Offline, so it runs without a Plane instance."""

    def test_a_cascading_property_parses(self) -> None:
        """Plane returns CASCADING properties; the enum lacked the value, so listing a
        workspace that had one raised ValidationError."""
        prop = WorkItemProperty.model_validate(
            {"id": "p", "property_type": "CASCADING", "display_name": "Region"}
        )

        assert prop.property_type == PropertyType.CASCADING

    def test_rich_text_is_a_relation_type_not_a_property_type(self) -> None:
        assert "RICH_TEXT" in {member.value for member in RelationType}
        assert "RICH_TEXT" not in {member.value for member in PropertyType}


class TestRichTextValueOffline:
    """A rich text value is an object with description_html -- Plane answers a bare
    string with 400 "Rich text value must be an object"."""

    @pytest.fixture
    def sent(self, monkeypatch: pytest.MonkeyPatch):
        client = PlaneClient(api_key="k", base_url="http://plane.invalid")
        payloads: list[dict] = []

        def post(endpoint: str, data: dict | None = None, params: dict | None = None) -> dict:
            payloads.append(data or {})
            return {"id": "v", "property_id": "p", "issue_id": "w", "value": "desc-1"}

        monkeypatch.setattr(client.work_item_properties.values, "_post", post)

        def send(value) -> dict:
            client.work_item_properties.values.create(
                "ws", "p", "w", "prop", CreateWorkItemPropertyValue(value=value)
            )
            return payloads[-1]

        return send

    def test_a_rich_text_value_is_sent_as_an_object(self, sent) -> None:
        assert sent(RichTextValue(description_html="<p>Notes</p>")) == {
            "value": {"description_html": "<p>Notes</p>"}
        }

    def test_the_other_value_types_are_unchanged(self, sent) -> None:
        assert sent("plain") == {"value": "plain"}
        assert sent(True) == {"value": True}
        assert sent(["a", "b"]) == {"value": ["a", "b"]}

    def test_a_rich_text_read_carries_its_html_in_value_detail(self) -> None:
        """`value` is the stored content's ID; the HTML is beside it."""
        detail = WorkItemPropertyValueDetail.model_validate(
            {
                "id": "v",
                "property_id": "p",
                "issue_id": "w",
                "value": "desc-1",
                "value_detail": {
                    "id": "desc-1",
                    "description_html": "<p>Notes</p>",
                    "description_stripped": "Notes",
                },
            }
        )

        assert detail.value == "desc-1"
        assert detail.value_detail.description_html == "<p>Notes</p>"


class TestNumberDisplayFormatsOffline:
    """Number (DECIMAL) display formats live in `settings`, picked by `display_format`."""

    @pytest.mark.parametrize("settings", NUMBER_SETTINGS, ids=lambda s: s.display_format)
    def test_each_format_is_accepted_on_create_and_update(self, settings) -> None:
        as_dict = settings.model_dump(exclude_none=True)
        create = CreateWorkItemProperty(
            display_name="Budget", property_type=PropertyType.DECIMAL, settings=as_dict
        )
        update = UpdateWorkItemProperty(property_type=PropertyType.DECIMAL, settings=as_dict)

        assert create.settings == settings
        assert update.settings == settings
        assert create.model_dump(exclude_none=True)["settings"] == as_dict
        assert update.model_dump(exclude_none=True)["settings"] == as_dict

    def test_the_reported_currency_example_validates(self) -> None:
        prop = CreateWorkItemProperty(
            display_name="Budget",
            property_type="DECIMAL",
            settings={"display_format": "currency", "currency_code": "USD", "decimal_places": 2},
        )

        assert isinstance(prop.settings, CurrencyNumberAttributeSettings)

    def test_decimal_settings_are_optional(self) -> None:
        """Plane fills in the standard format, so nothing is sent."""
        create = CreateWorkItemProperty(display_name="Budget", property_type=PropertyType.DECIMAL)
        update = UpdateWorkItemProperty(property_type=PropertyType.DECIMAL)

        assert "settings" not in create.model_dump(exclude_none=True)
        assert "settings" not in update.model_dump(exclude_none=True)

    def test_currency_without_decimal_places_leaves_them_to_the_server(self) -> None:
        prop = CreateWorkItemProperty(
            display_name="Budget",
            property_type=PropertyType.DECIMAL,
            settings={"display_format": "currency", "currency_code": "JPY"},
        )

        assert prop.model_dump(exclude_none=True)["settings"] == {
            "display_format": "currency",
            "currency_code": "JPY",
        }

    @pytest.mark.parametrize("decimal_places", [-1, 5])
    @pytest.mark.parametrize(
        "settings",
        [
            {"display_format": "standard", "thousand_separator": True},
            {"display_format": "percentage"},
            {"display_format": "currency", "currency_code": "USD"},
        ],
        ids=lambda s: s["display_format"],
    )
    def test_decimal_places_out_of_range_is_rejected(self, settings, decimal_places) -> None:
        with pytest.raises(ValidationError, match="decimal_places"):
            CreateWorkItemProperty(
                display_name="Budget",
                property_type=PropertyType.DECIMAL,
                settings={**settings, "decimal_places": decimal_places},
            )

    @pytest.mark.parametrize("currency_code", ["usd", "US", "USDT", "U$D"])
    def test_a_malformed_currency_code_is_rejected(self, currency_code) -> None:
        with pytest.raises(ValidationError, match="currency_code"):
            CurrencyNumberAttributeSettings(display_format="currency", currency_code=currency_code)

    def test_standard_requires_thousand_separator(self) -> None:
        with pytest.raises(ValidationError, match="thousand_separator"):
            StandardNumberAttributeSettings(display_format="standard", decimal_places=2)

    @pytest.mark.parametrize(
        ("property_type", "settings", "message"),
        [
            (PropertyType.TEXT, NUMBER_SETTINGS[0], "TextAttributeSettings"),
            (PropertyType.DATETIME, NUMBER_SETTINGS[2], "DateAttributeSettings"),
            (
                PropertyType.DECIMAL,
                TextAttributeSettings(display_format="single-line"),
                "for DECIMAL properties",
            ),
            (
                PropertyType.DECIMAL,
                DateAttributeSettings(display_format="MM/dd/yyyy"),
                "for DECIMAL properties",
            ),
        ],
        ids=["number-on-text", "number-on-datetime", "text-on-decimal", "date-on-decimal"],
    )
    def test_settings_of_another_property_type_are_rejected(
        self, property_type, settings, message
    ) -> None:
        with pytest.raises(ValidationError, match=message):
            CreateWorkItemProperty(
                display_name="Budget", property_type=property_type, settings=settings
            )
        with pytest.raises(ValidationError, match=message):
            UpdateWorkItemProperty(property_type=property_type, settings=settings)

    def test_a_retrieved_decimal_property_parses_its_settings(self) -> None:
        prop = WorkItemProperty.model_validate(
            {
                "id": "p",
                "display_name": "Budget",
                "property_type": "DECIMAL",
                "settings": {
                    "display_format": "currency",
                    "currency_code": "USD",
                    "decimal_places": 2,
                },
            }
        )

        assert prop.settings == CurrencyNumberAttributeSettings(
            display_format="currency", currency_code="USD", decimal_places=2
        )

    def test_unknown_settings_still_read_as_a_dict(self) -> None:
        """A display format this SDK doesn't know yet must not break listing."""
        prop = WorkItemProperty.model_validate(
            {
                "id": "p",
                "display_name": "Budget",
                "property_type": "DECIMAL",
                "settings": {"display_format": "scientific", "significant_figures": 3},
            }
        )

        assert prop.settings == {"display_format": "scientific", "significant_figures": 3}

    @pytest.mark.parametrize("settings", NUMBER_SETTINGS, ids=lambda s: s.display_format)
    def test_an_unknown_key_is_rejected_on_create_and_update(self, settings) -> None:
        """Plane rejects keys a format doesn't have, so a typo must not be dropped silently."""
        with_typo = {**settings.model_dump(exclude_none=True), "decimal_place": 2}

        with pytest.raises(ValidationError, match="decimal_place"):
            CreateWorkItemProperty(
                display_name="Budget", property_type=PropertyType.DECIMAL, settings=with_typo
            )
        with pytest.raises(ValidationError, match="decimal_place"):
            UpdateWorkItemProperty(property_type=PropertyType.DECIMAL, settings=with_typo)
        with pytest.raises(ValidationError, match="decimal_place"):
            type(settings).model_validate(with_typo)

    def test_a_number_format_with_an_unknown_key_still_reads(self) -> None:
        """A key the server adds later must not break listing: the settings read as a dict."""
        settings = {
            "display_format": "currency",
            "currency_code": "USD",
            "decimal_places": 2,
            "symbol_position": "before",
        }
        prop = WorkItemProperty.model_validate(
            {"id": "p", "display_name": "Budget", "property_type": "DECIMAL", "settings": settings}
        )

        assert prop.settings == settings

    def test_empty_decimal_settings_are_sent_as_empty(self) -> None:
        """Plane reads `settings={}` on a DECIMAL property as the default format, and on
        update resets the property to it, so the {} must reach the request body."""
        create = CreateWorkItemProperty(
            display_name="Budget", property_type=PropertyType.DECIMAL, settings={}
        )
        update = UpdateWorkItemProperty(property_type=PropertyType.DECIMAL, settings={})
        update_settings_only = UpdateWorkItemProperty(settings={})

        assert create.model_dump(exclude_none=True)["settings"] == {}
        assert update.model_dump(exclude_none=True)["settings"] == {}
        assert update_settings_only.model_dump(exclude_none=True) == {"settings": {}}

    def test_empty_decimal_settings_reach_the_request_body(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        client = PlaneClient(api_key="k", base_url="http://plane.invalid")
        sent: list[dict] = []
        # What Plane stores for {}: the default format
        response = {
            "id": "p",
            "display_name": "Budget",
            "property_type": "DECIMAL",
            "settings": {
                "display_format": "standard",
                "decimal_places": 2,
                "thousand_separator": True,
            },
        }

        def send(endpoint: str, data: dict | None = None, params: dict | None = None) -> dict:
            sent.append(data or {})
            return response

        for resource in (client.work_item_properties, client.workspace_work_item_properties):
            monkeypatch.setattr(resource, "_post", send)
            monkeypatch.setattr(resource, "_patch", send)

        create = CreateWorkItemProperty(
            display_name="Budget", property_type=PropertyType.DECIMAL, settings={}
        )
        update = UpdateWorkItemProperty(settings={})
        client.work_item_properties.create("ws", "proj", "type", create)
        client.work_item_properties.update("ws", "proj", "type", "p", update)
        client.workspace_work_item_properties.create("ws", create)
        prop = client.workspace_work_item_properties.update("ws", "p", update)

        assert [body["settings"] for body in sent] == [{}, {}, {}, {}]
        assert isinstance(prop.settings, StandardNumberAttributeSettings)

    def test_empty_settings_are_still_rejected_on_text_and_datetime(self) -> None:
        for property_type in (PropertyType.TEXT, PropertyType.DATETIME):
            with pytest.raises(ValidationError, match="must be"):
                CreateWorkItemProperty(
                    display_name="Notes", property_type=property_type, settings={}
                )

    def test_stored_empty_settings_still_read(self) -> None:
        """A DECIMAL property created before display formats holds {}."""
        prop = WorkItemProperty.model_validate(
            {"id": "p", "display_name": "Budget", "property_type": "DECIMAL", "settings": {}}
        )

        assert prop.settings == {}
