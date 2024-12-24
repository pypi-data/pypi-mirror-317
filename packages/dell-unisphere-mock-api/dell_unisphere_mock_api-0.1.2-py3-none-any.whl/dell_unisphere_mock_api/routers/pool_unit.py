from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from dell_unisphere_mock_api.core.auth import get_current_user
from dell_unisphere_mock_api.models.pool_unit import PoolUnitModel
from dell_unisphere_mock_api.schemas.pool_unit import PoolUnit, PoolUnitCreate, PoolUnitUpdate

router = APIRouter()
pool_unit_model = PoolUnitModel()


@router.post(
    "/types/poolUnit/instances",
    response_model=PoolUnit,
    status_code=status.HTTP_201_CREATED,
)
async def create_pool_unit(pool_unit: PoolUnitCreate, current_user: dict = Depends(get_current_user)):
    """Create a new pool unit."""
    return pool_unit_model.create(pool_unit.model_dump())


@router.get("/types/poolUnit/instances", response_model=List[PoolUnit])
async def list_pool_units(current_user: dict = Depends(get_current_user)):
    """List all pool units."""
    return pool_unit_model.list()


@router.get("/types/poolUnit/instances/{pool_unit_id}", response_model=PoolUnit)
async def get_pool_unit(pool_unit_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific pool unit by ID."""
    pool_unit = pool_unit_model.get(pool_unit_id)
    if not pool_unit:
        raise HTTPException(status_code=404, detail="Pool unit not found")
    return pool_unit


@router.patch("/types/poolUnit/instances/{pool_unit_id}", response_model=PoolUnit)
async def update_pool_unit(
    pool_unit_id: str,
    pool_unit: PoolUnitUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update a pool unit."""
    updated_pool_unit = pool_unit_model.update(pool_unit_id, pool_unit.model_dump(exclude_unset=True))
    if not updated_pool_unit:
        raise HTTPException(status_code=404, detail="Pool unit not found")
    return updated_pool_unit


@router.delete("/types/poolUnit/instances/{pool_unit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pool_unit(pool_unit_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a pool unit."""
    if not pool_unit_model.delete(pool_unit_id):
        raise HTTPException(status_code=404, detail="Pool unit not found")
