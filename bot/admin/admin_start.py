import os
from aiogram import Router, types, F
from bot.admin.admin_keyboard import get_admin_kb
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramForbiddenError
from bot.utils.database import get_all_active_users, get_all_user_ids

load_dotenv()
router = Router()

@router.message(F.text == os.getenv("ADMIN_START"))
async def admin_start(message: types.Message):
    admin_id = int(os.getenv("ADMIN_ID"))
    if message.from_user.id == admin_id:
        await message.answer(
            "Привіт, ADMIN!",
            reply_markup=get_admin_kb(),
            parse_mode="HTML"
        )
    return

class SpamStates(StatesGroup):
  waiting_for_message = State()

@router.message(F.text == "Розсилка")
async def start_spam(message: types.Message, state: FSMContext):
  admin_id = int(os.getenv("ADMIN_ID"))
  if message.from_user.id == admin_id:
    await message.answer("Введіть текст розсилки або 'Назад' для відміни:")
    await state.set_state(SpamStates.waiting_for_message)

@router.message(SpamStates.waiting_for_message)
async def send_spam(message: types.Message, state: FSMContext, bot):
  admin_id = int(os.getenv("ADMIN_ID"))
  if message.from_user.id != admin_id:
    return

  if message.text.lower() == "назад":
    await message.answer("Розсилку скасовано.", reply_markup=get_admin_kb())
    await state.clear()
    return

  user_ids = await get_all_user_ids() 
  sent_count = 0
  failed_count = 0

  for user_id in user_ids:
    try:
        await bot.send_message(user_id, message.text)
        sent_count += 1
    except TelegramForbiddenError:
        # Користувач заблокував бота, це нормально
        failed_count += 1
    except Exception as e:
        # Інші помилки (наприклад, ID не знайдено, помилка API)
        print(f"Не вдалося надіслати повідомлення користувачу {user_id}: {e}")
        failed_count += 1
  
  # Надаємо адміну більш детальну інформацію
  await message.answer(
      f"Розсилку завершено.\n\n✅ Надіслано: {sent_count}\n❌ Не вдалося надіслати: {failed_count}",
      reply_markup=get_admin_kb()
  )
  await state.clear()


@router.message(F.text == "Статистика")
async def admin_back(message: types.Message):
    admin_id = int(os.getenv("ADMIN_ID"))
    if message.from_user.id == admin_id:
        await message.answer(
            "Ви повернулись назад до меню",  
            reply_markup=get_admin_kb()
        )
    return
