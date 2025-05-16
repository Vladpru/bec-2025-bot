from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

router = Router()

@router.message(F.text == "Реєстрація")
async def start_registration(message: types.Message):
    print(f"Received: {message.text}")
    if not is_correct_text(message.text):
        await message.answer(
            "Error!"
        )
        return
    await message.answer("Enter name: ",
                         parse_mode="HTML",
                         reply_markup=ReplyKeyboardRemove())
    