from typing import Dict, List, Optional

from dell_unisphere_mock_api.schemas.disk import DiskTierEnum, DiskTypeEnum


class DiskModel:
    def __init__(self):
        self.disks: Dict[str, dict] = {}
        self.next_id = 1

    def create(self, disk: dict) -> dict:
        disk_id = str(self.next_id)
        self.next_id += 1

        disk["id"] = disk_id
        self.disks[disk_id] = disk
        return disk

    def get(self, disk_id: str) -> Optional[dict]:
        return self.disks.get(disk_id)

    def list(self) -> List[dict]:
        return list(self.disks.values())

    def update(self, disk_id: str, disk_update: dict) -> Optional[dict]:
        if disk_id in self.disks:
            current_disk = self.disks[disk_id]
            for key, value in disk_update.items():
                if value is not None:
                    current_disk[key] = value
            return current_disk
        return None

    def delete(self, disk_id: str) -> bool:
        if disk_id in self.disks:
            del self.disks[disk_id]
            return True
        return False

    def get_by_pool(self, pool_id: str) -> List[dict]:
        """Get all disks associated with a specific pool."""
        return [disk for disk in self.disks.values() if disk.get("pool_id") == pool_id]

    def get_by_disk_group(self, disk_group_id: str) -> List[dict]:
        """Get all disks associated with a specific disk group."""
        return [disk for disk in self.disks.values() if disk.get("disk_group_id") == disk_group_id]

    def validate_disk_type(self, disk_type: str) -> bool:
        """Validate disk type and set appropriate tier type."""
        disk_to_tier = {
            "SAS_FLASH": "Extreme_Performance",
            "SAS": "Performance",
            "NL_SAS": "Capacity",
        }
        return disk_type in disk_to_tier
