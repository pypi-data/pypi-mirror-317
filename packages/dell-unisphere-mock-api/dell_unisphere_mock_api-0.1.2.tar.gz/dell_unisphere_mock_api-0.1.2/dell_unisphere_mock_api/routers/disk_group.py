from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from dell_unisphere_mock_api.core.auth import get_current_user
from dell_unisphere_mock_api.models.disk_group import DiskGroupModel
from dell_unisphere_mock_api.schemas.disk_group import DiskGroup, DiskGroupCreate, DiskGroupUpdate

router = APIRouter()
disk_group_model = DiskGroupModel()


@router.post(
    "/types/diskGroup/instances",
    response_model=DiskGroup,
    status_code=status.HTTP_201_CREATED,
)
async def create_disk_group(disk_group: DiskGroupCreate, current_user: dict = Depends(get_current_user)):
    """Create a new disk group."""
    # Validate RAID configuration
    if not disk_group_model.validate_raid_config(
        disk_group.raid_type, disk_group.stripe_width, len(disk_group.disk_ids)
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid RAID configuration for the given stripe width and number of disks",
        )
    return disk_group_model.create(disk_group.model_dump())


@router.get("/types/diskGroup/instances", response_model=List[DiskGroup])
async def list_disk_groups(current_user: dict = Depends(get_current_user)):
    """List all disk groups."""
    return disk_group_model.list()


@router.get("/types/diskGroup/instances/{disk_group_id}", response_model=DiskGroup)
async def get_disk_group(disk_group_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific disk group by ID."""
    disk_group = disk_group_model.get(disk_group_id)
    if not disk_group:
        raise HTTPException(status_code=404, detail="Disk group not found")
    return disk_group


@router.patch("/types/diskGroup/instances/{disk_group_id}", response_model=DiskGroup)
async def update_disk_group(
    disk_group_id: str,
    disk_group: DiskGroupUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update a disk group."""
    updated_disk_group = disk_group_model.update(disk_group_id, disk_group.model_dump(exclude_unset=True))
    if not updated_disk_group:
        raise HTTPException(status_code=404, detail="Disk group not found")
    return updated_disk_group


@router.delete("/types/diskGroup/instances/{disk_group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_disk_group(disk_group_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a disk group."""
    if not disk_group_model.delete(disk_group_id):
        raise HTTPException(status_code=404, detail="Disk group not found")
