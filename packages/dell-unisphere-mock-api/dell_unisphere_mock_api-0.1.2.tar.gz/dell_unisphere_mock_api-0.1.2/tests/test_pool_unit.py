import pytest
from fastapi.testclient import TestClient

from dell_unisphere_mock_api.main import app
from dell_unisphere_mock_api.schemas.pool_unit import PoolUnitOpStatusEnum, PoolUnitTypeEnum

client = TestClient(app)


def get_auth_headers():
    """Helper function to get authentication headers."""
    # admin:Password123! in base64
    return {
        "Authorization": "Basic YWRtaW46UGFzc3dvcmQxMjMh",
        "X-EMC-REST-CLIENT": "true",
        "EMC-CSRF-TOKEN": "test-csrf-token",
    }


def test_create_pool_unit():
    """Test creating a new pool unit."""
    pool_unit_data = {
        "name": "test_pool_unit",
        "description": "Test pool unit",
        "type": PoolUnitTypeEnum.VIRTUAL_DISK,
        "size_total": 1000000,
        "size_used": 0,
        "size_free": 1000000,
        "raid_type": "RAID5",
        "disk_group": "1",
    }

    response = client.post("/api/types/poolUnit/instances", json=pool_unit_data, headers=get_auth_headers())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == pool_unit_data["name"]
    assert "id" in data


def test_get_pool_unit():
    """Test getting a specific pool unit."""
    # First create a pool unit
    pool_unit_data = {
        "name": "test_pool_unit",
        "type": PoolUnitTypeEnum.VIRTUAL_DISK,
        "size_total": 1000000,
        "size_used": 0,
        "size_free": 1000000,
    }
    create_response = client.post("/api/types/poolUnit/instances", json=pool_unit_data, headers=get_auth_headers())
    pool_unit_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/types/poolUnit/instances/{pool_unit_id}", headers=get_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pool_unit_id
    assert data["name"] == pool_unit_data["name"]


def test_list_pool_units():
    """Test listing all pool units."""
    response = client.get("/api/types/poolUnit/instances", headers=get_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_pool_unit():
    """Test updating a pool unit."""
    # First create a pool unit
    pool_unit_data = {
        "name": "test_pool_unit",
        "type": PoolUnitTypeEnum.VIRTUAL_DISK,
        "size_total": 1000000,
        "size_used": 0,
        "size_free": 1000000,
    }
    create_response = client.post("/api/types/poolUnit/instances", json=pool_unit_data, headers=get_auth_headers())
    pool_unit_id = create_response.json()["id"]

    # Then update it
    update_data = {"name": "updated_pool_unit", "description": "Updated description"}
    response = client.patch(
        f"/api/types/poolUnit/instances/{pool_unit_id}",
        json=update_data,
        headers=get_auth_headers(),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]


def test_delete_pool_unit():
    """Test deleting a pool unit."""
    # First create a pool unit
    pool_unit_data = {
        "name": "test_pool_unit",
        "type": PoolUnitTypeEnum.VIRTUAL_DISK,
        "size_total": 1000000,
        "size_used": 0,
        "size_free": 1000000,
    }
    create_response = client.post("/api/types/poolUnit/instances", json=pool_unit_data, headers=get_auth_headers())
    pool_unit_id = create_response.json()["id"]

    # Then delete it
    response = client.delete(f"/api/types/poolUnit/instances/{pool_unit_id}", headers=get_auth_headers())
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/api/types/poolUnit/instances/{pool_unit_id}", headers=get_auth_headers())
    assert get_response.status_code == 404
