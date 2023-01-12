from aiogram import Dispatcher

from .banned import register_handlers_banned
from .admin import register_handlers_admin
from .user import register_handlers_users


def register_all_handlers(dp: Dispatcher):
    register_handlers_banned(dp)
    register_handlers_admin(dp)
    register_handlers_users(dp)
