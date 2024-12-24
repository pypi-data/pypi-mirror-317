from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException

from dell_unisphere_mock_api.core.auth import get_current_user
from dell_unisphere_mock_api.models.filesystem import FilesystemModel

router = APIRouter()
filesystem_model = FilesystemModel()


@router.post("/types/filesystem/instances")
async def create_filesystem(filesystem_data: dict, current_user: dict = Depends(get_current_user)) -> dict:
    """
    Create a new filesystem instance.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create filesystems")

    return filesystem_model.create_filesystem(filesystem_data)


@router.get("/types/filesystem/instances")
async def list_filesystems(
    current_user: dict = Depends(get_current_user),
) -> List[dict]:
    """
    List all filesystem instances.
    """
    return filesystem_model.list_filesystems()


@router.get("/instances/filesystem/{filesystem_id}")
async def get_filesystem(filesystem_id: str, current_user: dict = Depends(get_current_user)) -> dict:
    """
    Get a specific filesystem instance by ID.
    """
    filesystem = filesystem_model.get_filesystem(filesystem_id)
    if not filesystem:
        raise HTTPException(status_code=404, detail="Filesystem not found")
    return filesystem


@router.patch("/types/filesystem/instances/{filesystem_id}")
async def update_filesystem(
    filesystem_id: str,
    update_data: dict,
    current_user: dict = Depends(get_current_user),
) -> dict:
    """
    Update a specific filesystem instance.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update filesystems")

    filesystem = filesystem_model.update_filesystem(filesystem_id, update_data)
    if not filesystem:
        raise HTTPException(status_code=404, detail="Filesystem not found")
    return filesystem


@router.delete("/types/filesystem/instances/{filesystem_id}")
async def delete_filesystem(filesystem_id: str, current_user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a specific filesystem instance.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete filesystems")

    success = filesystem_model.delete_filesystem(filesystem_id)
    if not success:
        raise HTTPException(status_code=404, detail="Filesystem not found")
    return {"message": "Filesystem deleted successfully"}
