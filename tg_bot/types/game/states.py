from aiogram.dispatcher.filters.state import StatesGroup, State


class AddGame(StatesGroup):
    ENTER_DATE_START = State()
