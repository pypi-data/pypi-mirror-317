"""Test module for user management endpoints."""

import base64

from fastapi import status
from fastapi.testclient import TestClient

from dell_unisphere_mock_api.main import app

client = TestClient(app)


def get_auth_headers(username: str = "admin", password: str = "Password123!") -> dict:
    """
    Generate authentication headers for API requests.

    Args:
        username: Username for authentication
        password: Password for authentication

    Returns:
        dict: Headers with authentication information
    """
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {credentials}", "X-EMC-REST-CLIENT": "true"}


def test_get_users_unauthorized() -> None:
    """Test getting users without authentication."""
    response = client.get("/api/types/user/instances")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_users_missing_emc_header() -> None:
    """Test getting users without X-EMC-REST-CLIENT header."""
    credentials = base64.b64encode(b"admin:Password123!").decode()
    headers = {"Authorization": f"Basic {credentials}"}
    response = client.get("/api/types/user/instances", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "X-EMC-REST-CLIENT header is required"


def test_get_users_invalid_credentials() -> None:
    """Test getting users with invalid credentials."""
    headers = get_auth_headers("wrong", "wrong")
    response = client.get("/api/types/user/instances", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"


def test_get_users_success() -> None:
    """Test getting users successfully."""
    headers = get_auth_headers()
    response = client.get("/api/types/user/instances", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "@base" in data
    assert "updated" in data
    assert "links" in data
    assert "entries" in data

    # Verify response structure
    assert data["@base"] == "https://localhost:8000/api/types/user/instances?per_page=2000"
    assert len(data["links"]) == 1
    assert data["links"][0]["rel"] == "self"
    assert data["links"][0]["href"] == "&page=1"

    # Verify entries
    assert len(data["entries"]) > 0
    first_entry = data["entries"][0]
    assert "@base" in first_entry
    assert "links" in first_entry
    assert "content" in first_entry
    assert "id" in first_entry["content"]


def test_get_specific_user_not_found() -> None:
    """Test getting a non-existent user."""
    headers = get_auth_headers()
    response = client.get("/api/instances/user/nonexistent", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_get_specific_user_success() -> None:
    """Test getting a specific user successfully."""
    headers = get_auth_headers()
    response = client.get("/api/instances/user/user_admin", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "@base" in data
    assert "updated" in data
    assert "links" in data
    assert "content" in data

    # Verify response structure
    assert data["@base"] == "https://localhost:8000/api/instances/user"
    assert len(data["links"]) == 1
    assert data["links"][0]["rel"] == "self"
    assert data["links"][0]["href"] == "/user_admin"

    # Verify user content
    assert data["content"]["id"] == "user_admin"
    assert data["content"]["role"] == "admin"
