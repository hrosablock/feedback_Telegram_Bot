# import asyncio
from contextlib import suppress

# from motor.motor_asyncio import AsyncIOMotorClient
# from pymongo.errors import DuplicateKeyError
from motor.core import AgnosticDatabase as ADB

from aiogram import F, Bot, Router, html
from aiogram.filters import (CommandStart, Command)
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from html import escape as htmlescape
from env import admin_id

router = Router()

current_reply = []

is_mailing = False

router.message.filter(F.from_user.id == admin_id)
router.callback_query.filter(F.from_user.id == admin_id)

@router.message(CommandStart())
async def admin_start_handler(message: Message) -> None:

    await message.answer(f"Hello, admin {html.bold(htmlescape(message.from_user.full_name))}!\n\n"
                         "/mailing - Start mailing")



@router.callback_query(F.data.startswith("ban_"))
async def callbacks_ban(callback: CallbackQuery, bot : Bot, db: ADB):
    with suppress(TelegramBadRequest):
        id = int(callback.data.split("_")[1])

        messages = await db.users.find_one({'_id': int(id)})

        blocked = await db.users.find_one({'_id': 'blocked'})

        if id not in blocked['users']:
            
            await db.users.update_one({'_id': 'blocked'}, {'$push': {'users': int(id)}})

            await bot.send_message(chat_id=id, text="You've been blocked by the administrator")

            await bot.delete_messages(chat_id=admin_id, message_ids=messages['ids'])

            await db.users.update_one({'_id': id}, {'$set': {'ids': []}})

        await callback.answer()



@router.callback_query(F.data == 'del')
async def callbacks_del(callback: CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.delete()
        await callback.answer()



@router.callback_query(F.data.startswith("reply_"))
async def callbacks_reply(callback: CallbackQuery, db: ADB, bot : Bot):
    with suppress(TelegramBadRequest):
        id = callback.data.split("_")[1]
        msgid = callback.data.split("_")[2]

        current_reply.append({'id': id, 'msgid': msgid})

        await callback.message.answer(text="Your reply to the user(Add only 1 attachment):")
        await callback.answer()

@router.message(Command('mailing'))
async def mailing(message: Message):
    global is_mailing
    is_mailing = True
    await message.answer(text="Send message for mailing(Add only 1 attachment)")



@router.message(~F.text)
async def reply_with_content_handler(message: Message, db: ADB) -> None:
    with suppress(TelegramBadRequest):
        global is_mailing
        if is_mailing:
            cursor = db.users.find({})
            messages = await cursor.to_list(length=None)
            for msg in messages:
                if msg['is_active']:
                    with suppress(TelegramForbiddenError):
                        await message.copy_to(chat_id=msg['_id'])
            is_mailing = False
        else:
            try:
                reply = current_reply.pop()
                try:
                    if message.caption is None:
                        await message.copy_to(chat_id=reply['id'],reply_to_message_id=reply['msgid'], caption=f"Reply from admin")
                    else:
                        await message.copy_to(chat_id=reply['id'],reply_to_message_id=reply['msgid'], caption=f"Reply from admin:\n\n{htmlescape(message.caption)}")
                except TypeError:
                        await message.answer("Sorry, we don't work with this type of message")
            except IndexError:
                await message.answer('🤷‍♂️')



@router.message(F.text)
async def reply_handler(message: Message, bot : Bot, db: ADB) -> None:
    with suppress(TelegramBadRequest):
        global is_mailing
        if is_mailing:
            cursor = db.users.find({})
            messages = await cursor.to_list(length=None)
            for msg in messages:
                if msg['is_active']:
                    with suppress(TelegramForbiddenError):
                        await message.copy_to(chat_id=msg['_id'])
            is_mailing = False
        else:
            try:
                reply = current_reply.pop()
                await bot.send_message(chat_id=reply['id'],reply_to_message_id=reply['msgid'], text=f"Reply from admin:\n{htmlescape(message.text)}")
            except IndexError:
                await message.answer('🤷‍♂️')
