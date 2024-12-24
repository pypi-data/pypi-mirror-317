from typing import List

from fastapi import HTTPException

from dell_unisphere_mock_api.models.filesystem import FilesystemModel
from dell_unisphere_mock_api.schemas.filesystem import FilesystemCreate, FilesystemUpdate


class FilesystemController:
    def __init__(self):
        self.filesystem_model = FilesystemModel()

    async def create_filesystem(self, filesystem_data: FilesystemCreate) -> dict:
        try:
            # Validate NAS server existence (in a real implementation)
            # Validate pool existence and capacity (in a real implementation)

            filesystem = self.filesystem_model.create_filesystem(filesystem_data.model_dump())
            return filesystem
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_filesystem(self, filesystem_id: str) -> dict:
        filesystem = self.filesystem_model.get_filesystem(filesystem_id)
        if not filesystem:
            raise HTTPException(status_code=404, detail="Filesystem not found")
        return filesystem

    async def list_filesystems(self) -> List[dict]:
        return self.filesystem_model.list_filesystems()

    async def update_filesystem(self, filesystem_id: str, update_data: FilesystemUpdate) -> dict:
        # Get current filesystem
        current_filesystem = self.filesystem_model.get_filesystem(filesystem_id)
        if not current_filesystem:
            raise HTTPException(status_code=404, detail="Filesystem not found")

        # Validate size increase (in a real implementation)
        update_dict = update_data.dict(exclude_unset=True)
        if "size" in update_dict:
            if update_dict["size"] < current_filesystem["size"]:
                raise HTTPException(status_code=400, detail="Filesystem size cannot be decreased")

            # Check pool capacity (in a real implementation)
            pass

        filesystem = self.filesystem_model.update_filesystem(filesystem_id, update_dict)
        if not filesystem:
            raise HTTPException(status_code=404, detail="Filesystem not found")
        return filesystem

    async def delete_filesystem(self, filesystem_id: str) -> None:
        # Check if filesystem has shares
        filesystem = self.filesystem_model.get_filesystem(filesystem_id)
        if not filesystem:
            raise HTTPException(status_code=404, detail="Filesystem not found")

        if filesystem["cifsShares"] or filesystem["nfsShares"]:
            raise HTTPException(status_code=400, detail="Cannot delete filesystem with active shares")

        if not self.filesystem_model.delete_filesystem(filesystem_id):
            raise HTTPException(status_code=404, detail="Filesystem not found")

    async def add_share(self, filesystem_id: str, share_id: str, share_type: str) -> None:
        if not self.filesystem_model.add_share(filesystem_id, share_id, share_type):
            raise HTTPException(status_code=404, detail="Filesystem not found")

    async def remove_share(self, filesystem_id: str, share_id: str, share_type: str) -> None:
        if not self.filesystem_model.remove_share(filesystem_id, share_id, share_type):
            raise HTTPException(status_code=404, detail="Filesystem not found")
