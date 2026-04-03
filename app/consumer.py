from app.queue import message_queue
from app.websocket_manager import ConnectionManager
from app.state import latest_price

async def consume_messages(manager: ConnectionManager):
    while True:
        message = await message_queue.get()

        latest_price[message["symbol"]] = message

        # await manager.broadcast(message)
        # await manager.broadcast(latest_price)
        await manager.broadcast(dict(latest_price))