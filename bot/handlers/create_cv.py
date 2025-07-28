from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards.cv_keyboard import get_cv_kb

router = Router()

@router.message(F.text == "CV")
async def cv_start(message: types.Message, state: FSMContext):
    await message.answer(
        "У цьому меню ви зможете відправити CV! Воно може зацікавити роботодавців, що може змінити ваше життя =)",
        parse_mode="HTML",
        reply_markup=get_cv_kb()
    )