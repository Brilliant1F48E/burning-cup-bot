from aiogram.dispatcher.filters.state import StatesGroup, State


class AddTournament(StatesGroup):
    ENTER_NAME_TOURNAMENT = State()
    ENTER_LIMIT_TEAMS = State()
    ENTER_DATE_ANONS = State()
