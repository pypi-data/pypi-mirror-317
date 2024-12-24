from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class RaidTypeEnum(str, Enum):
    RAID5 = "RAID5"
    RAID0 = "RAID0"
    RAID1 = "RAID1"
    RAID3 = "RAID3"
    RAID10 = "RAID10"
    RAID6 = "RAID6"
    Mixed = "Mixed"
    None_ = "None"


class RaidStripeWidthEnum(str, Enum):
    BestFit = "BestFit"
    RAID10 = "2"
    RAID5_3 = "3"
    RAID5_4 = "4"
    RAID5_5 = "5"
    RAID5_6 = "6"
    RAID5_7 = "7"
    RAID5_8 = "8"
    RAID5_9 = "9"
    RAID5_10 = "10"
    RAID5_11 = "11"
    RAID5_12 = "12"
    RAID5_13 = "13"
    RAID5_14 = "14"


class TierTypeEnum(str, Enum):
    None_ = "None"
    Extreme_Performance = "Extreme_Performance"
    Performance = "Performance"
    Capacity = "Capacity"


class FastCacheStateEnum(str, Enum):
    Enabled = "Enabled"
    Disabled = "Disabled"
    Mixed = "Mixed"


class SpaceEfficiencyEnum(str, Enum):
    Thin = "Thin"
    Thick = "Thick"
    Mixed = "Mixed"


class TieringPolicyEnum(str, Enum):
    Autotier_High = "Autotier_High"
    Autotier = "Autotier"
    Highest = "Highest"
    Lowest = "Lowest"
    No_Data_Movement = "No_Data_Movement"
    Mixed = "Mixed"


class PoolHealth(BaseModel):
    value: int = Field(..., description="Health status value")
    descriptionIds: List[str] = Field(default_factory=list, description="List of health status description IDs")
    descriptions: List[str] = Field(default_factory=list, description="List of health status descriptions")


class Pool(BaseModel):
    """Pool model that includes all pool attributes."""

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the pool",
    )
    name: str = Field(..., description="Name of the pool", min_length=1, max_length=63)
    description: Optional[str] = Field(None, description="Description of the pool", max_length=170)
    health: Optional[PoolHealth] = None
    raidType: RaidTypeEnum = Field(..., description="RAID type of the pool")
    raidStripeWidth: Optional[RaidStripeWidthEnum] = Field(None, description="RAID stripe width")
    sizeFree: int = Field(..., description="Size of available space in the pool, in bytes", ge=0)
    sizeTotal: int = Field(..., description="Total size of the pool, in bytes", ge=0)
    sizeUsed: int = Field(..., description="Size of used space in the pool, in bytes", ge=0)
    sizeSubscribed: int = Field(
        ...,
        description="Total size of space in the pool that is subscribed by all storage resources",
        ge=0,
    )
    alertThreshold: int = Field(
        80,
        description="Threshold at which the system will generate alerts about the free space in the pool",
        ge=50,
        le=84,
    )
    poolFastVP: bool = Field(True, description="Indicates whether thin provisioning is enabled for the pool")
    poolType: TierTypeEnum = Field(..., description="Type of storage tier in the pool")
    isFASTCacheEnabled: bool = Field(False, description="Indicates whether FAST Cache is enabled for the pool")
    isFASTVpScheduleEnabled: bool = Field(True, description="Indicates whether scheduled data relocations are enabled")
    isHarvestEnabled: bool = Field(True, description="Indicates whether pool space harvesting is enabled")
    model_config = ConfigDict(from_attributes=True)


class PoolCreate(BaseModel):
    """Schema for creating a new pool."""

    name: str = Field(..., description="Name of the pool", min_length=1, max_length=63)
    description: Optional[str] = Field(None, description="Description of the pool", max_length=170)
    raidType: RaidTypeEnum = Field(..., description="RAID type of the pool")
    raidStripeWidth: Optional[RaidStripeWidthEnum] = Field(None, description="RAID stripe width")
    sizeFree: int = Field(..., description="Size of available space in the pool, in bytes", ge=0)
    sizeTotal: int = Field(..., description="Total size of the pool, in bytes", ge=0)
    sizeUsed: int = Field(..., description="Size of used space in the pool, in bytes", ge=0)
    sizeSubscribed: int = Field(
        ...,
        description="Total size of space in the pool that is subscribed by all storage resources",
        ge=0,
    )
    poolType: TierTypeEnum = Field(..., description="Type of storage tier in the pool")


class PoolUpdate(BaseModel):
    """Schema for updating an existing pool."""

    name: Optional[str] = Field(None, description="New name for the pool", min_length=1, max_length=63)
    description: Optional[str] = Field(None, description="New description for the pool", max_length=170)
    alertThreshold: Optional[int] = Field(None, description="New alert threshold", ge=50, le=84)
    isFASTCacheEnabled: Optional[bool] = Field(None, description="Enable/disable FAST Cache")
    isFASTVpScheduleEnabled: Optional[bool] = Field(None, description="Enable/disable scheduled data relocations")
    isHarvestEnabled: Optional[bool] = Field(None, description="Enable/disable pool space harvesting")
