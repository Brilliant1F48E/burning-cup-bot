from aiogram.dispatcher.filters.state import StatesGroup, State


class ModerationRequestEnterComment(StatesGroup):
    ENTER_COMMENT = State()
