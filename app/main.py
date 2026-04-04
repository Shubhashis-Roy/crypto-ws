from fastapi import FastAPI
import asyncio

from app.websocket_manager import ConnectionManager
from app.binance_client import listen_binance
from app.consumer import consume_messages

from app.routes import websocket as websocket_module
from app.routes.websocket import router as websocket_router
from app.routes.price import router as price_router

app = FastAPI()
manager = ConnectionManager()

websocket_module.manager = manager

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(listen_binance())
    asyncio.create_task(consume_messages(manager))


app.include_router(websocket_router)
app.include_router(price_router)