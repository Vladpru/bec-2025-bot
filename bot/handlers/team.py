from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from bot.utils.database import get_team, exit_team, change_stack
from bot.keyboards.registration import main_menu_kb
from bot.handlers.registration import is_correct_text

router = Router()

class Team(StatesGroup):
    waiting_for_stack_input = State()

@router.message(F.text == "Інфа про команду")
async def info_team_handler(message: types.Message, state: FSMContext):
    from bot.utils.database import users_collection  # імпорт тут, щоб уникнути циклічних імпортів
    user_id = message.from_user.id
    team = await get_team(user_id)
    if team:
        # Отримати список ObjectId учасників
        member_ids = team.get("members", [])
        # Витягнути username кожного учасника
        usernames = []
        if member_ids:
            member = users_collection.find({"_id": {"$in": member_ids}})
            async for user in member:
                username = user.get("username")
                name = user.get("name")
                if username:
                    usernames.append(f"@{username}")
                elif name:
                    usernames.append(name)
                else:
                    usernames.append("Без імені")
        members_str = ", ".join(usernames) if usernames else "Немає учасників"
        await message.answer(
            f"Команда '{team['team_name']}'!\n\n"
            f"Категорія: {team['category']}\n\n"
            f"Технології: {team['technologies']}\n\n"
            f"Учасники: {members_str}",
            parse_mode="HTML",
        )
    else:
        await message.answer(
            "Технічна помилка, спробуйте пізніше",
            parse_mode="HTML"
        )

@router.message(F.text == "вийти з команди")
async def exit_team_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await exit_team(user_id):
        await message.answer(
            "Успішно вийшов",
            parse_mode="HTML",
            reply_markup=main_menu_kb()
        )
    else:
        await message.answer(
            "Технічна помилка, спробуйте пізніше",
            parse_mode="HTML"
        )
        
@router.message(F.text == "Тестове завдання")
async def test_task_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await exit_team(user_id):
        await message.answer(
            "Поки тестового нема",
            parse_mode="HTML",
        )
    else:
        await message.answer(
            "Технічна помилка, спробуйте пізніше",
            parse_mode="HTML"
        )

@router.message(F.text == "змінити стек технологій")
async def change_stack_handler(message: types.Message, state: FSMContext):
    try:
        await message.answer(
            "Введіть новий стек технологій (через кому):",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Team.waiting_for_stack_input)
    except Exception as e:
        await message.answer(
            "Виникла технічна помилка. Спробуйте ще раз пізніше.",
            parse_mode="HTML"
        )

@router.message(Team.waiting_for_stack_input)
async def process_stack_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    stack = message.text.strip()
    try:
        if not is_correct_text(stack):
            await message.answer(
                "Некоректно введено стек технологій. Спробуйте ще раз.",
                parse_mode="HTML"
            )
            return

        if await change_stack(user_id, stack):
            await message.answer(
                "Стек технологій успішно змінено",
                parse_mode="HTML",
                reply_markup=main_menu_kb()
            )
            await state.clear()
        else:
            await message.answer(
                "Некоректно введено стек технологій. Спробуйте ще раз.",
                parse_mode="HTML"
            )
    except Exception as e:
        await message.answer(
            "Виникла технічна помилка при зміні стеку. Спробуйте ще раз пізніше.",
            parse_mode="HTML"
        )