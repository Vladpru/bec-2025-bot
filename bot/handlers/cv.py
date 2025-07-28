from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.keyboards.cv_keyboard import get_cv_kb
from bot.handlers.registration import is_correct_text
from bot.utils.cv_db import update_cv_file_path, add_cv
from bot.keyboards.team import get_have_team_kb

router = Router()

@router.message(F.text == "CV")
async def cv_start(message: types.Message, state: FSMContext):
    await message.answer(
        "У цьому меню ви зможете відправити CV! Воно може зацікавити роботодавців, що може змінити ваше життя =)",
        parse_mode="HTML",
        reply_markup=get_cv_kb()
    )

@router.message(F.text == "📤 Надіслати готове CV")
async def cv_send(message: types.Message, state: FSMContext):   
    if not is_correct_text(message.text):
        await message.answer(
            "⚠️ Схоже, що дані введені неправильно. Будь ласка, спробуй ще раз!"
        )
        return
    await message.answer(
        "Будь ласка, надішліть своє CV у форматі PDF або DOCX. "
        "Переконайтеся, що файл не містить особистої інформації, "
        "такої як номер телефону чи адреса електронної пошти.",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.document)
async def handle_cv_file(message: types.Message):
    if message.document.mime_type != "application/pdf":
        await message.answer("❗ Упс, схоже, що формат файлу неправильний. Спробуй ще раз, використовуючи PDF формат.")
        return

    max_file_size = 10 * 1024 * 1024  # 10 МБ
    if message.document.file_size > max_file_size:
        await message.answer("Упс. Схоже, файл завеликий. Його розмір має бути не більшим за 10 МБ.")
        return
    
    try:
        file_id = message.document.file_id
        file = await message.bot.get_file(file_id)
        if file.file_path is None or not file.file_path:
            await message.answer("❗ Помилка: не вдалося отримати шлях до файлу. Спробуй ще раз.")
            return
        print(f"File ID: {file_id}, File Path: {file.file_path}")
        await message.bot.download_file(file.file_path, timeout=30)
    except Exception as e:
        await message.answer("🕒 Файл завантажується дуже довго… Перевір розмір і спробуй ще раз!")
        return
    user_id = message.from_user.id
    await update_cv_file_path(message.from_user.id, file_id)
    await add_cv(user_id=user_id, cv_file_id=file_id)
    await message.answer("✅ CV завантажено! 🎉", reply_markup=get_have_team_kb())

















@router.message(F.text == "Створити CV")
async def cv_create(message: types.Message, state: FSMContext):
    if not is_correct_text(message.text):
        await message.answer(
            "⚠️ Схоже, що дані введені неправильно. Будь ласка, спробуй ще раз!"
        )
        return
    await message.answer(
        "Щоб створити CV, будь ласка, надішліть мені своє ім'я та прізвище.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state("cv_create")
