from typing import Dict, List, Optional

from dell_unisphere_mock_api.schemas.pool_unit import PoolUnitOpStatusEnum, PoolUnitTypeEnum


class PoolUnitModel:
    def __init__(self):
        self.pool_units: Dict[str, dict] = {}
        self.next_id = 1

    def create(self, pool_unit: dict) -> dict:
        pool_unit_id = str(self.next_id)
        self.next_id += 1

        pool_unit["id"] = pool_unit_id
        self.pool_units[pool_unit_id] = pool_unit
        return pool_unit

    def get(self, pool_unit_id: str) -> Optional[dict]:
        return self.pool_units.get(pool_unit_id)

    def list(self) -> List[dict]:
        return list(self.pool_units.values())

    def update(self, pool_unit_id: str, pool_unit_update: dict) -> Optional[dict]:
        if pool_unit_id in self.pool_units:
            current_pool_unit = self.pool_units[pool_unit_id]
            for key, value in pool_unit_update.items():
                if value is not None:
                    current_pool_unit[key] = value
            return current_pool_unit
        return None

    def delete(self, pool_unit_id: str) -> bool:
        if pool_unit_id in self.pool_units:
            del self.pool_units[pool_unit_id]
            return True
        return False
