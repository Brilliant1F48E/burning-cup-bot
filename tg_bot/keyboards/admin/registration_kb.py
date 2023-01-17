from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.types.request import RequestStatus
from tg_bot.types.registration import RegistrationStatus
from tg_bot.models.db_model.models import Registration


class RegistrationKb:
    ib_registrations: InlineKeyboardButton = InlineKeyboardButton("Регистрации", callback_data="registrations")

    # Requests
    ib_requests: InlineKeyboardButton = InlineKeyboardButton("Запросы", callback_data="requests")

    ib_view_all_requests: InlineKeyboardButton = InlineKeyboardButton("Все", callback_data="view_all_requests")
    ib_view_selection_requests: InlineKeyboardButton = InlineKeyboardButton("Выборка", callback_data="view_selection_requests")

    # Manager
    ib_manager_registration: InlineKeyboardButton = InlineKeyboardButton("Управление", callback_data="manager_registrations")

    # Manager actions
    ib_set_registration: InlineKeyboardButton = InlineKeyboardButton("Изменить", callback_data="set_registrations")
    ib_cancel_registration: InlineKeyboardButton = InlineKeyboardButton("Отменить", callback_data="cancel_registrations")
    ib_view_registration: InlineKeyboardButton = InlineKeyboardButton("Статистика", callback_data="view_registrations")

    async def get_registration_menu_ikb(self, registration: Registration) -> InlineKeyboardMarkup:
        registration_ikb = InlineKeyboardMarkup(row_width=1)

        if not registration or registration.registration_status == RegistrationStatus.CANCEL:
            registration_ikb.add(self.ib_set_registration)
        elif registration.registration_status == RegistrationStatus.OPEN:
            registration_ikb.add(self.ib_cancel_registration).add(self.ib_view_registration).add(self.ib_requests)
        elif registration.registration_status == RegistrationStatus.CLOSE:
            registration_ikb.add(self.ib_view_registration)

        registration_ikb.add(self.ib_back_to_tournament)

        return registration_ikb