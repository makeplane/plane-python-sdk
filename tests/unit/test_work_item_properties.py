"""Unit tests for WorkItemProperties API resource (smoke tests with real HTTP requests)."""

import pytest

from plane.client import PlaneClient
from plane.models.enums import PropertyType, RelationType
from plane.models.projects import Project
from plane.models.work_item_properties import (
    CreateWorkItemProperty,
    CreateWorkItemPropertyOption,
    UpdateWorkItemProperty,
)
from plane.models.work_item_property_configurations import (
    DateAttributeSettings,
    TextAttributeSettings,
)


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

        # Cleanup
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
