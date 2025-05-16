from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(F.text.lower().strip() == "реєстрація")
async def start_registration(message: types.Message):
    print(f"Received: {message.text}")
    questions = [
        "Як вас звати?",
        "Виберіть вік: 18-25 / 26-35 / 36+",
        "Опишіть свій досвід (якщо є):"
    ]
    for q in questions:
        await message.answer("Початок реєстрації. Відповідайте на питання:\n1. " + q)