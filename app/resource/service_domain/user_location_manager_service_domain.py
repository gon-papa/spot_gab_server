
from fastapi import WebSocket


class UserLocationManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    # 接続
    async def connect(self, websocket: WebSocket, user_uuid: str):
        await websocket.accept()
        self.active_connections.append(user_uuid, websocket)

    # 切断
    def disconnect(self, websocket: WebSocket, user_uuid: str):
        self.active_connections.remove(user_uuid, websocket)

    # 全体に位置情報を共有
    