from typing import List, Optional

from fastapi import HTTPException

from dell_unisphere_mock_api.controllers.pool_controller import PoolController
from dell_unisphere_mock_api.models.lun import LUNModel
from dell_unisphere_mock_api.schemas.lun import LUN, LUNCreate, LUNUpdate


class LUNController:
    def __init__(self):
        self.lun_model = LUNModel()
        self.pool_controller = PoolController()

    def create_lun(self, lun_create: LUNCreate) -> LUN:
        """Create a new LUN."""
        # Validate pool exists and has enough space
        pool = self.pool_controller.get_pool(str(lun_create.pool_id))
        if not pool:
            raise HTTPException(status_code=404, detail="Pool not found")

        if pool.sizeFree < lun_create.size:
            raise HTTPException(status_code=400, detail="Pool does not have enough free space")

        # Check if LUN with same name exists
        existing_lun = self.lun_model.get_lun_by_name(lun_create.name)
        if existing_lun:
            raise HTTPException(status_code=409, detail="LUN with this name already exists")

        # Create the LUN
        return self.lun_model.create_lun(lun_create)

    def get_lun(self, lun_id: str) -> Optional[LUN]:
        """Get a LUN by ID."""
        lun = self.lun_model.get_lun(lun_id)
        if not lun:
            raise HTTPException(status_code=404, detail=f"LUN with ID '{lun_id}' not found")
        return lun

    def get_lun_by_name(self, name: str) -> Optional[LUN]:
        """Get a LUN by name."""
        lun = self.lun_model.get_lun_by_name(name)
        if not lun:
            raise HTTPException(status_code=404, detail=f"LUN with name '{name}' not found")
        return lun

    def list_luns(self) -> List[LUN]:
        """List all LUNs."""
        return self.lun_model.list_luns()

    def get_luns_by_pool(self, pool_id: str) -> List[LUN]:
        """Get all LUNs in a pool."""
        return self.lun_model.get_luns_by_pool(pool_id)

    def update_lun(self, lun_id: str, lun_update: LUNUpdate) -> Optional[LUN]:
        """Update a LUN."""
        # Get existing LUN
        current_lun = self.lun_model.get_lun(lun_id)
        if not current_lun:
            raise HTTPException(status_code=404, detail=f"LUN with ID '{lun_id}' not found")

        # If name is being changed, check for conflicts
        if lun_update.name and lun_update.name != current_lun.name:
            existing_lun = self.lun_model.get_lun_by_name(lun_update.name)
            if existing_lun:
                raise HTTPException(status_code=409, detail="LUN with this name already exists")

        return self.lun_model.update_lun(lun_id, lun_update)

    def delete_lun(self, lun_id: str) -> bool:
        """Delete a LUN."""
        if not self.lun_model.delete_lun(lun_id):
            raise HTTPException(status_code=404, detail=f"LUN with ID '{lun_id}' not found")
        return True
