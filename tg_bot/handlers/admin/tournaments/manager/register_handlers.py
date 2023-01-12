from aiogram import Dispatcher

from .menu_management import register_handlers_menu_management
from tg_bot.handlers.admin.tournaments.days import register_handlers_menu_days
from tg_bot.handlers.admin.tournaments.games import register_handlers_games
from tg_bot.handlers.admin.tournaments.match import register_handlers_match


def register_handlers_management(dp: Dispatcher):
    register_handlers_menu_management(dp)
    register_handlers_menu_days(dp)
    register_handlers_games(dp)
    register_handlers_match(dp)
