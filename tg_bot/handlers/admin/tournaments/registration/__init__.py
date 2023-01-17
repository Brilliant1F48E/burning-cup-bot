from aiogram import Dispatcher

from .menu_registration import register_handlers_menu_registration
from .cancel_registration import register_handlers_cancel_registration
from .open_registration import register_handlers_start_registration
from .view_registration import register_handlers_view_registration


def register_handlers_registration(dp: Dispatcher):
    register_handlers_menu_registration(dp)
    register_handlers_cancel_registration(dp)
    register_handlers_start_registration(dp)
    register_handlers_view_registration(dp)
