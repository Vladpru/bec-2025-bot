from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from bot.keyboards.team import get_have_team_kb
from bot.utils.database import get_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    if user:
        await message.answer(
            text="Знову привіт! 👋 Ви вже зареєстровані.",
            reply_markup=get_have_team_kb()
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Реєстрація")],
                [KeyboardButton(text="Більше про івент")]
            ],
            resize_keyboard=True
        )
        await message.answer(
            text=("Привіт!👋\n\n"
                  "Я – бот <b>BEC</b> й допоможу тобі дізнатися про всі наші активності\n\n"
                  "Щоб розпочати наше знайомство натисни <b>«Старт 🚀»</b>!"),
            reply_markup=keyboard,
            parse_mode="HTML"
        )
