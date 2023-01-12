from aiogram.dispatcher.filters.state import StatesGroup, State


class ResponseRequestStudent(StatesGroup):
    ENTER_ANSWER = State()


class VerifRequestMember(StatesGroup):
    ENTER_RESPONSE = State()


class VerifRequestTeam(StatesGroup):
    ENTER_COMMENT_REQUEST_TEAM = State()
