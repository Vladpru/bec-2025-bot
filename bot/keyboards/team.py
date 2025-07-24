from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_have_team_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Створити/знайти команду")], 
            [KeyboardButton(text="Тестове завдання")], 
            [KeyboardButton(text="змінити стек технологій")], 
            [KeyboardButton(text="CV")],
        ],
        resize_keyboard=True
    )
