import asyncio
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase as ADB

from pymongo.errors import DuplicateKeyError


from aiogram import F, Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from contextlib import suppress
# from aiogram.filters import (CommandStart, Command, CommandObject)
# from aiogram.types import Message
# from html import escape as htmlescape

from handlers import admin_hd, users_hd

from env import botToken




TOKEN = botToken


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()



async def startup(db: ADB) -> Any:
    with suppress(DuplicateKeyError):
        await db.users.insert_one(
            {
                '_id': 'blocked',
                'users': []
            }
        )




async def main() -> None:

    
    #client is your MongoDB
    client = AsyncIOMotorClient(host='localhost', port=27017)
    db=client.feedback

    dp.startup.register(startup)

    dp.include_router(admin_hd.router)
    dp.include_router(users_hd.router)

    print('Started')
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    asyncio.run(main())