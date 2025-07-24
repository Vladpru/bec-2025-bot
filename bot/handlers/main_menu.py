from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re
from bot.keyboards.team import get_have_team_kb
from bot.keyboards.no_team import get_not_team_kb


router = Router()

@router.message(F.text== "Лінка на групу для пошуку тімки")
async def get_link(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        await message.answer("Ось лінка: ----", parse_mode="HTML")
       
    except Exception as e:
        await message.answer("An error occurred")
        await print(f"An error occurred: {str(e)}")
        await state.clear()

@router.message(F.text== "Моя команда")
async def get_team(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        if 'have team':
            await message.answer(
                "",
                parse_mode="HTML",
                reply_markup=get_have_team_kb()
            )
        await message.answer(
            "",
            parse_mode="HTML",
            reply_markup=get_not_team_kb()
        )
        current_state = await state.get_state()
        print(f"State after setting: {current_state}")
    except Exception as e:
        await message.answer("An error occurred")
        await print(f"An error occurred: {str(e)}")
        await state.clear()

@router.message(F.text== "Більше інфи")
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
