from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_cv_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Створити CV")], 
            [KeyboardButton(text="📤 Надіслати готове CV")],
        ],
        resize_keyboard=True
    )
