from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_uni_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎓 НУ “ЛП”"), KeyboardButton(text="🎓 ЛНУ ім. І. Франка")],
            [KeyboardButton(text="🎓 УКУ"), KeyboardButton(text="🎓 ЛНАМ")],
            [KeyboardButton(text="🎓 ЛДУБЖД"), KeyboardButton(text="🎓 ІТ Степ Університет")],
            [KeyboardButton(text="🎓 Інший")]
        ],
        resize_keyboard=True
    )

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Більше інфи")],
            [KeyboardButton(text="Лінка на групу для пошуку тімки")],
            [KeyboardButton(text="Моя команда")],
        ],
        resize_keyboard=True
    )

