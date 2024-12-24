"""User management router module."""

from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status

from dell_unisphere_mock_api.core.auth import MOCK_USERS, get_current_user

router = APIRouter()


@router.get("/types/user/instances", response_model=Dict)
async def get_users(current_user: Dict = Depends(get_current_user)) -> Dict:
    """
    Get a list of all users.

    Args:
        current_user: Currently authenticated user

    Returns:
        Dict containing list of users with their details
    """
    users = []
    for username, _ in MOCK_USERS.items():
        users.append(
            {
                "@base": "https://localhost:8000/api/instances/user",
                "updated": "2024-12-23T18:32:19+02:00",
                "links": [{"rel": "self", "href": f"/user_{username}"}],
                "content": {"id": f"user_{username}"},
            }
        )

    return {
        "@base": "https://localhost:8000/api/types/user/instances?per_page=2000",
        "updated": "2024-12-23T18:32:19+02:00",
        "links": [{"rel": "self", "href": "&page=1"}],
        "entries": users,
    }


@router.get("/instances/user/{user_id}", response_model=Dict)
async def get_user(user_id: str, current_user: Dict = Depends(get_current_user)) -> Dict:
    """
    Get details of a specific user.

    Args:
        user_id: ID of the user to retrieve
        current_user: Currently authenticated user

    Returns:
        Dict containing user details

    Raises:
        HTTPException: If user is not found
    """
    # Extract username from user_id (remove 'user_' prefix)
    username = user_id.replace("user_", "")

    if username not in MOCK_USERS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_data = MOCK_USERS[username]
    return {
        "@base": "https://localhost:8000/api/instances/user",
        "updated": "2024-12-23T18:32:19+02:00",
        "links": [{"rel": "self", "href": f"/user_{username}"}],
        "content": {"id": f"user_{username}", "role": user_data["role"]},
    }
