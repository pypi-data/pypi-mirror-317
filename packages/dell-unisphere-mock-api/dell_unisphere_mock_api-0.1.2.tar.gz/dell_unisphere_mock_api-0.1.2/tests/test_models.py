from datetime import datetime

import pytest

from dell_unisphere_mock_api.models.filesystem import FilesystemModel
from dell_unisphere_mock_api.models.nas_server import NasServerModel
from dell_unisphere_mock_api.models.storage_resource import StorageResourceModel


class TestStorageResourceModel:
    @pytest.fixture
    def model(self):
        return StorageResourceModel()

    @pytest.fixture
    def sample_resource_data(self):
        return {
            "name": "test_resource",
            "description": "Test storage resource",
            "type": "LUN",
            "pool": "pool_1",
            "isThinEnabled": True,
            "isCompressionEnabled": False,
            "isAdvancedDedupEnabled": False,
            "sizeTotal": 1024 * 1024 * 1024 * 100,  # 100GB
        }

    def test_create_storage_resource(self, model, sample_resource_data):
        resource = model.create_storage_resource(sample_resource_data)
        assert resource["name"] == sample_resource_data["name"]
        assert resource["type"] == sample_resource_data["type"]
        assert resource["health"] == "OK"
        assert resource["sizeTotal"] == sample_resource_data["sizeTotal"]
        assert resource["sizeUsed"] == 0
        assert resource["sizeAllocated"] < resource["sizeTotal"]
        assert "id" in resource

    def test_get_storage_resource(self, model, sample_resource_data):
        resource = model.create_storage_resource(sample_resource_data)
        retrieved = model.get_storage_resource(resource["id"])
        assert retrieved == resource

    def test_list_storage_resources(self, model, sample_resource_data):
        # Create multiple resources
        resource1 = model.create_storage_resource(sample_resource_data)
        resource2 = model.create_storage_resource(
            {**sample_resource_data, "name": "test_resource_2", "type": "FILESYSTEM"}
        )

        # Test listing all resources
        resources = model.list_storage_resources()
        assert len(resources) == 2

        # Test filtering by type
        lun_resources = model.list_storage_resources("LUN")
        assert len(lun_resources) == 1
        assert lun_resources[0]["id"] == resource1["id"]

    def test_update_storage_resource(self, model, sample_resource_data):
        resource = model.create_storage_resource(sample_resource_data)
        update_data = {
            "description": "Updated description",
            "isCompressionEnabled": True,
        }
        updated = model.update_storage_resource(resource["id"], update_data)
        assert updated["description"] == update_data["description"]
        assert updated["isCompressionEnabled"] == update_data["isCompressionEnabled"]

    def test_delete_storage_resource(self, model, sample_resource_data):
        resource = model.create_storage_resource(sample_resource_data)
        assert model.delete_storage_resource(resource["id"]) is True
        assert model.get_storage_resource(resource["id"]) is None

    def test_host_access_management(self, model, sample_resource_data):
        resource = model.create_storage_resource(sample_resource_data)

        # Add host access
        assert model.update_host_access(resource["id"], "host1", "READ_WRITE") is True
        updated = model.get_storage_resource(resource["id"])
        assert len(updated["hostAccess"]) == 1
        assert updated["hostAccess"][0]["host"] == "host1"

        # Remove host access
        assert model.remove_host_access(resource["id"], "host1") is True
        updated = model.get_storage_resource(resource["id"])
        assert len(updated["hostAccess"]) == 0

    def test_update_usage_stats(self, model, sample_resource_data):
        resource = model.create_storage_resource(sample_resource_data)
        size_used = 1024 * 1024 * 1024 * 50  # 50GB
        tier_usage = {"tier_1": size_used}

        assert model.update_usage_stats(resource["id"], size_used, tier_usage) is True
        updated = model.get_storage_resource(resource["id"])
        assert updated["sizeUsed"] == size_used
        assert updated["perTierSizeUsed"] == tier_usage


class TestFilesystemModel:
    @pytest.fixture
    def model(self):
        return FilesystemModel()

    @pytest.fixture
    def sample_filesystem_data(self):
        return {
            "name": "test_fs",
            "description": "Test filesystem",
            "nasServer": "nas1",
            "pool": "pool_1",
            "size": 1024 * 1024 * 1024 * 100,  # 100GB
            "isThinEnabled": True,
            "supportedProtocols": ["NFS", "CIFS"],
        }

    def test_create_filesystem(self, model, sample_filesystem_data):
        fs = model.create_filesystem(sample_filesystem_data)
        assert fs["name"] == sample_filesystem_data["name"]
        assert fs["size"] == sample_filesystem_data["size"]
        assert fs["health"] == "OK"
        assert "id" in fs

    def test_get_filesystem(self, model, sample_filesystem_data):
        fs = model.create_filesystem(sample_filesystem_data)
        retrieved = model.get_filesystem(fs["id"])
        assert retrieved == fs

    def test_list_filesystems(self, model, sample_filesystem_data):
        fs1 = model.create_filesystem(sample_filesystem_data)
        fs2 = model.create_filesystem({**sample_filesystem_data, "name": "test_fs_2"})

        filesystems = model.list_filesystems()
        assert len(filesystems) == 2


class TestNasServerModel:
    @pytest.fixture
    def model(self):
        return NasServerModel()

    @pytest.fixture
    def sample_nas_data(self):
        return {
            "name": "test_nas",
            "description": "Test NAS server",
            "homeSP": "spa",
            "pool": "pool_1",
            "currentUnixDirectoryService": "NONE",
            "isMultiProtocolEnabled": True,
        }

    def test_create_nas_server(self, model, sample_nas_data):
        nas = model.create_nas_server(sample_nas_data)
        assert nas["name"] == sample_nas_data["name"]
        assert nas["health"] == "OK"
        assert "id" in nas

    def test_get_nas_server(self, model, sample_nas_data):
        nas = model.create_nas_server(sample_nas_data)
        retrieved = model.get_nas_server(nas["id"])
        assert retrieved == nas

    def test_list_nas_servers(self, model, sample_nas_data):
        nas1 = model.create_nas_server(sample_nas_data)
        nas2 = model.create_nas_server({**sample_nas_data, "name": "test_nas_2"})

        servers = model.list_nas_servers()
        assert len(servers) == 2
