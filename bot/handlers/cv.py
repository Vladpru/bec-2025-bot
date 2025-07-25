from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re
from bot.keyboards.registration import get_uni_kb, main_menu_kb, get_course_kb, where_kb, get_phone_kb
from bot.utils.database import save_user_data

router = Router()

@router.message(F.text == "CV")
async def cv_start(message: types.Message, state: FSMContext):
    await message.answer(
        "📝 Введи Ім’я та Прізвище (через пробіл).",
        parse_mode="HTML",
    )
