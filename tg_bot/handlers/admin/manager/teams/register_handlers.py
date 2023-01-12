from aiogram import Dispatcher

from .menu_teams import register_handlers_menu_teams


def register_handlers_teams(dp: Dispatcher):
    register_handlers_menu_teams(dp)
