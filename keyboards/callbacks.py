from aiogram import types


def get_keyboard(id: int, msgid: int):
    buttons = [
        [
            types.InlineKeyboardButton(text="🚫", callback_data=f"ban_{id}"),
            types.InlineKeyboardButton(text="🗑", callback_data=f"del"),
            types.InlineKeyboardButton(text="↩️", callback_data=f"reply_{id}_{msgid}"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard