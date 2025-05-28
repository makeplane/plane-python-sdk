import pytest
from unittest.mock import MagicMock
import httpx
from plane.models.workspace import Workspace, WorkspaceUpdate
from plane.exceptions import NotFoundError


class TestWorkspacesResource:
    """Test workspaces resource."""

    @pytest.mark.asyncio
    async def test_list_workspaces(
        self, client, mock_http_client, sample_workspace_data
    ):
        """Test listing workspaces."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {
            "data": [sample_workspace_data],
            "pagination": {
                "page": 1,
                "perPage": 20,
                "total": 1,
                "totalPages": 1,
                "hasNext": False,
                "hasPrev": False,
            },
        }
        mock_http_client.request.return_value = mock_response

        result = await client.workspaces.list()

        assert len(result["workspaces"]) == 1
        assert isinstance(result["workspaces"][0], Workspace)
        assert result["workspaces"][0].name == "Test Workspace"
        assert result["pagination"].total == 1

    @pytest.mark.asyncio
    async def test_get_workspace(self, client, mock_http_client, sample_workspace_data):
        """Test getting a workspace."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = sample_workspace_data
        mock_http_client.request.return_value = mock_response

        workspace = await client.workspaces.get("ws-123")

        assert isinstance(workspace, Workspace)
        assert workspace.id == "ws-123"
        assert workspace.name == "Test Workspace"
        assert workspace.slug == "test-workspace"

    @pytest.mark.asyncio
    async def test_get_workspace_not_found(self, client, mock_http_client):
        """Test getting a non-existent workspace."""
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workspace not found"}
        mock_http_client.request.return_value = mock_response

        with pytest.raises(NotFoundError):
            await client.workspaces.get("ws-999")

    @pytest.mark.asyncio
    async def test_create_workspace(
        self, client, mock_http_client, sample_workspace_data
    ):
        """Test creating a workspace."""
        workspace_create = WorkspaceUpdate(
            name="New Workspace",
            logo="https://logo.url/newlogo.png",
            logo_asset="https://logo.url/newasset.png",
            organization_size="medium",
            timezone="UTC",
        )

        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {
            **sample_workspace_data,
            "name": "New Workspace",
            "logo": "https://logo.url/newlogo.png",
            "logo_asset": "https://logo.url/newasset.png",
            "organization_size": "medium",
        }
        mock_http_client.request.return_value = mock_response

        workspace = await client.workspaces.create(workspace_create)

        assert isinstance(workspace, Workspace)
        assert workspace.name == "New Workspace"
        assert workspace.logo == "https://logo.url/newlogo.png"

    @pytest.mark.asyncio
    async def test_update_workspace(
        self, client, mock_http_client, sample_workspace_data
    ):
        """Test updating a workspace."""
        workspace_update = WorkspaceUpdate(name="Updated Workspace")

        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {
            **sample_workspace_data,
            "name": "Updated Workspace",
        }
        mock_http_client.request.return_value = mock_response

        workspace = await client.workspaces.update("ws-123", workspace_update)

        assert isinstance(workspace, Workspace)
        assert workspace.name == "Updated Workspace"

    @pytest.mark.asyncio
    async def test_delete_workspace(self, client, mock_http_client):
        """Test deleting a workspace."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {}
        mock_http_client.request.return_value = mock_response

        result = await client.workspaces.delete("ws-123")

        assert result is True

    @pytest.mark.asyncio
    async def test_search_workspaces(
        self, client, mock_http_client, sample_workspace_data
    ):
        """Test searching workspaces."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {"workspaces": [sample_workspace_data]}
        mock_http_client.request.return_value = mock_response

        workspaces = await client.workspaces.search("test", limit=5)

        assert len(workspaces) == 1
        assert isinstance(workspaces[0], Workspace)
        assert workspaces[0].name == "Test Workspace"
