from aiogram.dispatcher.filters.state import StatesGroup, State


class SetTeamName(StatesGroup):
    ENTER_NEW_TEAM_NAME = State()


class SetTeamPhoto(StatesGroup):
    SEND_NEW_TEAM_PHOTO = State()
