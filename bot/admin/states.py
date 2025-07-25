from aiogram.fsm.state import StatesGroup, State


class AdminStates:
    waiting_for_team_selection = "waiting_for_team_selection"

class BroadcastStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_speed_dating_message = State()  # НОВИЙ

class StageSelectionStates(StatesGroup):
    waiting_for_stage = State()

class TeamMessageState(StatesGroup):
    waiting_for_message = State()