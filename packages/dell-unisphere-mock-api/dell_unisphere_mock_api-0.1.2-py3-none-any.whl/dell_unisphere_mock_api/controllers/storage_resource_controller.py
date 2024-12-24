from typing import Dict, List, Optional

from fastapi import HTTPException

from dell_unisphere_mock_api.models.storage_resource import StorageResourceModel
from dell_unisphere_mock_api.schemas.storage_resource import StorageResourceCreate, StorageResourceUpdate


class StorageResourceController:
    def __init__(self):
        self.storage_resource_model = StorageResourceModel()

    async def create_storage_resource(self, resource_data: StorageResourceCreate) -> dict:
        try:
            # Validate pool existence (in a real implementation)
            # Validate pool capacity (in a real implementation)
            # Validate host IDs if provided (in a real implementation)

            # Convert Pydantic model to dict
            resource_dict = resource_data.model_dump()

            # Create the storage resource
            resource = self.storage_resource_model.create_storage_resource(resource_dict)
            return resource
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_storage_resource(self, resource_id: str) -> dict:
        resource = self.storage_resource_model.get_storage_resource(resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Storage resource not found")
        return resource

    async def list_storage_resources(self, resource_type: Optional[str] = None) -> List[dict]:
        return self.storage_resource_model.list_storage_resources(resource_type)

    async def update_storage_resource(self, resource_id: str, update_data: StorageResourceUpdate) -> dict:
        # Get current resource
        current_resource = self.storage_resource_model.get_storage_resource(resource_id)
        if not current_resource:
            raise HTTPException(status_code=404, detail="Storage resource not found")

        # Convert Pydantic model to dict
        update_dict = update_data.model_dump(exclude_unset=True)

        # Validate updates
        if "isCompressionEnabled" in update_dict and update_dict["isCompressionEnabled"]:
            # Check if compression is supported for this resource type
            if current_resource["type"] not in ["LUN", "FILESYSTEM"]:
                raise HTTPException(
                    status_code=400,
                    detail="Compression is not supported for this resource type",
                )

        if "isAdvancedDedupEnabled" in update_dict and update_dict["isAdvancedDedupEnabled"]:
            # Check if deduplication is supported for this resource type
            if current_resource["type"] not in ["LUN", "FILESYSTEM"]:
                raise HTTPException(
                    status_code=400,
                    detail="Advanced deduplication not supported for resource",
                )

        # Update the resource
        resource = self.storage_resource_model.update_storage_resource(resource_id, update_dict)
        if not resource:
            raise HTTPException(status_code=404, detail="Storage resource not found")
        return resource

    async def delete_storage_resource(self, resource_id: str) -> None:
        # Get current resource
        resource = self.storage_resource_model.get_storage_resource(resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Storage resource not found")

        # Check for snapshots
        if resource["snapCount"] > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete storage resource with existing snapshots",
            )

        # Check for host connections
        if resource["hostAccess"]:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete storage resource with active host connections",
            )

        if not self.storage_resource_model.delete_storage_resource(resource_id):
            raise HTTPException(status_code=404, detail="Storage resource not found")

    async def add_host_access(self, resource_id: str, host_id: str, access_type: str) -> dict:
        # Validate host existence (in a real implementation)
        if not self.storage_resource_model.add_host_access(resource_id, host_id, access_type):
            raise HTTPException(status_code=404, detail="Storage resource not found")
        return await self.get_storage_resource(resource_id)

    async def update_host_access(self, resource_id: str, host_id: str, access_type: str) -> dict:
        # Validate host existence (in a real implementation)
        if not self.storage_resource_model.update_host_access(resource_id, host_id, access_type):
            raise HTTPException(status_code=404, detail="Storage resource not found")
        return await self.get_storage_resource(resource_id)

    async def remove_host_access(self, resource_id: str, host_id: str) -> dict:
        if not self.storage_resource_model.remove_host_access(resource_id, host_id):
            raise HTTPException(status_code=404, detail="Storage resource not found")
        return await self.get_storage_resource(resource_id)

    async def update_usage_stats(self, resource_id: str, size_used: int, tier_usage: Dict[str, int]) -> dict:
        if not self.storage_resource_model.update_usage_stats(resource_id, size_used, tier_usage):
            raise HTTPException(status_code=404, detail="Storage resource not found")
        return await self.get_storage_resource(resource_id)
