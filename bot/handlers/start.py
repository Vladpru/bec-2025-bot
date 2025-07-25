from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from bot.keyboards.team import get_have_team_kb
from bot.keyboards.no_team import get_not_team_kb
from bot.keyboards.registration import get_reg_kb
from bot.utils.database import get_user, is_user_in_team, is_user_registered   

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if not await is_user_registered(user_id):
        await message.answer(
            "Привіт!👋\n\n"
            "Я – бот <b>BEC</b> й допоможу тобі дізнатися про всі наші активності\n\n"
            "Щоб розпочати наше знайомство натисни <b>«Старт 🚀»</b>!",
            reply_markup=get_reg_kb(),
            parse_mode="HTML"
        )
        return

    in_team = await is_user_in_team(user_id)
    reply = get_have_team_kb() if in_team else get_not_team_kb()
    await message.answer(
        "Знову привіт! 👋 Ви вже зареєстровані.",
        reply_markup=reply
    )
