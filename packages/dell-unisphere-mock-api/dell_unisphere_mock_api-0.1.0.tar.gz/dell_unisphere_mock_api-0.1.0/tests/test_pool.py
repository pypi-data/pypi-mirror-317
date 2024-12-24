import pytest
from fastapi.testclient import TestClient
from dell_unisphere_mock_api.main import app


@pytest.fixture
def sample_pool_data():
    return {
        "name": "test_pool",
        "description": "Test pool for unit tests",
        "raidType": "RAID5",
        "sizeFree": 1000000000,
        "sizeTotal": 2000000000,
        "sizeUsed": 1000000000,
        "sizeSubscribed": 1500000000,
        "poolType": "Performance",
        "alertThreshold": 80,
        "poolFastVP": True,
        "isFASTCacheEnabled": False,
        "isFASTVpScheduleEnabled": True,
        "isHarvestEnabled": True
    }


def test_create_pool(test_client, sample_pool_data, auth_headers):
    response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_pool_data["name"]
    assert data["description"] == sample_pool_data["description"]
    assert "id" in data


def test_get_pool(test_client, sample_pool_data, auth_headers):
    # First create a pool
    create_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert create_response.status_code == 201
    pool_id = create_response.json()["id"]

    # Then get it by ID
    response = test_client.get(f"/api/instances/pool/{pool_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pool_id
    assert data["name"] == sample_pool_data["name"]


def test_get_pool_by_name(test_client, sample_pool_data, auth_headers):
    # First create a pool
    create_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert create_response.status_code == 201

    # Then get it by name
    response = test_client.get(f"/api/instances/pool/name:{sample_pool_data['name']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_pool_data["name"]


def test_list_pools(test_client, sample_pool_data, auth_headers):
    # First create a pool
    create_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert create_response.status_code == 201

    # Then list all pools
    response = test_client.get("/api/types/pool/instances", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "@base" in data
    assert "entries" in data
    assert len(data["entries"]) > 0
    assert any(pool["content"]["name"] == sample_pool_data["name"] for pool in data["entries"])


def test_modify_pool(test_client, sample_pool_data, auth_headers):
    # First create a pool
    create_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert create_response.status_code == 201
    pool_id = create_response.json()["id"]

    # Modify the pool
    update_data = {
        "description": "Modified test pool",
        "alertThreshold": 75
    }
    response = test_client.patch(f"/api/instances/pool/{pool_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == update_data["description"]
    assert data["alertThreshold"] == update_data["alertThreshold"]


def test_delete_pool(test_client, sample_pool_data, auth_headers):
    # First create a pool
    create_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert create_response.status_code == 201
    pool_id = create_response.json()["id"]

    # Then delete it
    response = test_client.delete(f"/api/instances/pool/{pool_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = test_client.get(f"/api/instances/pool/{pool_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_pool_by_name(test_client, sample_pool_data, auth_headers):
    # First create a pool
    create_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert create_response.status_code == 201

    # Delete the pool by name
    response = test_client.delete(f"/api/instances/pool/name:{sample_pool_data['name']}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = test_client.get(f"/api/instances/pool/name:{sample_pool_data['name']}", headers=auth_headers)
    assert get_response.status_code == 404
