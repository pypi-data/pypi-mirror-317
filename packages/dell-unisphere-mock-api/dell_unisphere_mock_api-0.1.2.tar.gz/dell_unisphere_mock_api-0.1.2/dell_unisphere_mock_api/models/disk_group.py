from typing import Dict, List, Optional

from dell_unisphere_mock_api.schemas.disk_group import RaidStripeWidthEnum, RaidTypeEnum


class DiskGroupModel:
    def __init__(self):
        self.disk_groups: Dict[str, dict] = {}
        self.next_id = 1

    def create(self, disk_group: dict) -> dict:
        disk_group_id = str(self.next_id)
        self.next_id += 1

        disk_group["id"] = disk_group_id
        self.disk_groups[disk_group_id] = disk_group
        return disk_group

    def get(self, disk_group_id: str) -> Optional[dict]:
        return self.disk_groups.get(disk_group_id)

    def list(self) -> List[dict]:
        return list(self.disk_groups.values())

    def update(self, disk_group_id: str, disk_group_update: dict) -> Optional[dict]:
        if disk_group_id in self.disk_groups:
            current_disk_group = self.disk_groups[disk_group_id]
            for key, value in disk_group_update.items():
                if value is not None:
                    current_disk_group[key] = value
            return current_disk_group
        return None

    def delete(self, disk_group_id: str) -> bool:
        if disk_group_id in self.disk_groups:
            del self.disk_groups[disk_group_id]
            return True
        return False

    def validate_raid_config(self, raid_type: str, stripe_width: int, disk_count: int) -> bool:
        """Validate RAID configuration based on stripe width and disk count."""
        valid_configs = {
            "RAID5": {5: 5, 9: 9, 13: 13},  # stripe_width: required_disks
            "RAID6": {6: 6, 8: 8, 10: 10, 12: 12, 14: 14, 16: 16},
            "RAID10": {2: 2, 4: 4, 6: 6, 8: 8, 10: 10, 12: 12},
        }

        if raid_type not in valid_configs:
            return False

        if stripe_width not in valid_configs[raid_type]:
            return False

        return disk_count == valid_configs[raid_type][stripe_width]
