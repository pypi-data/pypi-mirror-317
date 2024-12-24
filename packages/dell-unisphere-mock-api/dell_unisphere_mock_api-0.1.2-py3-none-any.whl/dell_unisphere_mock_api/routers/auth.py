from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from dell_unisphere_mock_api.core.auth import generate_csrf_token, get_current_user

router = APIRouter()


@router.post("/auth", dependencies=[])  # Remove CSRF token verification for login
async def login(response: Response, current_user: dict = Depends(get_current_user)):
    """Login endpoint that returns a CSRF token."""
    csrf_token = generate_csrf_token()
    response.headers["EMC-CSRF-TOKEN"] = csrf_token
    return {"success": True}
