import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional


class NasServerModel:
    def __init__(self):
        self.nas_servers: Dict[str, dict] = {}

    def create_nas_server(self, nas_server_data: dict) -> dict:
        nas_server_id = str(uuid.uuid4())
        nas_server = {
            **nas_server_data,
            "id": nas_server_id,
            "health": "OK",
            "protocols": ["NFSv3"] if not nas_server_data.get("isMultiProtocolEnabled") else ["NFSv3", "CIFS"],
            "fileInterfaces": [],
            "fileSystemCount": 0,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        self.nas_servers[nas_server_id] = nas_server
        return nas_server

    def get_nas_server(self, nas_server_id: str) -> Optional[dict]:
        return self.nas_servers.get(nas_server_id)

    def list_nas_servers(self) -> List[dict]:
        return list(self.nas_servers.values())

    def update_nas_server(self, nas_server_id: str, update_data: dict) -> Optional[dict]:
        if nas_server_id not in self.nas_servers:
            return None

        nas_server = self.nas_servers[nas_server_id]
        for key, value in update_data.items():
            if value is not None:
                nas_server[key] = value

                # Update protocols if multiprotocol setting changes
                if key == "isMultiProtocolEnabled":
                    nas_server["protocols"] = ["NFSv3", "CIFS"] if value else ["NFSv3"]

        nas_server["updated_at"] = datetime.now(timezone.utc)
        return nas_server

    def delete_nas_server(self, nas_server_id: str) -> bool:
        if nas_server_id in self.nas_servers:
            del self.nas_servers[nas_server_id]
            return True
        return False
