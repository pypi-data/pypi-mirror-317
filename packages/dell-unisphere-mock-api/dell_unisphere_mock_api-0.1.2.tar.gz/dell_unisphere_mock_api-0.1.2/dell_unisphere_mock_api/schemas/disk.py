from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class DiskTypeEnum(str, Enum):
    SAS = "SAS"
    SAS_FLASH = "SAS_FLASH"
    NL_SAS = "NL_SAS"


class DiskTierEnum(str, Enum):
    NONE = "None"
    EXTREME_PERFORMANCE = "Extreme_Performance"  # SSD/Flash
    PERFORMANCE = "Performance"  # SAS
    CAPACITY = "Capacity"  # NL-SAS


class DiskBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    disk_type: DiskTypeEnum
    tier_type: DiskTierEnum
    size: int
    disk_technology: Optional[str] = None
    rpm: Optional[int] = None
    slot_number: int
    pool_id: Optional[str] = None
    disk_group_id: Optional[str] = None
    firmware_version: Optional[str] = None
    health_status: str = "OK"


class DiskCreate(DiskBase):
    pass


class DiskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    firmware_version: Optional[str] = None


class Disk(DiskBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
