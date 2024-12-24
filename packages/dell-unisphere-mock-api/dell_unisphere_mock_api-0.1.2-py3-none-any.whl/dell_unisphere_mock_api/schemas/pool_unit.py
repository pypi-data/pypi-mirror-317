from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class PoolUnitTypeEnum(str, Enum):
    VIRTUAL_DISK = "Virtual_Disk"
    RAID_GROUP = "RAID_Group"


class PoolUnitOpStatusEnum(str, Enum):
    UNKNOWN = "Unknown"
    OK = "OK"
    DEGRADED = "Degraded"
    ERROR = "Error"
    NOT_READY = "Not_Ready"
    OFFLINE = "Offline"


class PoolUnitBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    health: PoolUnitOpStatusEnum = PoolUnitOpStatusEnum.OK
    type: PoolUnitTypeEnum
    size_total: int
    size_used: int
    size_free: int
    raid_type: Optional[str] = None
    disk_group: Optional[str] = None


class PoolUnitCreate(PoolUnitBase):
    pass


class PoolUnitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class PoolUnit(PoolUnitBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
