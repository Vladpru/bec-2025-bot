from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Keyboard
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Реєстрація")],
            [KeyboardButton(text="Більше про івент")]
        ],
        resize_keyboard=True
    )
    await message.answer("Шо ти галава нажимай далі, на кнопки🙄", reply_markup=keyboard)