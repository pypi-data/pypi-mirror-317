from typing import List, Optional
from uuid import uuid4

from dell_unisphere_mock_api.models.pool import PoolModel
from dell_unisphere_mock_api.schemas.pool import Pool, PoolCreate, PoolUpdate


class PoolController:
    def __init__(self):
        self.pool_model = PoolModel()

    def create_pool(self, pool_create: PoolCreate) -> Pool:
        """Create a new storage pool."""
        # Check if pool with same name exists
        existing_pool = self.pool_model.get_pool_by_name(pool_create.name)
        if existing_pool:
            raise ValueError("Pool with this name already exists")

        # Create the pool
        pool_dict = pool_create.model_dump()
        pool_dict["id"] = str(uuid4())
        pool = Pool(**pool_dict)
        return self.pool_model.create_pool(pool)

    def get_pool(self, pool_id: str) -> Optional[Pool]:
        """Get a pool by ID."""
        return self.pool_model.get_pool(pool_id)

    def get_pool_by_name(self, name: str) -> Optional[Pool]:
        """Get a pool by name."""
        return self.pool_model.get_pool_by_name(name)

    def list_pools(self) -> List[Pool]:
        """List all pools."""
        return self.pool_model.list_pools()

    def update_pool(self, pool_id: str, pool_update: PoolUpdate) -> Optional[Pool]:
        """Update a pool."""
        # Get existing pool
        current_pool = self.pool_model.get_pool(pool_id)
        if not current_pool:
            return None

        # If name is being changed, check for conflicts
        if pool_update.name and pool_update.name != current_pool.name:
            existing_pool = self.pool_model.get_pool_by_name(pool_update.name)
            if existing_pool:
                raise ValueError("Pool with this name already exists")

        return self.pool_model.update_pool(pool_id, pool_update)

    def delete_pool(self, pool_id: str) -> bool:
        """Delete a pool."""
        return self.pool_model.delete_pool(pool_id)

    def delete_pool_by_name(self, name: str) -> bool:
        """Delete a pool by name."""
        pool = self.pool_model.get_pool_by_name(name)
        if not pool:
            return False
        return self.pool_model.delete_pool(pool.id)
