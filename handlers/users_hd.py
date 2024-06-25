# import asyncio

# from motor.motor_asyncio import AsyncIOMotorClient

from contextlib import suppress

from motor.core import AgnosticDatabase as ADB
from pymongo.errors import DuplicateKeyError

from aiogram import F, Bot, Router, html
from aiogram.filters.chat_member_updated import (ChatMemberUpdatedFilter, MEMBER, KICKED)
from aiogram.filters import (CommandStart)
from aiogram.types import Message, ChatMemberUpdated


from html import escape as htmlescape


from Middlewares.FloodMD import FloodMiddleware
from Middlewares.SpamMD import SpamMiddleware

from keyboards.callbacks import get_keyboard

from env import admin_id, flood_delay

router = Router()
router.message.middleware(FloodMiddleware())
router.message.middleware(SpamMiddleware())


@router.message(CommandStart())
async def user_start_handler(message: Message, db: ADB) -> None:

    with suppress(DuplicateKeyError):
        await db.users.insert_one(
            {
                '_id': message.from_user.id,
                'ids': [],
                'is_active': True
            }
        )

    await message.answer(f"Hello, user {html.bold(htmlescape(message.from_user.full_name))}!\n\n"
                         'Here you can send your message to the chat administration\n(Add only 1 attachment)\n\n'
                         f"Flood delay - {flood_delay} seconds")
    
@router.message(~F.text)
async def send_handler(message: Message, db: ADB) -> None:
    try:
        from_id = message.from_user.id
        if message.caption is None:
            msg = await message.copy_to(chat_id=admin_id, caption=f"🙎‍♂️{htmlescape(message.from_user.full_name)}, {f'Username: @{message.from_user.username}\n' if message.from_user.username else ''}\nId: <code>{from_id}</code>\n\n", reply_markup=get_keyboard(from_id, message.message_id))
        else:
            msg = await message.copy_to(chat_id=admin_id, caption=f"🙎‍♂️{htmlescape(message.from_user.full_name)}, {f'Username: @{message.from_user.username}\n' if message.from_user.username else ''}\nId: <code>{from_id}</code>\n\n{htmlescape(message.caption)}", reply_markup=get_keyboard(from_id, message.message_id))
        await db.users.update_one({'_id': message.from_user.id}, {'$push': {'ids': msg.message_id}})
    except TypeError:
        await message.answer("Sorry, we don't work with this type of message")

@router.message(F.text)
async def send_just_text_handler(message: Message, bot: Bot, db: ADB) -> None:
    msg = await bot.send_message(chat_id=admin_id, text=f"🙎‍♂️{htmlescape(message.from_user.full_name)}, {f'Username: @{message.from_user.username}\n' if message.from_user.username else ''}Id: <code>{message.from_user.id}</code>\n\n{htmlescape(message.text)}", reply_markup=get_keyboard(message.from_user.id, message.message_id))
    await db.users.update_one({'_id': message.from_user.id}, {'$push': {'ids': msg.message_id}})



@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, db: ADB):
    await db.users.update_one({'_id': event.from_user.id}, {'$set': {'is_active': False}})



@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, db: ADB):
    await db.users.update_one({'_id': event.from_user.id}, {'$set': {'is_active': True}})
