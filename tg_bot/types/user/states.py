from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateRequestMember(StatesGroup):
    CHOICE_MEMBER_TYPE = State()
    CHOICE_EDUCATIONAL_INSTITUTION = State()
    ENTER_FULLNAME = State()
    ENTER_GROUP = State()
    SEND_DOCUMENT_PHOTO = State()