from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

from app.websocket_manager import ConnectionManager
from app.binance_client import listen_binance

app = FastAPI()
manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(listen_binance(manager))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)