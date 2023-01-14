from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .request_kb import RequestKb
from tg_bot.types.request import RequestStatus


class RequestMemberKb(RequestKb):
    __ib_get_by_status_wait: InlineKeyboardButton = InlineKeyboardButton(text="В ожидании", callback_data="get_by?type=member&by=status&value=wait")
    __ib_get_by_status_success: InlineKeyboardButton = InlineKeyboardButton(text="Успешно", callback_data="get_by?type=member&by=status&value=success")
    __ib_get_by_status_process: InlineKeyboardButton = InlineKeyboardButton(text="В процессе", callback_data="get_by?type=member&by=status&value=process")
    __ib_get_by_status_cancel: InlineKeyboardButton = InlineKeyboardButton(text="Отменено", callback_data="get_by?type=member&by=status&value=cancel")
    __ib_get_by_status_fail: InlineKeyboardButton = InlineKeyboardButton(text="Провал", callback_data="get_by?type=member&by=status&value=fail")

    __ib_moderation_yes: InlineKeyboardButton = InlineKeyboardButton(text="Да", callback_data="verif?type=member&value=yes")
    __ib_moderation_no: InlineKeyboardButton = InlineKeyboardButton(text="Нет", callback_data="verif?type=member&value=no")
    __ib_moderation_postpone: InlineKeyboardButton = InlineKeyboardButton(text="Нет", callback_data="verif?type=member&value=postpone")

    __ib_confirm_set_yes: InlineKeyboardButton = InlineKeyboardButton(text="Да", callback_data="confirm_set?&value=yes")
    __ib_confirm_set_no: InlineKeyboardButton = InlineKeyboardButton(text="Нет", callback_data="confirm_set?&value=no")

    async def get_all(self) -> InlineKeyboardMarkup:
        pass

    async def get_by(self) -> InlineKeyboardMarkup:
        pass

    async def view(self, request_type: str, status: RequestStatus, request_id: str) -> InlineKeyboardMarkup:
        pass

    async def moderation(self) -> InlineKeyboardMarkup:
        pass

    async def set(self) -> InlineKeyboardMarkup:
        pass
