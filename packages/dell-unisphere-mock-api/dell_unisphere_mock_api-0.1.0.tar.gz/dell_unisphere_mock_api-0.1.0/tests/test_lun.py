import pytest
from fastapi.testclient import TestClient
from dell_unisphere_mock_api.main import app

@pytest.fixture
def sample_pool_data():
    return {
        "name": "test_pool",
        "description": "Test pool for unit tests",
        "raidType": "RAID5",
        "sizeFree": 1000000000000,  # 1TB free
        "sizeTotal": 2000000000000,  # 2TB total
        "sizeUsed": 1000000000000,  # 1TB used
        "sizeSubscribed": 1500000000000,
        "poolType": "Performance",
        "alertThreshold": 80,
        "poolFastVP": True,
        "isFASTCacheEnabled": False,
        "isFASTVpScheduleEnabled": True,
        "isHarvestEnabled": True,
    }

@pytest.fixture
def sample_lun_data():
    return {
        "name": "test_lun",
        "description": "Test LUN for unit tests",
        "lunType": "GenericStorage",
        "size": 100000000000,  # 100GB
        "pool_id": None,  # Will be set in tests after pool creation
        "tieringPolicy": "Autotier",
        "defaultNode": 0,
        "isCompressionEnabled": False,
        "isThinEnabled": True,
        "isDataReductionEnabled": False,
        "hostAccess": []
    }

def test_create_lun(test_client, sample_pool_data, sample_lun_data, auth_headers):
    # First create a pool
    pool_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert pool_response.status_code == 201
    pool_id = pool_response.json()["id"]
    sample_lun_data["pool_id"] = pool_id

    # Then create a LUN
    response = test_client.post("/api/types/lun/instances", json=sample_lun_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_lun_data["name"]
    assert data["description"] == sample_lun_data["description"]
    assert data["pool_id"] == pool_id
    assert "id" in data
    assert "wwn" in data

def test_get_lun(test_client, sample_pool_data, sample_lun_data, auth_headers):
    # First create a pool
    pool_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert pool_response.status_code == 201
    pool_id = pool_response.json()["id"]
    sample_lun_data["pool_id"] = pool_id

    # Then create a LUN
    create_response = test_client.post("/api/types/lun/instances", json=sample_lun_data, headers=auth_headers)
    assert create_response.status_code == 201
    lun_id = create_response.json()["id"]

    # Then get it by ID
    response = test_client.get(f"/api/instances/lun/{lun_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == lun_id
    assert data["name"] == sample_lun_data["name"]

def test_get_lun_by_name(test_client, sample_pool_data, sample_lun_data, auth_headers):
    # First create a pool
    pool_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert pool_response.status_code == 201
    pool_id = pool_response.json()["id"]
    sample_lun_data["pool_id"] = pool_id

    # Then create a LUN
    create_response = test_client.post("/api/types/lun/instances", json=sample_lun_data, headers=auth_headers)
    assert create_response.status_code == 201

    # Then get it by name
    response = test_client.get(f"/api/instances/lun/name:{sample_lun_data['name']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_lun_data["name"]

def test_list_luns(test_client, sample_pool_data, sample_lun_data, auth_headers):
    # First create a pool
    pool_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert pool_response.status_code == 201
    pool_id = pool_response.json()["id"]
    sample_lun_data["pool_id"] = pool_id

    # Create a LUN
    create_response = test_client.post("/api/types/lun/instances", json=sample_lun_data, headers=auth_headers)
    assert create_response.status_code == 201

    # List all LUNs
    response = test_client.get("/api/types/lun/instances", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_luns_by_pool(test_client, sample_pool_data, sample_lun_data, auth_headers):
    # First create a pool
    pool_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert pool_response.status_code == 201
    pool_id = pool_response.json()["id"]
    sample_lun_data["pool_id"] = pool_id

    # Create a LUN
    create_response = test_client.post("/api/types/lun/instances", json=sample_lun_data, headers=auth_headers)
    assert create_response.status_code == 201

    # Get LUNs by pool
    response = test_client.get(f"/api/types/lun/instances?filter=pool_id eq '{pool_id}'", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(lun["pool_id"] == pool_id for lun in data)

def test_modify_lun(test_client, sample_pool_data, sample_lun_data, auth_headers):
    # First create a pool
    pool_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert pool_response.status_code == 201
    pool_id = pool_response.json()["id"]
    sample_lun_data["pool_id"] = pool_id

    # Create a LUN
    create_response = test_client.post("/api/types/lun/instances", json=sample_lun_data, headers=auth_headers)
    assert create_response.status_code == 201
    lun_id = create_response.json()["id"]

    # Modify the LUN
    update_data = {
        "description": "Updated LUN description",
        "isCompressionEnabled": True
    }
    response = test_client.patch(f"/api/instances/lun/{lun_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == update_data["description"]
    assert data["isCompressionEnabled"] == update_data["isCompressionEnabled"]

def test_delete_lun(test_client, sample_pool_data, sample_lun_data, auth_headers):
    # First create a pool
    pool_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert pool_response.status_code == 201
    pool_id = pool_response.json()["id"]
    sample_lun_data["pool_id"] = pool_id

    # Create a LUN
    create_response = test_client.post("/api/types/lun/instances", json=sample_lun_data, headers=auth_headers)
    assert create_response.status_code == 201
    lun_id = create_response.json()["id"]

    # Delete the LUN
    response = test_client.delete(f"/api/instances/lun/{lun_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = test_client.get(f"/api/instances/lun/{lun_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_lun_by_name(test_client, sample_pool_data, sample_lun_data, auth_headers):
    # First create a pool
    pool_response = test_client.post("/api/types/pool/instances", json=sample_pool_data, headers=auth_headers)
    assert pool_response.status_code == 201
    pool_id = pool_response.json()["id"]
    sample_lun_data["pool_id"] = pool_id

    # Create a LUN
    create_response = test_client.post("/api/types/lun/instances", json=sample_lun_data, headers=auth_headers)
    assert create_response.status_code == 201

    # Delete the LUN by name
    response = test_client.delete(f"/api/instances/lun/name:{sample_lun_data['name']}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = test_client.get(f"/api/instances/lun/name:{sample_lun_data['name']}", headers=auth_headers)
    assert get_response.status_code == 404
