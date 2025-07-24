from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_not_team_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Створити команду")], 
            [KeyboardButton(text="Знайти команду")], 
            [KeyboardButton(text="Лінка на групу для пошуку команди")],
            [KeyboardButton(text="CV")],
        ],
        resize_keyboard=True
    )

def get_category_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Team Design")], 
            [KeyboardButton(text="Innovative Design")],
        ],
        resize_keyboard=True
    )