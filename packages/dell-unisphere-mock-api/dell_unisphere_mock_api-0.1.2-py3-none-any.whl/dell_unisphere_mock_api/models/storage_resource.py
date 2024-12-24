import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional


class StorageResourceModel:
    def __init__(self):
        self.storage_resources: Dict[str, dict] = {}

    def create_storage_resource(self, resource_data: dict) -> dict:
        resource_id = str(uuid.uuid4())

        # Initialize size-related fields based on type
        size_total = resource_data.get("sizeTotal", 0)
        is_thin = resource_data.get("isThinEnabled", True)

        # Calculate initial allocated size
        size_allocated = size_total // 10 if is_thin else size_total

        resource = {
            **resource_data,
            "id": resource_id,
            "health": "OK",
            "sizeTotal": size_total,
            "sizeUsed": 0,
            "sizeAllocated": size_allocated,
            "thinStatus": "True" if is_thin else "False",
            "metadataSize": 0,
            "metadataSizeAllocated": 0,
            "snapCount": 0,
            "snapSize": 0,
            "snapSizeAllocated": 0,
            "hostAccess": [],
            "perTierSizeUsed": {},
            "created": datetime.now(timezone.utc),
            "modified": datetime.now(timezone.utc),
        }

        # Add VMware-specific fields if applicable
        if resource_data["type"] in ["VMwareFS", "VVolDatastoreFS"]:
            resource["esxFilesystemMajorVersion"] = "6"

        self.storage_resources[resource_id] = resource
        return resource

    def get_storage_resource(self, resource_id: str) -> Optional[dict]:
        return self.storage_resources.get(resource_id)

    def list_storage_resources(self, resource_type: Optional[str] = None) -> List[dict]:
        resources = list(self.storage_resources.values())
        if resource_type:
            resources = [r for r in resources if r["type"] == resource_type]
        return resources

    def update_storage_resource(self, resource_id: str, update_data: dict) -> Optional[dict]:
        if resource_id not in self.storage_resources:
            return None

        resource = self.storage_resources[resource_id]

        # Handle compression and deduplication updates
        if "isCompressionEnabled" in update_data:
            # In a real implementation, this would trigger compression
            pass

        if "isAdvancedDedupEnabled" in update_data:
            # In a real implementation, this would trigger deduplication
            pass

        # Update fields
        for key, value in update_data.items():
            if value is not None:
                resource[key] = value

        resource["modified"] = datetime.now(timezone.utc)
        return resource

    def delete_storage_resource(self, resource_id: str) -> bool:
        if resource_id not in self.storage_resources:
            return False
        del self.storage_resources[resource_id]
        return True

    def update_host_access(self, resource_id: str, host_id: str, access_type: str) -> bool:
        if resource_id not in self.storage_resources:
            return False

        resource = self.storage_resources[resource_id]
        # Check if host already has access
        for access in resource["hostAccess"]:
            if access["host"] == host_id:
                access["accessType"] = access_type
                return True

        # Add new host access
        resource["hostAccess"].append({"host": host_id, "accessType": access_type})
        return True

    def remove_host_access(self, resource_id: str, host_id: str) -> bool:
        if resource_id not in self.storage_resources:
            return False

        resource = self.storage_resources[resource_id]
        resource["hostAccess"] = [access for access in resource["hostAccess"] if access["host"] != host_id]
        return True

    def update_usage_stats(self, resource_id: str, size_used: int, tier_usage: dict) -> bool:
        if resource_id not in self.storage_resources:
            return False

        resource = self.storage_resources[resource_id]
        resource["sizeUsed"] = size_used
        resource["perTierSizeUsed"] = tier_usage

        # Update allocated size for thin provisioning
        if resource["isThinEnabled"]:
            resource["sizeAllocated"] = max(
                size_used + (1024 * 1024 * 1024),  # Add 1GB buffer
                resource["sizeAllocated"],
            )

        return True
