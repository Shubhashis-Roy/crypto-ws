from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException
import asyncio
import time

from app.websocket_manager import ConnectionManager
from app.binance_client import listen_binance
from app.state import latest_price 

app = FastAPI()
manager = ConnectionManager()

client_last_message = {}
RATE_LIMIT_SECONDS = 0.1

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(listen_binance(manager))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

            now = time.time()
            last = client_last_message.get(websocket, 0)

            if now - last < RATE_LIMIT_SECONDS:
                continue

            client_last_message[websocket] = now

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        client_last_message.pop(websocket, None)

# Get all price
@app.get("/price")
async def get_all_prices():
    try:
        return latest_price
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch all prices: {str(e)}"
        )

# Get price by symbol
@app.get("/price/{symbol}")
async def get_price(symbol: str):
    try:
        result = latest_price.get(symbol.upper())
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Symbol '{symbol}' not found"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching price for {symbol}: {str(e)}"
        )