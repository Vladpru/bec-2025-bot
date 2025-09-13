from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Розсилка")],
            [KeyboardButton(text="Статистика")],
        ],
        resize_keyboard=True
    )
