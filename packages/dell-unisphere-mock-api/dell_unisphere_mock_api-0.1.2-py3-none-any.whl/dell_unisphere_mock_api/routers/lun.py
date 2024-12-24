from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response

from dell_unisphere_mock_api.controllers.lun_controller import LUNController
from dell_unisphere_mock_api.core.auth import get_current_user
from dell_unisphere_mock_api.schemas.lun import LUN, LUNCreate, LUNUpdate

router = APIRouter()

lun_controller = LUNController()


@router.post("/types/lun/instances", response_model=LUN, status_code=201)
async def create_lun(lun: LUNCreate, _: dict = Depends(get_current_user)) -> LUN:
    """Create a new LUN."""
    return lun_controller.create_lun(lun)


@router.get("/instances/lun/name:{name}", response_model=LUN)
async def get_lun_by_name(name: str, _: dict = Depends(get_current_user)) -> LUN:
    """Get a LUN by name."""
    lun = lun_controller.get_lun_by_name(name)
    if not lun:
        raise HTTPException(status_code=404, detail="LUN not found")
    return lun


@router.get("/instances/lun/{lun_id}", response_model=LUN)
async def get_lun(lun_id: str, _: dict = Depends(get_current_user)) -> LUN:
    """Get a LUN by ID."""
    lun = lun_controller.get_lun(lun_id)
    if not lun:
        raise HTTPException(status_code=404, detail="LUN not found")
    return lun


@router.get("/types/lun/instances", response_model=List[LUN])
async def list_luns(_: dict = Depends(get_current_user)) -> List[LUN]:
    """List all LUNs."""
    return lun_controller.list_luns()


@router.patch("/instances/lun/{lun_id}", response_model=LUN)
async def modify_lun(lun_id: str, lun_update: LUNUpdate, _: dict = Depends(get_current_user)) -> LUN:
    """Modify a LUN."""
    lun = lun_controller.update_lun(lun_id, lun_update)
    if not lun:
        raise HTTPException(status_code=404, detail="LUN not found")
    return lun


@router.delete("/instances/lun/name:{name}", status_code=204)
async def delete_lun_by_name(name: str, _: dict = Depends(get_current_user)):
    """Delete a LUN by name."""
    lun = lun_controller.get_lun_by_name(name)
    if not lun:
        raise HTTPException(status_code=404, detail="LUN not found")
    lun_controller.delete_lun(lun.id)
    return Response(status_code=204)


@router.delete("/instances/lun/{lun_id}", status_code=204)
async def delete_lun(lun_id: str, _: dict = Depends(get_current_user)):
    """Delete a LUN."""
    success = lun_controller.delete_lun(lun_id)
    if not success:
        raise HTTPException(status_code=404, detail="LUN not found")
    return Response(status_code=204)


@router.get("/instances/pool/{pool_id}/luns", response_model=List[LUN])
async def get_luns_by_pool(pool_id: str, _: dict = Depends(get_current_user)) -> List[LUN]:
    """Get all LUNs in a pool."""
    return lun_controller.get_luns_by_pool(pool_id)
