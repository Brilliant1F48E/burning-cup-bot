from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .request_kb import RequestKb


class RequestTeamKb(RequestKb):
    __ib_get_by_status_wait: InlineKeyboardButton = InlineKeyboardButton(text="В ожидании", callback_data="get_by?type=team&by=status&value=wait")
    __ib_get_by_status_success: InlineKeyboardButton = InlineKeyboardButton(text="Успешно", callback_data="get_by?type=team&by=status&value=success")
    __ib_get_by_status_process: InlineKeyboardButton = InlineKeyboardButton(text="В процессе", callback_data="get_by?type=team&by=status&value=process")
    __ib_get_by_status_cancel: InlineKeyboardButton = InlineKeyboardButton(text="Отменено", callback_data="get_by?type=team&by=status&value=cancel")
    __ib_get_by_status_fail: InlineKeyboardButton = InlineKeyboardButton(text="Провал", callback_data="get_by?type=team&by=status&value=fail")

    __ib_verif_yes: InlineKeyboardButton = InlineKeyboardButton(text="Да", callback_data="verif?type=team&value=yes")
    __ib_verif_no: InlineKeyboardButton = InlineKeyboardButton(text="Нет", callback_data="verif?type=team&value=no")
    __ib_verif_postpone: InlineKeyboardButton = InlineKeyboardButton(text="Нет", callback_data="verif?type=team&value=postpone")

    __ib_confirm_set_yes: InlineKeyboardButton = InlineKeyboardButton(text="Да", callback_data="confirm_set?type=team&value=yes")
    __ib_confirm_set_no: InlineKeyboardButton = InlineKeyboardButton(text="Нет", callback_data="confirm_set?type=team&value=no")

    async def get_all(self) -> InlineKeyboardMarkup:
        pass

    async def get_by(self) -> InlineKeyboardMarkup:
        get_by_status_bs: list = [
            self.__ib_get_by_status_wait,
            self.__ib_get_by_status_success,
            self.__ib_get_by_status_process,
            self.__ib_get_by_status_cancel,
            self.__ib_get_by_status_fail
        ]

        ikb_get_by_status: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1).add(*get_by_status_bs)

        return ikb_get_by_status

    async def view(self) -> InlineKeyboardMarkup:
        pass

    async def verif(self) -> InlineKeyboardMarkup:
        pass

    async def set(self) -> InlineKeyboardMarkup:
        pass
