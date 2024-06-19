from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache
from env import flood_delay



class FloodMiddleware(BaseMiddleware):
    def __init__(self, timer: int=flood_delay):
        self.delay = TTLCache(maxsize=10_000, ttl=timer)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],) -> Any:
                
                if event.chat.id in self.delay:
                    return
                
                else:
                    self.delay[event.chat.id] = None
                
                return await handler(event, data)