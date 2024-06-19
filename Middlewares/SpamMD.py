from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from motor.motor_asyncio import AsyncIOMotorClient



class SpamMiddleware(BaseMiddleware):
    def __init__(self):
        ...


    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],) -> Any:
                
                client = AsyncIOMotorClient(host='localhost', port=27017)
                blocked = await client.feedback.users.find_one({'_id': 'blocked'})
                block_list = blocked['users']
                
                if event.chat.id in block_list:
                    await event.reply(text="You've been blocked by the administrator")
                    return
                
                return await handler(event, data)