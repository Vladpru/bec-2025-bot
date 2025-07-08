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

@router.message(F.text == "Реєстрація")
async def start_registration(message: types.Message, state: FSMContext):
    try:
        print(f"Received: {message.text}")
        await message.answer(
            "Введи своє ім’я та прізвище:",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Registration.name)
        print(f"State set to: Registration.name")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await message.answer("⚠️ Виникла помилка. Спробуй пізніше.")
        await state.clear()

@router.message(Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    print(f"Processing name: {message.text}")
    try:
        name = message.text.strip()
        if not is_correct_text(name):
            await message.answer("🚫 Некоректне ім’я. Спробуй ще раз.")
            return

        parts = name.split()
        if len(parts) != 2:
            await message.answer("📝 Введи Ім’я та Прізвище (через пробіл).")
            return

        await state.update_data(name=name)
        await message.answer(
            f"Привіт, <b>{parts[0]}</b>! Обери свій університет:",
            reply_markup=get_uni_kb(),
            parse_mode="HTML"
        )
        await state.set_state(Registration.uni)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await message.answer("⚠️ Сталася помилка.")
        await state.clear()

@router.message(Registration.uni)
async def finish(message: types.Message, state: FSMContext):
    print("Finishing registration")
    try:
        if message.text in ["Більше інфи", "Лінка на групу для пошуку тімки", "Моя команда"]:
            await message.answer("⬆️ Спершу заверши реєстрацію, а тоді можна буде перейти до меню.")
            return

        data = await state.get_data()
        name = data.get("name", "користувач")

        await message.answer(
            f"✅ Тебе зареєстровано, <b>{name}</b>!\nОсь головне меню 👇",
            parse_mode="HTML",
            reply_markup=main_menu_kb()
        )
        await state.clear()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await message.answer("⚠️ Щось пішло не так...")
        await state.clear()
