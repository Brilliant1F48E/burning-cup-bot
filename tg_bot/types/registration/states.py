from aiogram.dispatcher.filters.state import StatesGroup, State


class StartRegistrationStates(StatesGroup):
    ENTER_START_DATE = State()
    ENTER_COUNT_TEAMS = State()
