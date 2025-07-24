from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.team import get_have_team_kb
from keyboards.no_team import get_not_team_kb

router = Router()

