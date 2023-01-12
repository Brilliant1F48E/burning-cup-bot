from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from abc import ABC, abstractmethod


class RequestKb(ABC):
    __ib_get_by_status_wait: InlineKeyboardButton
    __ib_get_by_status_success: InlineKeyboardButton
    __ib_get_by_status_process: InlineKeyboardButton
    __ib_get_by_status_cancel: InlineKeyboardButton
    __ib_get_by_status_fail: InlineKeyboardButton

    __ib_verif: InlineKeyboardButton
    __ib_no_verif: InlineKeyboardButton
    __ib_verif_postpone: InlineKeyboardButton

    __ib_confirm_set_yes: InlineKeyboardButton
    __ib_confirm_set_no: InlineKeyboardButton

    @abstractmethod
    async def get_all(self) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def get_by(self) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def view(self) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def verif(self) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def set(self) -> InlineKeyboardMarkup:
        pass
