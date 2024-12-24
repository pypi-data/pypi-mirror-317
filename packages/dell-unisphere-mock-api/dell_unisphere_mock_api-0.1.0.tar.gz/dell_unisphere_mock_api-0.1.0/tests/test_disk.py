from fastapi.testclient import TestClient
import pytest
from dell_unisphere_mock_api.main import app
from dell_unisphere_mock_api.schemas.disk import DiskTypeEnum, DiskTierEnum

@pytest.fixture(autouse=True)
def client(test_client):
    return test_client

def get_auth_headers():
    """Helper function to get authentication headers."""
    return {"Authorization": "Basic YWRtaW46c2VjcmV0"}  # admin:secret

def test_create_disk(client, auth_headers):
    """Test creating a new disk."""
    disk_data = {
        "name": "test_disk",
        "description": "Test disk",
        "disk_type": DiskTypeEnum.SAS,
        "tier_type": DiskTierEnum.PERFORMANCE,
        "size": 1000000,
        "slot_number": 1,
        "firmware_version": "1.0.0"
    }
    
    response = client.post(
        "/api/types/disk/instances",
        json=disk_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == disk_data["name"]
    assert "id" in data

def test_create_disk_invalid_type(client, auth_headers):
    """Test creating a disk with invalid disk type."""
    disk_data = {
        "name": "test_disk",
        "disk_type": "INVALID_TYPE",
        "tier_type": DiskTierEnum.PERFORMANCE,
        "size": 1000000,
        "slot_number": 1
    }
    
    response = client.post(
        "/api/types/disk/instances",
        json=disk_data,
        headers=auth_headers
    )
    assert response.status_code == 422  # Validation error

def test_get_disk(client, auth_headers):
    """Test getting a specific disk."""
    # First create a disk
    disk_data = {
        "name": "test_disk",
        "disk_type": DiskTypeEnum.SAS,
        "tier_type": DiskTierEnum.PERFORMANCE,
        "size": 1000000,
        "slot_number": 1
    }
    create_response = client.post(
        "/api/types/disk/instances",
        json=disk_data,
        headers=auth_headers
    )
    disk_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(
        f"/api/types/disk/instances/{disk_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == disk_id
    assert data["name"] == disk_data["name"]

def test_list_disks(client, auth_headers):
    """Test listing all disks."""
    response = client.get(
        "/api/types/disk/instances",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_disk(client, auth_headers):
    """Test updating a disk."""
    # First create a disk
    disk_data = {
        "name": "test_disk",
        "disk_type": DiskTypeEnum.SAS,
        "tier_type": DiskTierEnum.PERFORMANCE,
        "size": 1000000,
        "slot_number": 1
    }
    create_response = client.post(
        "/api/types/disk/instances",
        json=disk_data,
        headers=auth_headers
    )
    disk_id = create_response.json()["id"]
    
    # Then update it
    update_data = {
        "name": "updated_disk",
        "description": "Updated description",
        "firmware_version": "2.0.0"
    }
    response = client.patch(
        f"/api/types/disk/instances/{disk_id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["firmware_version"] == update_data["firmware_version"]

def test_delete_disk(client, auth_headers):
    """Test deleting a disk."""
    # First create a disk
    disk_data = {
        "name": "test_disk",
        "disk_type": DiskTypeEnum.SAS,
        "tier_type": DiskTierEnum.PERFORMANCE,
        "size": 1000000,
        "slot_number": 1
    }
    create_response = client.post(
        "/api/types/disk/instances",
        json=disk_data,
        headers=auth_headers
    )
    disk_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(
        f"/api/types/disk/instances/{disk_id}",
        headers=auth_headers
    )
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(
        f"/api/types/disk/instances/{disk_id}",
        headers=auth_headers
    )
    assert get_response.status_code == 404

def test_get_disks_by_pool(client, auth_headers):
    """Test getting disks by pool ID."""
    # First create a disk with a pool ID
    disk_data = {
        "name": "test_disk",
        "disk_type": DiskTypeEnum.SAS,
        "tier_type": DiskTierEnum.PERFORMANCE,
        "size": 1000000,
        "slot_number": 1,
        "pool_id": "test_pool"
    }
    client.post(
        "/api/types/disk/instances",
        json=disk_data,
        headers=auth_headers
    )
    
    # Get disks by pool
    response = client.get(
        "/api/types/disk/instances/byPool/test_pool",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(disk["pool_id"] == "test_pool" for disk in data)

def test_get_disks_by_disk_group(client, auth_headers):
    """Test getting disks by disk group ID."""
    # First create a disk with a disk group ID
    disk_data = {
        "name": "test_disk",
        "disk_type": DiskTypeEnum.SAS,
        "tier_type": DiskTierEnum.PERFORMANCE,
        "size": 1000000,
        "slot_number": 1,
        "disk_group_id": "test_group"
    }
    client.post(
        "/api/types/disk/instances",
        json=disk_data,
        headers=auth_headers
    )
    
    # Get disks by disk group
    response = client.get(
        "/api/types/disk/instances/byDiskGroup/test_group",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(disk["disk_group_id"] == "test_group" for disk in data)
