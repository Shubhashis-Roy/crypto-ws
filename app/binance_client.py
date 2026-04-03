import asyncio
import json
import websockets
from app.websocket_manager import ConnectionManager
from app.state import latest_price    
from app.queue import message_queue


BINANCE_URL = (
    "wss://stream.binance.com:9443/stream?"
    "streams=btcusdt@ticker/ethusdt@ticker/bnbusdt@ticker"
)

async def listen_binance():

    async with websockets.connect(BINANCE_URL) as websocket:

        while True:
            data = await websocket.recv()
            parsed = json.loads(data)

            ticker = parsed["data"]

            message = {
                "symbol": ticker["s"],
                "price": float(ticker["c"]),
                "change_percent": float(ticker["P"]),
                "timestamp": ticker["E"]
            }
            
            await message_queue.put(message)