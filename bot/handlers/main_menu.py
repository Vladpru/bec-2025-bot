from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re
from bot.keyboards.team import get_have_team_kb
from bot.keyboards.no_team import get_not_team_kb
from bot.utils.database import get_user

router = Router()

@router.message(F.text=="Лінка на групу для пошуку команди")
async def get_link(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        await message.answer("Ось лінка: ----", parse_mode="HTML")
       
    except Exception as e:
        await message.answer("An error occurred")
        await print(f"An error occurred: {str(e)}")
        await state.clear()

@router.message(F.text=="Моя команда")
async def get_team(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        user_id = message.from_user.id
        if not user_id:
            await message.answer("⚠️ Не вдалося знайти твої дані. Спробуй ще раз пізніше.")
            return
        
        user_data = await get_user(user_id)
        if not user_data:
            await message.answer("⚠️ Не вдалося знайти твої дані. Спробуй ще раз пізніше.")
            return
        
        
        team_status = user_data.get('team','-')
        if team_status != '-':
            await message.answer(
                ' В тебе вже є команда! ',
                parse_mode="HTML",
                reply_markup=get_have_team_kb()
            )
        else:
            await message.answer(
                ' В тебе ще нема команди! ',
                parse_mode="HTML",
                reply_markup=get_not_team_kb()
            )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await message.answer("An error occurred")
        await state.clear()

@router.message(F.text=="Більше інфи")
async def get_more_info(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        await message.answer("Більше інфииииии аоаоаоааоаа", parse_mode="HTML")

        current_state = await state.get_state()
        print(f"State after setting: {current_state}")
    except Exception as e:
        await message.answer("An error occurred")
        await print(f"An error occurred: {str(e)}")
        await state.clear()
