from aiogram import Dispatcher

from .add_game import register_handlers_add_game
from .update_result_game import register_handlers_update_result_game
from .games import register_handlers_menu_games


def register_handlers_games(dp: Dispatcher):
    register_handlers_menu_games(dp)
    register_handlers_add_game(dp)
    register_handlers_update_result_game(dp)
