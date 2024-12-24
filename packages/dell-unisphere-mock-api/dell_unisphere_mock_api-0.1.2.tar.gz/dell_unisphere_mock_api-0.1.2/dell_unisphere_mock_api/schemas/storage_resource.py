from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class StorageResourceTypeEnum(str, Enum):
    LUN = "LUN"
    CONSISTENCY_GROUP = "ConsistencyGroup"
    FILESYSTEM = "FileSystem"
    VMWARE_LUN = "VMwareLUN"
    VMWARE_FILESYSTEM = "VMwareFS"
    VVOL_DATASTORE_LUN = "VVolDatastoreLUN"
    VVOL_DATASTORE_FS = "VVolDatastoreFS"


class StorageResourceHealthEnum(str, Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


class ThinStatusEnum(str, Enum):
    True_ = "True"
    False_ = "False"
    Mixed = "Mixed"


class RelocationPolicyEnum(str, Enum):
    Auto = "Auto"
    Scheduled = "Scheduled"
    Manual = "Manual"


class TieringPolicyEnum(str, Enum):
    Autotier = "Autotier"
    HighestAvailable = "HighestAvailable"
    LowestAvailable = "LowestAvailable"
    NoData = "NoData"
    StartHighThenAutotier = "StartHighThenAutotier"


class StorageResourceBase(BaseModel):
    name: str = Field(..., description="User-specified storage resource name")
    description: Optional[str] = Field(None, description="User-specified description")
    type: StorageResourceTypeEnum = Field(..., description="Type of storage resource")
    pool: str = Field(..., description="Storage pool containing this resource")
    isThinEnabled: bool = Field(True, description="Whether thin provisioning is enabled")
    isCompressionEnabled: bool = Field(False, description="Whether compression is enabled")
    isAdvancedDedupEnabled: bool = Field(False, description="Whether advanced deduplication is enabled")
    tieringPolicy: Optional[TieringPolicyEnum] = Field(None, description="FAST VP tiering policy")
    relocationPolicy: Optional[RelocationPolicyEnum] = Field(None, description="Data relocation policy")


class StorageResourceCreate(StorageResourceBase):
    pass


class StorageResourceUpdate(BaseModel):
    description: Optional[str] = None
    isCompressionEnabled: Optional[bool] = None
    isAdvancedDedupEnabled: Optional[bool] = None
    tieringPolicy: Optional[TieringPolicyEnum] = None
    relocationPolicy: Optional[RelocationPolicyEnum] = None


class StorageResourceResponse(StorageResourceBase):
    id: str = Field(..., description="Unique identifier of the storage resource")
    health: StorageResourceHealthEnum = Field(..., description="Health status of the storage resource")
    sizeTotal: int = Field(..., description="Total size in bytes")
    sizeUsed: int = Field(..., description="Used size in bytes")
    sizeAllocated: int = Field(..., description="Allocated size in bytes")
    thinStatus: ThinStatusEnum = Field(..., description="Thin provisioning status")
    esxFilesystemMajorVersion: Optional[str] = Field(
        None, description="ESX filesystem major version for VMware resources"
    )
    metadataSize: int = Field(0, description="Size of metadata in bytes")
    metadataSizeAllocated: int = Field(0, description="Allocated size of metadata in bytes")
    snapCount: int = Field(0, description="Number of snapshots")
    snapSize: int = Field(0, description="Total size of snapshots in bytes")
    snapSizeAllocated: int = Field(0, description="Allocated size of snapshots in bytes")
    hostAccess: List[Dict] = Field([], description="List of hosts with access to this resource")
    perTierSizeUsed: Dict[str, int] = Field({}, description="Size used per storage tier")
    created: datetime = Field(..., description="Creation timestamp")
    modified: datetime = Field(..., description="Last modification timestamp")
