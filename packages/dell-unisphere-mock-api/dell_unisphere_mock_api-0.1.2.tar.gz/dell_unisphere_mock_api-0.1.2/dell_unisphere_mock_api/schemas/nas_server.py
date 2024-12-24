from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class NasServerProtocolEnum(str, Enum):
    NFSv3 = "NFSv3"
    NFSv4 = "NFSv4"
    CIFS = "CIFS"
    Multiprotocol = "Multiprotocol"


class NasServerHealthEnum(str, Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


class NasServerBase(BaseModel):
    name: str = Field(..., description="User-specified NAS server name")
    description: Optional[str] = Field(None, description="User-specified NAS server description")
    homeSP: str = Field(..., description="Storage Processor (SP) that owns the NAS server")
    pool: str = Field(..., description="Storage pool that contains the NAS server")
    isReplicationDestination: bool = Field(False, description="Indicates whether this is a replication destination")
    currentSP: Optional[str] = Field(None, description="SP currently running the NAS server")
    defaultUnixUser: Optional[str] = Field(None, description="Default Unix user for NFS access")
    defaultWindowsUser: Optional[str] = Field(None, description="Default Windows user for CIFS access")
    currentUnixDirectory: Optional[str] = Field(None, description="Current Unix directory service being used")
    isMultiProtocolEnabled: bool = Field(False, description="Indicates whether multi-protocol sharing is enabled")


class NasServerCreate(NasServerBase):
    pass


class NasServerUpdate(BaseModel):
    description: Optional[str] = None
    defaultUnixUser: Optional[str] = None
    defaultWindowsUser: Optional[str] = None
    isMultiProtocolEnabled: Optional[bool] = None


class NasServerResponse(NasServerBase):
    id: str = Field(..., description="Unique identifier of the NAS server")
    health: NasServerHealthEnum = Field(..., description="Health status of the NAS server")
    protocols: List[NasServerProtocolEnum] = Field(..., description="List of protocols enabled on the NAS server")
    fileInterfaces: List[str] = Field([], description="List of file interfaces associated with the NAS server")
    fileSystemCount: int = Field(0, description="Number of file systems hosted by the NAS server")
    model_config = ConfigDict(from_attributes=True)
