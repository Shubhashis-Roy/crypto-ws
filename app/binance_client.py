import asyncio
import json
import websockets

from app.queue import message_queue

BINANCE_URL = (
    "wss://stream.binance.com:9443/stream?"
    "streams=btcusdt@ticker/ethusdt@ticker/bnbusdt@ticker"
)


async def listen_binance():
    while True:  # 🔁 reconnect loop
        try:
            print("🔌 Connecting to Binance...")

            async with websockets.connect(BINANCE_URL) as websocket:
                print("✅ Connected to Binance")

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

        except Exception as e:
            print("❌ Binance connection error:", e)
            print("⏳ Reconnecting in 5 seconds...")
            await asyncio.sleep(5)