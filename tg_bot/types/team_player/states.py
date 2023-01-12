from aiogram.dispatcher.filters.state import StatesGroup, State


class SetDiscord(StatesGroup):
    ENTER_NEW_DISCORD = State()


class SetFastcup(StatesGroup):
    ENTER_NEW_FASTCUP = State()


class SetUsername(StatesGroup):
    ENTER_NEW_USERNAME = State()



