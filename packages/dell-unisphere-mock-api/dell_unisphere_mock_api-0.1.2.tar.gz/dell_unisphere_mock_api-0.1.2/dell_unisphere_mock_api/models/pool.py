from typing import Dict, List, Optional

from dell_unisphere_mock_api.schemas.pool import Pool, PoolHealth, PoolUpdate, RaidTypeEnum, TierTypeEnum


class PoolModel:
    """Model for managing storage pools."""

    _instance = None
    pools: Dict[str, Pool]  # Class-level type annotation

    def __new__(cls) -> "PoolModel":
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.pools = {}  # Initialize in __new__

            # Create a test pool that matches the tutorial example
            test_pool = Pool(
                id="pool_1",
                name="Cinder_Pool",
                description="",
                raidType=RaidTypeEnum.RAID5,
                sizeFree=1975148085248,
                sizeTotal=2359010787328,
                sizeUsed=331662901248,
                sizeSubscribed=1154576531456,
                poolType=TierTypeEnum.Capacity,
                health=PoolHealth(
                    value=5,
                    descriptionIds=["ALRT_COMPONENT_OK"],
                    descriptions=["The component is operating normally. No action is required."],
                ),
            )
            cls._instance.pools[test_pool.id] = test_pool

        return cls._instance

    def __init__(self) -> None:
        """Initialize the Pool model."""
        # No initialization needed as it's handled in __new__
        pass

    def create_pool(self, pool: Pool) -> Pool:
        """Create a new storage pool."""
        self.pools[pool.id] = pool
        return pool

    def get_pool(self, pool_id: str) -> Optional[Pool]:
        """Get a pool by ID."""
        return self.pools.get(pool_id)

    def get_pool_by_name(self, name: str) -> Optional[Pool]:
        """Get a pool by name."""
        for pool in self.pools.values():
            if pool.name == name:
                return pool
        return None

    def list_pools(self) -> List[Pool]:
        """List all pools."""
        return list(self.pools.values())

    def update_pool(self, pool_id: str, pool_update: PoolUpdate) -> Optional[Pool]:
        """Update a pool."""
        if pool_id not in self.pools:
            return None

        current_pool = self.pools[pool_id]
        update_data = pool_update.model_dump(exclude_unset=True)

        updated_pool_dict = current_pool.model_dump()
        updated_pool_dict.update(update_data)

        updated_pool = Pool(**updated_pool_dict)
        self.pools[pool_id] = updated_pool
        return updated_pool

    def delete_pool(self, pool_id: str) -> bool:
        """Delete a pool by ID."""
        if pool_id in self.pools:
            del self.pools[pool_id]
            return True
        return False

    def delete_pool_by_name(self, name: str) -> bool:
        """Delete a pool by name."""
        pool = self.get_pool_by_name(name)
        if pool:
            return self.delete_pool(pool.id)
        return False
