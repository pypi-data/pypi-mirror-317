import random
from typing import Dict, List, Optional
from uuid import uuid4

from dell_unisphere_mock_api.schemas.lun import LUN, LUNCreate, LUNHealth, LUNUpdate


class LUNModel:
    """Model for managing LUNs (Logical Unit Numbers)."""

    _instance = None
    luns: Dict[str, LUN]  # Class-level type annotation

    def __new__(cls) -> "LUNModel":
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.luns = {}  # Initialize in __new__
        return cls._instance

    def __init__(self) -> None:
        """Initialize the LUN model."""
        # No initialization needed as it's handled in __new__
        pass

    def _generate_wwn(self) -> str:
        """Generate a random World Wide Name for a LUN."""
        prefix = "60060160372045"
        suffix = "".join([random.choice("0123456789ABCDEF") for _ in range(18)])
        return f"{prefix}{suffix}"

    def _create_default_health(self) -> LUNHealth:
        """Create a default health status for a new LUN."""
        return LUNHealth(
            value=5,
            descriptionIds=["ALRT_COMPONENT_OK"],
            descriptions=["The component is operating normally."],
        )

    def create_lun(self, lun_create: LUNCreate) -> LUN:
        """Create a new LUN."""
        lun_dict = lun_create.model_dump()
        lun_dict["pool_id"] = str(lun_dict["pool_id"])  # Ensure pool_id is string
        lun_dict["wwn"] = self._generate_wwn()
        lun_dict["health"] = self._create_default_health()
        lun_dict["currentNode"] = lun_dict.get("defaultNode", 0)
        lun_dict["sizeAllocated"] = 0  # Initially no space allocated for thin provisioning
        lun_dict["id"] = str(uuid4())  # Explicitly set ID

        # Create LUN instance
        new_lun = LUN(**lun_dict)
        self.luns[new_lun.id] = new_lun
        return new_lun

    def get_lun(self, lun_id: str) -> Optional[LUN]:
        """Get a LUN by ID."""
        return self.luns.get(lun_id)

    def get_lun_by_name(self, name: str) -> Optional[LUN]:
        """Get a LUN by name."""
        for lun in self.luns.values():
            if lun.name == name:
                return lun
        return None

    def list_luns(self) -> List[LUN]:
        """List all LUNs."""
        return list(self.luns.values())

    def get_luns_by_pool(self, pool_id: str) -> List[LUN]:
        """Get all LUNs in a pool."""
        return [lun for lun in self.luns.values() if str(lun.pool_id) == pool_id]

    def update_lun(self, lun_id: str, lun_update: LUNUpdate) -> Optional[LUN]:
        """Update a LUN."""
        if lun_id not in self.luns:
            return None

        current_lun = self.luns[lun_id]
        update_data = lun_update.model_dump(exclude_unset=True)

        # Create updated LUN dict while preserving the id
        updated_lun_dict = current_lun.model_dump()
        updated_lun_dict.update(update_data)

        # Create new LUN instance
        updated_lun = LUN(**updated_lun_dict)
        self.luns[lun_id] = updated_lun
        return updated_lun

    def delete_lun(self, lun_id: str) -> bool:
        """Delete a LUN by ID."""
        if lun_id in self.luns:
            del self.luns[lun_id]
            return True
        return False

    def delete_lun_by_name(self, name: str) -> bool:
        """Delete a LUN by name."""
        lun = self.get_lun_by_name(name)
        if lun:
            return self.delete_lun(lun.id)
        return False
