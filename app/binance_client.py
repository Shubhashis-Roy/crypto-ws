import asyncio
import json
import websockets
from app.websocket_manager import ConnectionManager

BINANCE_URL = "wss://stream.binance.com:9443/ws/btcusdt@ticker"

async def listen_binance(manager: ConnectionManager):
    async with websockets.connect(BINANCE_URL) as websocket:
        while True:
            data = await websocket.recv()
            parsed = json.loads(data)

            message = {
                "symbol": parsed["s"],
                "price": float(parsed["c"]),
                "change_percent": float(parsed["P"]),
                "timestamp": parsed["E"]
            }

            await manager.broadcast(message)