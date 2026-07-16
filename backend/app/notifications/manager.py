import json
import uuid
from datetime import datetime
from typing import Dict, Set
from fastapi import WebSocket
import structlog

logger = structlog.get_logger()


class ConnectionManager:
    def __init__(self):
        self._connections: Dict[str, WebSocket] = {}
        self._client_subs: Dict[str, Set[str]] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self._connections[client_id] = websocket
        self._client_subs[client_id] = set()
        logger.info("ws_connected", client_id=client_id)

    def disconnect(self, client_id: str):
        self._connections.pop(client_id, None)
        self._client_subs.pop(client_id, None)
        logger.info("ws_disconnected", client_id=client_id)

    async def send_to_client(self, client_id: str, message: dict):
        ws = self._connections.get(client_id)
        if ws:
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(client_id)

    async def broadcast(self, message: dict, channel: str = None):
        disconnected = []
        for client_id, ws in self._connections.items():
            if channel and channel not in self._client_subs.get(client_id, set()):
                continue
            try:
                await ws.send_json(message)
            except Exception:
                disconnected.append(client_id)
        for cid in disconnected:
            self.disconnect(cid)

    def get_connected_clients(self) -> list:
        return list(self._connections.keys())

    def get_client_count(self) -> int:
        return len(self._connections)

    def subscribe_client(self, client_id: str, channel: str):
        if client_id in self._client_subs:
            self._client_subs[client_id].add(channel)

    def unsubscribe_client(self, client_id: str, channel: str):
        if client_id in self._client_subs:
            self._client_subs[client_id].discard(channel)
