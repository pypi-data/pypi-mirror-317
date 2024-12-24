from typing import List

from fastapi import HTTPException

from dell_unisphere_mock_api.models.nas_server import NasServerModel
from dell_unisphere_mock_api.schemas.nas_server import NasServerCreate, NasServerUpdate


class NasServerController:
    def __init__(self):
        self.nas_server_model = NasServerModel()

    async def create_nas_server(self, nas_server_data: NasServerCreate) -> dict:
        try:
            nas_server = self.nas_server_model.create_nas_server(nas_server_data.model_dump())
            return nas_server
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_nas_server(self, nas_server_id: str) -> dict:
        nas_server = self.nas_server_model.get_nas_server(nas_server_id)
        if not nas_server:
            raise HTTPException(status_code=404, detail="NAS server not found")
        return nas_server

    async def list_nas_servers(self) -> List[dict]:
        return self.nas_server_model.list_nas_servers()

    async def update_nas_server(self, nas_server_id: str, update_data: NasServerUpdate) -> dict:
        nas_server = self.nas_server_model.update_nas_server(nas_server_id, update_data.dict(exclude_unset=True))
        if not nas_server:
            raise HTTPException(status_code=404, detail="NAS server not found")
        return nas_server

    async def delete_nas_server(self, nas_server_id: str) -> None:
        if not self.nas_server_model.delete_nas_server(nas_server_id):
            raise HTTPException(status_code=404, detail="NAS server not found")
