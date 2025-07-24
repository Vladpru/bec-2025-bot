from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Реєстрація")],
            [KeyboardButton(text="Більше про івент")]
        ],
        resize_keyboard=True
    )
    if True:
        await message.answer(
            text=("Привіт!👋\n\n"
                "Я – бот <b>BEC</b> й допоможу тобі дізнатися про всі наші активності\n\n"
                "Щоб розпочати наше знайомство натисни <b>«Старт 🚀»</b>!"), 
            reply_markup=keyboard, 
            parse_mode="HTML"
        )
    else:
        pass

