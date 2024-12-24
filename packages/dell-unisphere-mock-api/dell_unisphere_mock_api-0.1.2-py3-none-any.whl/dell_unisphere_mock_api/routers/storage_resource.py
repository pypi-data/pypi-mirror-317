from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException

from dell_unisphere_mock_api.core.auth import get_current_user
from dell_unisphere_mock_api.models.storage_resource import StorageResourceModel

router = APIRouter()
storage_resource_model = StorageResourceModel()


@router.post("/types/storageResource/instances", status_code=201)
async def create_storage_resource(resource_data: dict, current_user: dict = Depends(get_current_user)) -> dict:
    """Create a new storage resource instance."""
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create storage resources")

    return storage_resource_model.create_storage_resource(resource_data)


@router.get("/types/storageResource/instances")
async def list_storage_resources(
    current_user: dict = Depends(get_current_user),
) -> List[dict]:
    """List all storage resource instances."""
    return storage_resource_model.list_storage_resources()


@router.get("/types/storageResource/instances/{resource_id}")
async def get_storage_resource(resource_id: str, current_user: dict = Depends(get_current_user)) -> dict:
    """Get a specific storage resource instance by ID."""
    resource = storage_resource_model.get_storage_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Storage resource not found")
    return resource


@router.patch("/types/storageResource/instances/{resource_id}")
async def update_storage_resource(
    resource_id: str, update_data: dict, current_user: dict = Depends(get_current_user)
) -> dict:
    """Update a specific storage resource instance."""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update storage resources")

    resource = storage_resource_model.update_storage_resource(resource_id, update_data)
    if not resource:
        raise HTTPException(status_code=404, detail="Storage resource not found")
    return resource


@router.delete("/types/storageResource/instances/{resource_id}")
async def delete_storage_resource(resource_id: str, current_user: dict = Depends(get_current_user)) -> dict:
    """Delete a specific storage resource instance."""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete storage resources")

    success = storage_resource_model.delete_storage_resource(resource_id)
    if not success:
        raise HTTPException(status_code=404, detail="Storage resource not found")
    return {"message": "Storage resource deleted successfully"}


@router.post("/types/storageResource/instances/{resource_id}/action/modifyHostAccess")
async def modify_host_access(
    resource_id: str, host_access: dict, current_user: dict = Depends(get_current_user)
) -> dict:
    """Modify host access for a storage resource."""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to modify host access")

    # Get the resource first to check it exists
    resource = storage_resource_model.get_storage_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Storage resource not found")

    # Update host access
    success = storage_resource_model.update_host_access(
        resource_id=resource_id,
        host_id=host_access["host"],
        access_type=host_access["accessType"],
    )

    if not success:
        raise HTTPException(status_code=400, detail="Failed to update host access")

    return storage_resource_model.get_storage_resource(resource_id)
