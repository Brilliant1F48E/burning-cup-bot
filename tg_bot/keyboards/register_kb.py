from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from tg_bot.keyboards.base_kb import BaseKb

from tg_bot.types.member.type import MemberType


class RegisterKb(BaseKb):
    ib_register = InlineKeyboardButton("Регистрация", callback_data="create_player")

    b_menu = '💠 Меню'

    ib_choice_member_type_student = InlineKeyboardButton('Студент',
                                                              callback_data=f'choice_member_type?member_type={MemberType.STUDENT}')
    ib_choice_member_type_schoolboy = InlineKeyboardButton('Школьник',
                                                                callback_data=f'choice_member_type?member_type={MemberType.SCHOOLBOY}')

    ib_choice_educational_institution = InlineKeyboardButton('СПК',
                                                                  callback_data=f'choice_educational_institution?educational_institution=СПК')

    async def get_register_ikb(self):
        register_ikb = InlineKeyboardMarkup(row_width=1)

        register_ikb.add(self.ib_register)

        return register_ikb

    async def get_start_kb(self) -> ReplyKeyboardMarkup:
        kb_start = ReplyKeyboardMarkup(resize_keyboard=True)

        kb_start.add(self.b_menu)

        return kb_start

    async def get_choice_institution_ikb(self, institutions: list) -> InlineKeyboardMarkup:
        institution_ikb = InlineKeyboardMarkup(row_width=3)

        for institution in institutions:
            institution_ikb.add(InlineKeyboardButton(institution.name, callback_data=f'choice_institution?id={institution.id}&type={institution.institution_type}'))

        return institution_ikb

    async def get_choice_member_type_ikb(self) -> InlineKeyboardMarkup:
        ikb_choice_member_type = InlineKeyboardMarkup(row_width=2)

        ikb_choice_member_type.add(self.ib_choice_member_type_student).insert(self.ib_choice_member_type_schoolboy)

        return ikb_choice_member_type

    async def get_repeated_request_member_ikb(self) -> InlineKeyboardMarkup:
        repeated_request_member_ikb = InlineKeyboardMarkup(row_width=1)

        ib_repeated_request_member = InlineKeyboardButton('Подать повторно', callback_data='repeated_request_member')

        repeated_request_member_ikb.add(ib_repeated_request_member)

        return repeated_request_member_ikb