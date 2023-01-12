from aiogram.dispatcher.filters.state import StatesGroup, State


class AddDay(StatesGroup):
    CHOICE_GAME = State()
    ENTER_STREAM_LINK = State()
