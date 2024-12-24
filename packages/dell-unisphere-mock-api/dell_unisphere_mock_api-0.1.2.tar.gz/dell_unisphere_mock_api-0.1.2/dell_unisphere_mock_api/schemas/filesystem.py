from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class FilesystemTypeEnum(str, Enum):
    FileSystem = "FileSystem"
    VMware = "VMware"


class FilesystemSnapAccessTypeEnum(str, Enum):
    Checkpoint = "Checkpoint"
    Protocol = "Protocol"


class FilesystemHealthEnum(str, Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


class FilesystemBase(BaseModel):
    name: str = Field(..., description="User-specified filesystem name")
    description: Optional[str] = Field(None, description="User-specified filesystem description")
    nasServer: str = Field(..., description="NAS server that hosts the filesystem")
    pool: str = Field(..., description="Storage pool that contains the filesystem")
    size: int = Field(..., description="Size of the filesystem in bytes")
    supportedProtocols: List[str] = Field(default=["NFS", "CIFS"], description="Supported access protocols")
    isReadOnly: bool = Field(False, description="Indicates if the filesystem is read-only")
    isThinEnabled: bool = Field(True, description="Indicates if thin provisioning is enabled")
    isCacheEnabled: bool = Field(True, description="Indicates if caching is enabled")
    isCompressionEnabled: bool = Field(False, description="Indicates if compression is enabled")
    isAdvancedDedupEnabled: bool = Field(False, description="Indicates if advanced deduplication is enabled")


class FilesystemCreate(FilesystemBase):
    pass


class FilesystemUpdate(BaseModel):
    description: Optional[str] = None
    size: Optional[int] = None
    isReadOnly: Optional[bool] = None
    isCacheEnabled: Optional[bool] = None
    isCompressionEnabled: Optional[bool] = None
    isAdvancedDedupEnabled: Optional[bool] = None


class FilesystemResponse(FilesystemBase):
    id: str = Field(..., description="Unique identifier of the filesystem")
    health: FilesystemHealthEnum = Field(..., description="Health status of the filesystem")
    type: FilesystemTypeEnum = Field(FilesystemTypeEnum.FileSystem, description="Type of the filesystem")
    sizeAllocated: int = Field(..., description="Actual space allocated to the filesystem")
    sizeUsed: int = Field(..., description="Space used by the filesystem")
    cifsShares: List[str] = Field([], description="List of CIFS shares on this filesystem")
    nfsShares: List[str] = Field([], description="List of NFS shares on this filesystem")
    created: datetime = Field(..., description="Creation timestamp")
    modified: datetime = Field(..., description="Last modification timestamp")
    model_config = ConfigDict(from_attributes=True)
