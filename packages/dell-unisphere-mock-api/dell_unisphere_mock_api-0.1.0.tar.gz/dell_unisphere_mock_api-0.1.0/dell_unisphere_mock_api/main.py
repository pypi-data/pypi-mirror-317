from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from dell_unisphere_mock_api.core.auth import get_current_user, verify_csrf_token
from dell_unisphere_mock_api.routers import (
    storage_resource,
    filesystem,
    nas_server,
    pool,
    lun,
    pool_unit,
    disk_group,
    disk,
    auth
)
from datetime import timedelta
from fastapi import status

# Initialize FastAPI app
app = FastAPI(
    title="Mock Unity Unisphere API",
    description="""
A mock implementation of Dell Unity Unisphere Management REST API.

## Authentication

This API uses HTTP Basic Authentication with additional Dell Unisphere specific requirements:

1. Include your credentials in the Authorization header:
   `Authorization: Basic base64(username:password)`

2. Include the X-EMC-REST-CLIENT header:
   `X-EMC-REST-CLIENT: true`

3. For POST and DELETE requests, include the EMC-CSRF-TOKEN header with the token received from the server.

Default credentials:
- Username: `admin`
- Password: `Password123!`

## Features

- Storage Resource Management
- Filesystem Management
- NAS Server Management
- Pool Management
- LUN Management
- Pool Unit Management
- Disk Group Management
- Disk Management
""",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to verify CSRF token for POST, PATCH and DELETE requests
@app.middleware("http")
async def csrf_middleware(request: Request, call_next):
    try:
        verify_csrf_token(request, request.method)
    except HTTPException as e:
        if e.status_code == status.HTTP_403_FORBIDDEN:
            return Response(
                content=str(e.detail),
                status_code=e.status_code,
                headers=e.headers
            )
    response = await call_next(request)
    return response

# Configure routers
app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(storage_resource.router, prefix="/api", tags=["Storage Resource"], dependencies=[Depends(get_current_user)])
app.include_router(filesystem.router, prefix="/api", tags=["Filesystem"], dependencies=[Depends(get_current_user)])
app.include_router(nas_server.router, prefix="/api", tags=["NAS Server"], dependencies=[Depends(get_current_user)])
app.include_router(pool.router, prefix="/api", tags=["Pool"], dependencies=[Depends(get_current_user)])
app.include_router(lun.router, prefix="/api", tags=["LUN"], dependencies=[Depends(get_current_user)])
app.include_router(pool_unit.router, prefix="/api", tags=["Pool Unit"], dependencies=[Depends(get_current_user)])
app.include_router(disk_group.router, prefix="/api", tags=["Disk Group"], dependencies=[Depends(get_current_user)])
app.include_router(disk.router, prefix="/api", tags=["Disk"], dependencies=[Depends(get_current_user)])

@app.get("/api/instances/system/0")
async def get_system_details(current_user: dict = Depends(get_current_user)):
    return {
        "content": {
            "id": "APM00123456789",
            "model": "Unity 380",
            "name": "Unity-380",
            "softwareVersion": "5.0.0.0.0.001",
            "apiVersion": "10.0",
            "earliestApiVersion": "5.0",
            "platform": "Platform2",
            "mac": "00:60:16:5C:B7:E0"
        }
    }

@app.get("/api/types/system/0/basicSystemInfo")
async def get_system_info():
    """This endpoint is accessible without authentication as per Dell Unisphere API spec."""
    return {
        "content": {
            "name": "Unity-380",
            "model": "Unity 380",
            "serialNumber": "APM00123456789",
            "softwareVersion": "5.0.0.0.0.001"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
