from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re
from keyboards.registration import get_uni_kb, main_menu_kb

router = Router()

class Registration(StatesGroup):
    name = State()
    uni = State()

def is_correct_text(text):
    contains_letters = re.search(r'[a-zA-Zа-яА-ЯіІїЇєЄґҐ]', text)
    only_symbols = re.fullmatch(r'[\W_]+', text)
    return bool(contains_letters) and not only_symbols

@router.message(F.text== "Реєстрація")
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

@router.message(Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    print(f"Processing name: {message.text}")
    try:
        name = message.text.strip()
        if not is_correct_text(name):
            await message.answer("Not accepted")
            return

        await message.answer(f"Hello: {name}, now choose university:",
                            reply_markup=get_uni_kb(),
                            parse_mode="HTML" 
                            )
        await state.set_state(Registration.uni)

    except Exception as e:
        await message.answer("An error occurred")
        await print(f"An error occurred: {str(e)}")
        await state.clear()
    
@router.message(Registration.uni)
async def finish(message: types.Message, state: FSMContext):
    print("Finishing")
    try:
        if not is_correct_text(message.text):
            await message.answer("Not accepted")
            return
        await message.answer(
            "Тебе зареєстровано",
            
            parse_mode="HTML",
            reply_markup=main_menu_kb()
        )

    except Exception as e:
        await message.answer("An error occurred")
        await print(f"An error occurred: {str(e)}")
        await state.clear()
