from aiogram import Dispatcher

from .ban import register_handlers_ban
from .unban import register_handlers_unban
from .menu import register_handlers_menu
from .view import register_handlers_view


def register_handlers_teams(dp: Dispatcher):
    register_handlers_unban(dp)
    register_handlers_ban(dp)
    register_handlers_menu(dp)
    register_handlers_view(dp)
