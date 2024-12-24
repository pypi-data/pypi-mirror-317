from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class LUNTypeEnum(str, Enum):
    GenericStorage = "GenericStorage"
    Standalone = "Standalone"
    VMware = "VMware"
    VVol = "VVol"


class TieringPolicyEnum(str, Enum):
    Autotier_High = "Autotier_High"
    Autotier = "Autotier"
    Highest = "Highest"
    Lowest = "Lowest"
    No_Data_Movement = "No_Data_Movement"
    Mixed = "Mixed"


class HostAccessEnum(str, Enum):
    NoAccess = "NoAccess"
    Production = "Production"
    Snapshot = "Snapshot"
    Both = "Both"
    Mixed = "Mixed"


class LUNHealth(BaseModel):
    value: int = Field(..., description="Health status value")
    descriptionIds: List[str] = Field(default_factory=list, description="List of health status description IDs")
    descriptions: List[str] = Field(default_factory=list, description="List of health status descriptions")


class LUNBase(BaseModel):
    name: str = Field(..., description="Name of the LUN", min_length=1, max_length=63)
    description: Optional[str] = Field(None, description="Description of the LUN", max_length=170)
    health: Optional[LUNHealth] = None
    pool_id: str = Field(..., description="ID of the pool containing this LUN")
    size: int = Field(..., description="Size of the LUN in bytes", gt=0)
    lunType: LUNTypeEnum = Field(LUNTypeEnum.GenericStorage, description="Type of LUN")
    wwn: Optional[str] = Field(None, description="World Wide Name of the LUN")
    tieringPolicy: TieringPolicyEnum = Field(TieringPolicyEnum.Autotier, description="Tiering policy for the LUN")
    isCompressionEnabled: bool = Field(False, description="Whether compression is enabled")
    isDataReductionEnabled: bool = Field(False, description="Whether data reduction is enabled")
    isThinEnabled: bool = Field(True, description="Whether thin provisioning is enabled")
    hostAccess: List[HostAccessEnum] = Field(default_factory=list, description="List of host access types")
    defaultNode: int = Field(0, description="Default node for the LUN")
    currentNode: Optional[int] = Field(None, description="Current node for the LUN")
    sizeAllocated: Optional[int] = Field(0, description="Allocated size for thin provisioning")


class LUNCreate(LUNBase):
    pass


class LUNUpdate(BaseModel):
    name: Optional[str] = Field(None, description="New name for the LUN", min_length=1, max_length=63)
    description: Optional[str] = Field(None, description="New description for the LUN", max_length=170)
    size: Optional[int] = Field(None, description="New size in bytes", gt=0)
    tieringPolicy: Optional[TieringPolicyEnum] = Field(None, description="New tiering policy")
    isCompressionEnabled: Optional[bool] = Field(None, description="Enable/disable compression")
    isDataReductionEnabled: Optional[bool] = Field(None, description="Enable/disable data reduction")
    hostAccess: Optional[List[HostAccessEnum]] = Field(None, description="New host access list")


class LUNInDB(LUNBase):
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the LUN",
    )


class LUN(LUNInDB):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "sample_lun",
                "description": "Sample LUN description",
                "pool_id": "pool-123",
                "size": 1073741824,  # 1GB
                "lunType": "GenericStorage",
                "tieringPolicy": "Autotier",
                "isCompressionEnabled": False,
                "isDataReductionEnabled": False,
                "isThinEnabled": True,
                "hostAccess": [],
                "health": {
                    "value": 5,
                    "descriptionIds": ["ALRT_COMPONENT_OK"],
                    "descriptions": ["The component is operating normally."],
                },
            }
        },
    )
