from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from abc import ABC, abstractmethod

from tg_bot.types.request import RequestStatus


class RequestKb(ABC):
    __ib_get_by_status_wait: InlineKeyboardButton
    __ib_get_by_status_success: InlineKeyboardButton
    __ib_get_by_status_process: InlineKeyboardButton
    __ib_get_by_status_cancel: InlineKeyboardButton
    __ib_get_by_status_fail: InlineKeyboardButton

    __ib_moderation: InlineKeyboardButton
    __ib_no_moderation: InlineKeyboardButton
    __ib_moderation_postpone: InlineKeyboardButton

    __ib_confirm_set_yes: InlineKeyboardButton
    __ib_confirm_set_no: InlineKeyboardButton

    @abstractmethod
    async def get_all(self, requests) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def get_by(self) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def view(self, request_type: str, status: RequestStatus, request_id: str) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def moderation(self) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def set(self) -> InlineKeyboardMarkup:
        pass
