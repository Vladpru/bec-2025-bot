from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re
from bot.keyboards.registration import get_uni_kb, main_menu_kb, get_course_kb, where_kb, get_phone_kb
from bot.utils.database import save_user_data

router = Router()

class Registration(StatesGroup):
    name = State()
    course = State()
    university = State()
    speciality = State()
    where_know = State()
    custom_where_know = State()
    phone = State()

def is_correct_text(text):
    contains_letters = re.search(r'[a-zA-Zа-яА-ЯіІїЇєЄґҐ]', text)
    only_symbols = re.fullmatch(r'[\W_]+', text)
    return bool(contains_letters) and not only_symbols

@router.message(F.text == "Реєстрація")
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer(
        "📝 Введи Ім’я та Прізвище (через пробіл).",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Registration.name)

@router.message(Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not is_correct_text(name):
        await message.answer("🚫 Некоректне ім’я. Спробуй ще раз. Використовуй лише літери.")
        return

    parts = name.split()
    if len(parts) != 2:
        await message.answer("📝 Введи Ім’я та Прізвище (через пробіл). Формат: ім'я прізвище")
        return

    await state.update_data(name=name)
    await message.answer(
        f"Приємно познайомитись, <b>{parts[0]}</b>!\nОбери курс, на якому навчаєшся:",
        reply_markup=get_course_kb(),
        parse_mode="HTML"
    )
    await state.set_state(Registration.course)

@router.message(Registration.course)
async def ask_university_or_finish(message: types.Message, state: FSMContext):
    courses = ["🔹 1 курс", "🔹 2 курс", "🔹 3 курс", "🔹 4 курс", "🔹 Магістратура"]
    special_cases = ["🔹 Не навчаюсь", "🔹 Ще у школі/коледжі"]

    if message.text not in courses + special_cases:
        await message.answer("⚠️ Некоректні дані. Обери курс зі списку.")
        return

    await state.update_data(course=message.text)

    if message.text in special_cases:
        data = await state.get_data()
        await save_user_data(
            user_id=message.from_user.id,
            user_name=message.from_user.username,
            name=data["name"],
            course=data["course"],
            university="Не вказано",
            speciality="Не вказано",
            team='-'
        )
        await message.answer(
            "Чудово, тебе зареєстровано. 🎉\n\n"
            "Тепер ти можеш перейти до <b>меню</b> і дізнатися більше 🔎.",
            parse_mode="HTML",
            reply_markup=main_menu_kb()
        )
        await state.clear()
    else:
        await message.answer("Оберіть свій університет:", reply_markup=get_uni_kb())
        await state.set_state(Registration.university)

@router.message(Registration.university)
async def ask_speciality(message: types.Message, state: FSMContext):
    text = message.text.strip()
    unis = ["🎓 НУ “ЛП”", "🎓 ЛНУ ім. І. Франка", "🎓 УКУ", "🎓 ЛНАМ", "🎓 ЛДУБЖД", "🎓 ІТ Степ Університет", "🎓 Інший"]

    if message.text not in unis:
        await message.answer("⚠️ Некоректні дані. Обери університет зі списку.")
        return

    await state.update_data(university=text)
    await message.answer(
        "Яка твоя спеціальність?\nНапиши її у форматі: СШІ / ІГДГ / ІБІС …",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Registration.speciality)

@router.message(Registration.speciality)
async def ask_where(message: types.Message, state: FSMContext):
    if not is_correct_text(message.text):
        await message.answer("⚠️ Схоже, що дані введені неправильно. Спробуй ще раз. Використовуй лише літери.")
        return

    await state.update_data(speciality=message.text)
    data = await state.get_data()

    await message.answer(
        "✅ звідки ти знаєш нас?",
        parse_mode="HTML",
        reply_markup=where_kb()
    )
    await state.set_state(Registration.where_know)

@router.message(Registration.where_know)
async def ask_phone(message: types.Message, state: FSMContext):
    text = message.text.strip()

    where = ["інста", "тікток", "постер", "інше"]

    if message.text not in where:
        await message.answer("⚠️ Некоректні дані. Обери опцію зі списку.")
        return
    if text == "інше":
        await state.set_state(Registration.custom_where_know)
        await message.answer("Напиши звідки:", reply_markup=ReplyKeyboardRemove())
        return
        return

    await state.update_data(where_know=message.text)

    await message.answer(
        "Дай свій номер!!!!\nНатисни кнопку, щоб поділитися контактом.",
        reply_markup=get_phone_kb()
    )
    await state.set_state(Registration.phone)
# Handle custom 'where_know' input
@router.message(Registration.custom_where_know)
async def process_custom_where_know(message: types.Message, state: FSMContext):
    text = message.text.strip()
    if not is_correct_text(text):
        await message.answer("⚠️ Некоректна відповідь. Спробуй ще раз.")
        return

    await state.update_data(where_know=text)
    await message.answer(
        "Дай свій номер!!!!\nНатисни кнопку, щоб поділитися контактом.",
        reply_markup=get_phone_kb()
    )
    await state.set_state(Registration.phone)
    await state.set_state(Registration.phone)

@router.message(Registration.phone)
async def finish_registration(message: types.Message, state: FSMContext):
    # Перевірка, чи надіслано контакт
    if not message.contact or not message.contact.phone_number:
        await message.answer("⚠️ Будь ласка, надішли свій номер через кнопку 'Поділитися контактом', або у форматі +38-xxx-xxx-xxxx")
        return

    phone_number = message.contact.phone_number
    await state.update_data(phone=phone_number)

    data = await state.get_data()

    await save_user_data(
        user_id=message.from_user.id,
        user_name=message.from_user.username,
        name=data["name"],
        course=data["course"],
        university=data["university"],
        speciality=data["speciality"],
        where_know=data["where_know"],
        phone=phone_number,
        team='-'
    )

    await message.answer(
        "Чудово, тебе зареєстровано. 🎉\n\n"
        "Тепер ти можеш перейти до <b>меню</b> і дізнатися більше 🔎.",
        parse_mode="HTML",
        reply_markup=main_menu_kb()
    )
    await state.clear()
