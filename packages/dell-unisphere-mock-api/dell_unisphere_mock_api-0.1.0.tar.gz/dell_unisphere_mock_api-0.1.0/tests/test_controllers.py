import pytest
from fastapi import HTTPException
from dell_unisphere_mock_api.controllers.storage_resource_controller import StorageResourceController
from dell_unisphere_mock_api.controllers.filesystem_controller import FilesystemController
from dell_unisphere_mock_api.controllers.nas_server_controller import NasServerController
from dell_unisphere_mock_api.schemas.storage_resource import StorageResourceCreate, StorageResourceUpdate
from dell_unisphere_mock_api.schemas.filesystem import FilesystemCreate, FilesystemUpdate
from dell_unisphere_mock_api.schemas.nas_server import NasServerCreate, NasServerUpdate

class TestStorageResourceController:
    @pytest.fixture
    def controller(self):
        return StorageResourceController()

    @pytest.fixture
    def sample_resource_data(self):
        return StorageResourceCreate(
            name="test_resource",
            description="Test storage resource",
            type="LUN",
            pool="pool_1",
            isThinEnabled=True,
            isCompressionEnabled=False,
            isAdvancedDedupEnabled=False,
            sizeTotal=1024 * 1024 * 1024 * 100  # 100GB
        )

    @pytest.mark.asyncio
    async def test_create_storage_resource(self, controller, sample_resource_data):
        resource = await controller.create_storage_resource(sample_resource_data)
        assert resource["name"] == sample_resource_data.name
        assert resource["type"] == sample_resource_data.type
        assert resource["health"] == "OK"

    @pytest.mark.asyncio
    async def test_get_storage_resource(self, controller, sample_resource_data):
        created = await controller.create_storage_resource(sample_resource_data)
        retrieved = await controller.get_storage_resource(created["id"])
        assert retrieved == created

    @pytest.mark.asyncio
    async def test_list_storage_resources(self, controller, sample_resource_data):
        await controller.create_storage_resource(sample_resource_data)
        resources = await controller.list_storage_resources()
        assert len(resources) == 1
        assert resources[0]["name"] == sample_resource_data.name

    @pytest.mark.asyncio
    async def test_update_storage_resource(self, controller, sample_resource_data):
        created = await controller.create_storage_resource(sample_resource_data)
        update_data = StorageResourceUpdate(
            description="Updated description",
            isCompressionEnabled=True
        )
        updated = await controller.update_storage_resource(created["id"], update_data)
        assert updated["description"] == update_data.description
        assert updated["isCompressionEnabled"] == update_data.isCompressionEnabled

    @pytest.mark.asyncio
    async def test_delete_storage_resource(self, controller, sample_resource_data):
        created = await controller.create_storage_resource(sample_resource_data)
        await controller.delete_storage_resource(created["id"])
        with pytest.raises(HTTPException) as exc_info:
            await controller.get_storage_resource(created["id"])
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_host_access_management(self, controller, sample_resource_data):
        created = await controller.create_storage_resource(sample_resource_data)
        
        # Update host access
        success = await controller.update_host_access(created["id"], "host1", "READ_WRITE")
        assert success
        
        # Verify host access was added
        retrieved = await controller.get_storage_resource(created["id"])
        assert len(retrieved["hostAccess"]) == 1
        assert retrieved["hostAccess"][0]["host"] == "host1"
        assert retrieved["hostAccess"][0]["accessType"] == "READ_WRITE"
        
        # Remove host access
        success = await controller.remove_host_access(created["id"], "host1")
        assert success
        
        # Verify host access was removed
        retrieved = await controller.get_storage_resource(created["id"])
        assert len(retrieved["hostAccess"]) == 0

class TestFilesystemController:
    @pytest.fixture
    def controller(self):
        return FilesystemController()

    @pytest.fixture
    def sample_filesystem_data(self):
        return FilesystemCreate(
            name="test_fs",
            description="Test filesystem",
            nasServer="nas1",
            pool="pool_1",
            size=1024 * 1024 * 1024 * 100,  # 100GB
            isThinEnabled=True,
            supportedProtocols=["NFS", "CIFS"]
        )

    @pytest.mark.asyncio
    async def test_create_filesystem(self, controller, sample_filesystem_data):
        fs = await controller.create_filesystem(sample_filesystem_data)
        assert fs["name"] == sample_filesystem_data.name
        assert fs["size"] == sample_filesystem_data.size
        assert fs["health"] == "OK"

    @pytest.mark.asyncio
    async def test_get_filesystem(self, controller, sample_filesystem_data):
        created = await controller.create_filesystem(sample_filesystem_data)
        retrieved = await controller.get_filesystem(created["id"])
        assert retrieved == created

class TestNasServerController:
    @pytest.fixture
    def controller(self):
        return NasServerController()

    @pytest.fixture
    def sample_nas_data(self):
        return NasServerCreate(
            name="test_nas",
            description="Test NAS server",
            homeSP="spa",
            pool="pool_1",
            currentUnixDirectoryService="NONE",
            isMultiProtocolEnabled=True
        )

    @pytest.mark.asyncio
    async def test_create_nas_server(self, controller, sample_nas_data):
        nas = await controller.create_nas_server(sample_nas_data)
        assert nas["name"] == sample_nas_data.name
        assert nas["health"] == "OK"

    @pytest.mark.asyncio
    async def test_get_nas_server(self, controller, sample_nas_data):
        created = await controller.create_nas_server(sample_nas_data)
        retrieved = await controller.get_nas_server(created["id"])
        assert retrieved == created
