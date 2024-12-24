from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException

from dell_unisphere_mock_api.core.auth import get_current_user
from dell_unisphere_mock_api.models.nas_server import NasServerModel

router = APIRouter()
nas_server_model = NasServerModel()


@router.post("/types/nasServer/instances")
async def create_nas_server(nas_server_data: dict, current_user: dict = Depends(get_current_user)) -> dict:
    """
    Create a new NAS server instance.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create NAS servers")

    return nas_server_model.create_nas_server(nas_server_data)


@router.get("/types/nasServer/instances")
async def list_nas_servers(
    current_user: dict = Depends(get_current_user),
) -> List[dict]:
    """
    List all NAS server instances.
    """
    return nas_server_model.list_nas_servers()


@router.get("/instances/nasServer/{nas_id}")
async def get_nas_server(nas_id: str, current_user: dict = Depends(get_current_user)) -> dict:
    """
    Get a specific NAS server instance by ID.
    """
    nas_server = nas_server_model.get_nas_server(nas_id)
    if not nas_server:
        raise HTTPException(status_code=404, detail="NAS server not found")
    return nas_server


@router.patch("/types/nasServer/instances/{nas_server_id}")
async def update_nas_server(
    nas_server_id: str,
    update_data: dict,
    current_user: dict = Depends(get_current_user),
) -> dict:
    """
    Update a specific NAS server instance.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update NAS servers")

    nas_server = nas_server_model.update_nas_server(nas_server_id, update_data)
    if not nas_server:
        raise HTTPException(status_code=404, detail="NAS server not found")
    return nas_server


@router.delete("/types/nasServer/instances/{nas_server_id}")
async def delete_nas_server(nas_server_id: str, current_user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a specific NAS server instance.
    """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete NAS servers")

    success = nas_server_model.delete_nas_server(nas_server_id)
    if not success:
        raise HTTPException(status_code=404, detail="NAS server not found")
    return {"message": "NAS server deleted successfully"}
