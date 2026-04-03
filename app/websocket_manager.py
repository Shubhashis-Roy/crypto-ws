from typing import List
from fastapi import WebSocket
import time  

MAX_CONNECTIONS = 5
RATE_LIMIT_SECONDS = 0.2   

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.last_sent = {}   

    async def connect(self, websocket: WebSocket):
        if len(self.active_connections) >= MAX_CONNECTIONS:
            await websocket.close(code=1008)
            return

        await websocket.accept()
        self.active_connections.append(websocket)
        self.last_sent[websocket] = 0   

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        self.last_sent.pop(websocket, None)   

    async def broadcast(self, message: dict):
        now = time.time()   

        for connection in self.active_connections:
            last = self.last_sent.get(connection, 0)   

            # if now - last < RATE_LIMIT_SECONDS:  
            #     continue

            try:
                await connection.send_json(message)
                self.last_sent[connection] = now   
            except:
                pass