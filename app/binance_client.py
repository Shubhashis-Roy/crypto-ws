import asyncio
import json
import websockets
from app.websocket_manager import ConnectionManager
from app.state import latest_price    

BINANCE_URL = (
    "wss://stream.binance.com:9443/stream?"
    "streams=btcusdt@ticker/ethusdt@ticker/bnbusdt@ticker"
)

async def listen_binance(manager: ConnectionManager):

    async with websockets.connect(BINANCE_URL) as websocket:

        while True:
            data = await websocket.recv()
            parsed = json.loads(data)

            ticker = parsed["data"]  # important change

            message = {
                "symbol": ticker["s"],
                "price": float(ticker["c"]),
                "change_percent": float(ticker["P"]),
                "timestamp": ticker["E"]
            }

            latest_price[message["symbol"]] = message

            await manager.broadcast(message)