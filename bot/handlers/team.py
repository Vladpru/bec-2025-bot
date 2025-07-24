from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from bot.utils.database import get_team, exit_team
from bot.keyboards.registration import main_menu_kb

router = Router()

@router.message(F.text == "Інфа про команду")
async def start_registration(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    team = await get_team(user_id)
    await message.answer(
        f"Команда '{team['team_name']}' створена!\nКатегорія: {team['category']}\nТехнології: {team['technologies']}",
        parse_mode="HTML",
    )

@router.message(F.text == "вийти з команди")
async def start_registration(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await exit_team(user_id):
        await message.answer(
            "Успішно вийшов",
            parse_mode="HTML",
            reply_markup=main_menu_kb()
        )
    else:
        await message.answer(
            "Якась помилка",
            parse_mode="HTML"
        )
        
@router.message(F.text == "Тестове завдання")
async def start_registration(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await exit_team(user_id):
        await message.answer(
            "Успішно вийшов",
            parse_mode="HTML",
            reply_markup=main_menu_kb()
        )
    else:
        await message.answer(
            "Якась помилка",
            parse_mode="HTML"
        )

