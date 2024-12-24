import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional


class FilesystemModel:
    def __init__(self):
        self.filesystems: Dict[str, dict] = {}

    def create_filesystem(self, filesystem_data: dict) -> dict:
        filesystem_id = str(uuid.uuid4())
        filesystem = {
            **filesystem_data,
            "id": filesystem_id,
            "health": "OK",
            "sizeAllocated": 0,
            "sizeUsed": 0,
            "cifsShares": [],
            "nfsShares": [],
            "created": datetime.now(timezone.utc),
            "modified": datetime.now(timezone.utc),
        }

        # Calculate initial allocated size based on thin provisioning
        if filesystem.get("isThinEnabled", True):
            filesystem["sizeAllocated"] = min(filesystem["size"] // 10, 1024 * 1024 * 1024)  # 10% or 1GB
        else:
            filesystem["sizeAllocated"] = filesystem["size"]

        self.filesystems[filesystem_id] = filesystem
        return filesystem

    def get_filesystem(self, filesystem_id: str) -> Optional[dict]:
        return self.filesystems.get(filesystem_id)

    def list_filesystems(self) -> List[dict]:
        return list(self.filesystems.values())

    def update_filesystem(self, filesystem_id: str, update_data: dict) -> Optional[dict]:
        if filesystem_id not in self.filesystems:
            return None

        filesystem = self.filesystems[filesystem_id]

        # Handle size increase
        if "size" in update_data and update_data["size"] > filesystem["size"]:
            size_increase = update_data["size"] - filesystem["size"]
            if filesystem.get("isThinEnabled", True):
                filesystem["sizeAllocated"] += size_increase // 10
            else:
                filesystem["sizeAllocated"] += size_increase

        # Update other fields
        for key, value in update_data.items():
            if value is not None:
                filesystem[key] = value

        filesystem["modified"] = datetime.now(timezone.utc)
        return filesystem

    def delete_filesystem(self, filesystem_id: str) -> bool:
        if filesystem_id in self.filesystems:
            del self.filesystems[filesystem_id]
            return True
        return False

    def add_share(self, filesystem_id: str, share_id: str, share_type: str) -> bool:
        if filesystem_id not in self.filesystems:
            return False

        filesystem = self.filesystems[filesystem_id]
        if share_type.upper() == "CIFS":
            if share_id not in filesystem["cifsShares"]:
                filesystem["cifsShares"].append(share_id)
        elif share_type.upper() == "NFS":
            if share_id not in filesystem["nfsShares"]:
                filesystem["nfsShares"].append(share_id)
        else:
            return False

        return True

    def remove_share(self, filesystem_id: str, share_id: str, share_type: str) -> bool:
        if filesystem_id not in self.filesystems:
            return False

        filesystem = self.filesystems[filesystem_id]
        if share_type.upper() == "CIFS":
            if share_id in filesystem["cifsShares"]:
                filesystem["cifsShares"].remove(share_id)
        elif share_type.upper() == "NFS":
            if share_id in filesystem["nfsShares"]:
                filesystem["nfsShares"].remove(share_id)
        else:
            return False

        return True
