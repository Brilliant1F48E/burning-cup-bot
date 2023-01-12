from aiogram import Dispatcher

from .teams import register_handlers_teams
from .requests import register_handlers_menu_requests
from .players import register_handlers_player


def register_handlers_manager(dp: Dispatcher):
    register_handlers_teams(dp)
    register_handlers_menu_requests(dp)
    register_handlers_player(dp)
