from aiogram.dispatcher.filters.state import StatesGroup, State


class JoinTeam(StatesGroup):
    ENTER_INVITE_CODE = State()


class CreateTeam(StatesGroup):
    ENTER_TEAM_NAME = State()
    SEND_TEAM_PHOTO = State()