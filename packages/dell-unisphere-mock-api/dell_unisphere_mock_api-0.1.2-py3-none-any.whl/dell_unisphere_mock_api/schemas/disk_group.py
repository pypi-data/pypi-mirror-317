from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class RaidTypeEnum(str, Enum):
    RAID5 = "RAID5"
    RAID10 = "RAID10"
    RAID6 = "RAID6"


class RaidStripeWidthEnum(int, Enum):
    TWO = 2  # RAID10 1+1
    FOUR = 4  # RAID10 2+2
    FIVE = 5  # RAID5 4+1
    SIX = 6  # RAID6 4+2 or RAID10 3+3
    EIGHT = 8  # RAID6 6+2 or RAID10 4+4
    NINE = 9  # RAID5 8+1
    TEN = 10  # RAID6 8+2 or RAID10 5+5
    TWELVE = 12  # RAID6 10+2 or RAID10 6+6
    THIRTEEN = 13  # RAID5 12+1
    FOURTEEN = 14  # RAID6 12+2
    SIXTEEN = 16  # RAID6 14+2


class DiskGroupBase(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    raid_type: RaidTypeEnum
    stripe_width: RaidStripeWidthEnum
    disk_ids: List[str]
    size_total: int
    size_used: int
    size_free: int


class DiskGroupCreate(DiskGroupBase):
    pass


class DiskGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class DiskGroup(DiskGroupBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
