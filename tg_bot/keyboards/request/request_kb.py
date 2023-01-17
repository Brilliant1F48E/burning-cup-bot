from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from abc import ABC, abstractmethod

from tg_bot.types.request import RequestStatus


class RequestKb(ABC):
    __method_get_all: str = "get_all"
    __method_get_by: str = "get_by"
    __method_set_status: str = "set_status"
    __method_choice_status: str = "choice_status"
    __method_moderation: str = "moderation"
    __method_view: str = "view"

    __ib_get_by_status_wait: InlineKeyboardButton
    __ib_get_by_status_success: InlineKeyboardButton
    __ib_get_by_status_process: InlineKeyboardButton
    __ib_get_by_status_cancel: InlineKeyboardButton
    __ib_get_by_status_fail: InlineKeyboardButton

    @abstractmethod
    async def get_all(self, requests) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def get_by(self) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def view(self, status: RequestStatus, request_id: str) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def moderation(self) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def set(self) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def get_menu(self) -> InlineKeyboardMarkup:
        pass
