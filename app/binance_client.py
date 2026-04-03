import asyncio
import json
import websockets
from app.websocket_manager import ConnectionManager
from app.state import latest_price    

BINANCE_URL = "wss://stream.binance.com:9443/ws/btcusdt@ticker"

async def listen_binance(manager: ConnectionManager):

    async with websockets.connect(BINANCE_URL) as websocket:

        while True:
            data = await websocket.recv()
            parsed = json.loads(data)

            message = {
                "symbol": parsed["s"],
                "last_price": float(parsed["c"]),
                "change_percent": float(parsed["P"]),
                "timestamp": parsed["E"]
            }

            latest_price.clear()
            latest_price.update(message)

            await manager.broadcast(message)