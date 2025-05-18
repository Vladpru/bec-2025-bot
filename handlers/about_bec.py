from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import re

router = Router()

@router.message(F.text.lower().strip() == "більше про івент")
async def show_event_info(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        await message.answer("Інфа про ВВВЕЕЕССС")
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Реєстрація")],
            ],
            resize_keyboard=True
        )
        await message.answer("А тепер перейдемо до реєстрації", reply_markup=keyboard)
    except Exception as e:
        await message.answer("An error occurred")
        await print(f"An error occurred: {str(e)}")
