import asyncio
import os
import zipfile

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
    Message,
    CallbackQuery
)
from bson import ObjectId
from motor.core import AgnosticDatabase

from bot.admin.data import *
from bot.admin.services import *
from bot.admin.states import (
    StageSelectionStates,
    BroadcastStates,
    TeamMessageState
)
from bot.keyboards.admin_keyboard import (
    get_main_admin_keyboard,
    get_stage_selection_keyboard,
    get_broadcast_inline_keyboard,
    get_team_actions_inline_keyboard
)
from bot.utils.keyboards.start_keyboard import get_start_keyboard, get_user_team_info
from config_reader import ADMIN_PASSWORD

router = Router()


@router.message(F.text == str(ADMIN_PASSWORD))
async def open_admin_panel(message: types.Message):
    await message.answer(ADMIN_WELCOME, reply_markup=get_main_admin_keyboard())


@router.message(F.text == "Вийти з адмінки")
async def handle_admin_exit(message: Message, db: AgnosticDatabase):
    if not await is_user_admin(db, message.from_user.id):
        return
    is_registered = await is_user_registered(db, message.from_user.username)
    test_approved, event_approved = await get_user_team_info(db, message.from_user.id)
    stage = await get_current_stage(db)
    await message.answer(ADMIN_EXIT,
                         reply_markup=get_start_keyboard(stage, is_registered, test_approved, event_approved))


@router.message(F.text == "Переключити секцію")
async def handle_toggle_section(message: Message, state: FSMContext, db: AgnosticDatabase):
    if not await is_user_admin(db, message.from_user.id):
        return
    await message.answer(STAGE_SELECTION_PROMPT, reply_markup=get_stage_selection_keyboard())
    await state.set_state(StageSelectionStates.waiting_for_stage)
