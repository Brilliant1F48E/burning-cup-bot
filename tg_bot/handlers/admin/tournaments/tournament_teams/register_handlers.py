from aiogram import Dispatcher

from .menu_tournament_teams import register_handlers_menu_tournament_teams


def register_handlers_tournament_teams(dp: Dispatcher):
    register_handlers_menu_tournament_teams(dp)
