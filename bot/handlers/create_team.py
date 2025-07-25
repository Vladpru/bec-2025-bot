from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.team import get_have_team_kb, get_back_kb
from bot.keyboards.no_team import get_category_kb, get_not_team_kb
from bot.utils.database import save_team_data, update_user_team, get_team_by_name
from uuid import uuid4

router = Router()

class CreateTeam(StatesGroup):
    team_name = State()
    category = State()
    technologies = State()
    password = State()
    check_password = State()

@router.message(F.text == "⬅️ Назад")
async def process_back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Ви повернулися до головного меню.", reply_markup=get_not_team_kb())

@router.message(F.text == "Створити команду")
async def create_team(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Введи назву команди:", reply_markup=get_back_kb())
    await state.set_state(CreateTeam.team_name)

@router.message(CreateTeam.team_name)
async def process_team_name(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await process_back(message, state)
        return
    # Перевірка унікальності імені команди
    existing_team = await get_team_by_name(message.text)
    if existing_team:
        await message.answer("Команда з такою назвою вже існує. Введіть іншу назву або натисніть 'Назад'.", reply_markup=get_back_kb())
        return
    await state.update_data(team_name=message.text)
    await message.answer("Оберіть категорію:", reply_markup=get_category_kb(with_back=True))
    await state.set_state(CreateTeam.category)

@router.message(CreateTeam.category)
async def process_category(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await process_back(message, state)
        return
    valid_categories = ["Team Design", "Innovative Design"]
    if message.text not in valid_categories:
        await message.answer("Будь ласка, оберіть одну з категорій: Team Design або Innovative Design.", reply_markup=get_category_kb(with_back=True))
        return
    await state.update_data(category=message.text)
    await message.answer("Введи технології, з якими працює команда (через кому):", reply_markup=get_back_kb())
    await state.set_state(CreateTeam.technologies)

@router.message(CreateTeam.technologies)
async def process_technologies(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await process_back(message, state)
        return
    await state.update_data(technologies=message.text)
    await message.answer("Введи пароль для команди:", reply_markup=get_back_kb())
    await state.set_state(CreateTeam.password)

@router.message(CreateTeam.password)
async def process_team_password(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await process_back(message, state)
        return
    await state.update_data(password=message.text)
    await message.answer("Підтверди пароль для команди:", reply_markup=get_back_kb())
    await state.set_state(CreateTeam.check_password)

@router.message(CreateTeam.check_password)
async def process_team_check_password(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await process_back(message, state)
        return
    data = await state.get_data()
    if data["password"] != message.text:
        await message.answer("Неправильний пароль для команди. Спробуй ще раз:", reply_markup=get_back_kb())
        await state.set_state(CreateTeam.check_password)
        return

    team_id = str(uuid4())
    await save_team_data(
        team_id=team_id,
        team_name=data["team_name"],
        category=data["category"],
        password=data["password"],
        technologies=data["technologies"],
        members_telegram_ids=[message.from_user.id]
    )

    await message.answer(
        f"Команда '{data['team_name']}' створена!\nКатегорія: {data['category']}\nТехнології: {data['technologies']}",
        reply_markup=get_have_team_kb()
    )
    await update_user_team(user_id=message.from_user.id, team_id=team_id)

    await state.clear()
