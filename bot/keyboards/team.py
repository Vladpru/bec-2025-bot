from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_have_team_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Інфа про команду")], 
            [KeyboardButton(text="Тестове завдання")], 
            [KeyboardButton(text="змінити стек технологій")], 
            [KeyboardButton(text="CV")],
            [KeyboardButton(text="вийти з команди")],
        ],
        resize_keyboard=True
    )
