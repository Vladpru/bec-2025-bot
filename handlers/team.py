from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.team import get_have_team_kb
from keyboards.no_team import get_not_team_kb

router = Router()

class TeamReg(StatesGroup):
    name = State()


@router.message(F.text == "...")
async def start_registration(message: types.Message, state: FSMContext):
    try:
        print(f"Received: {message.text}")
        await message.answer("Enter name:", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Registration.name)

        current_state = await state.get_state()
        print(f"State after setting: {current_state}")
    except Exception as e:
        await message.answer("An error occurred")
        await print(f"An error occurred: {str(e)}")
        await state.clear()
