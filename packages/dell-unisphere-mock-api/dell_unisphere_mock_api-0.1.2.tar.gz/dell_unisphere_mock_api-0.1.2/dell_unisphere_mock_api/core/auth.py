import base64
import hashlib
import os
import secrets
from typing import Dict, Optional

from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Security configuration
security = HTTPBasic()

# Mock user database for testing
MOCK_USERS: Dict[str, Dict[str, str]] = {
    "admin": {
        "username": "admin",
        "role": "admin",
        # For testing, we'll use a simple password comparison
        "password": "Password123!",  # Changed to match tutorial default
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a stored password."""
    # For testing purposes, we'll do a simple comparison
    # In production, this should use proper password hashing
    return plain_password == hashed_password


def generate_csrf_token() -> str:
    """Generate a CSRF token."""
    return base64.b64encode(os.urandom(32)).decode("utf-8")


async def get_current_user(
    request: Request,
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security),
) -> Dict[str, str]:
    """Validate credentials and return the current user."""
    # Check if X-EMC-REST-CLIENT header is present
    if request.headers.get("X-EMC-REST-CLIENT") != "true":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-EMC-REST-CLIENT header is required",
            headers={"WWW-Authenticate": "Basic"},
        )

    user = MOCK_USERS.get(credentials.username)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Set cookie for subsequent requests
    response.set_cookie(key="mod_sec_emc", value=secrets.token_urlsafe(32), httponly=True, secure=True)

    # Generate and set CSRF token
    csrf_token = generate_csrf_token()
    response.headers["EMC-CSRF-TOKEN"] = csrf_token

    return {
        "username": user["username"],
        "role": user["role"],
        "csrf_token": csrf_token,
    }


def verify_csrf_token(request: Request, method: str) -> None:
    """Verify CSRF token for POST, PATCH and DELETE requests."""
    if method not in ["POST", "PATCH", "DELETE"]:
        return

    # Skip CSRF check for the auth endpoint
    if request.url.path == "/api/auth":
        return

    # Skip CSRF check only for unauthorized requests to non-GET methods
    if not request.headers.get("Authorization"):
        return

    token = request.headers.get("EMC-CSRF-TOKEN")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="EMC-CSRF-TOKEN header is required for POST, PATCH and DELETE requests",
        )
