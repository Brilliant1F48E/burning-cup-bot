from aiogram import Dispatcher

from .player import register_handlers_player
from .register import register_handlers_register


def register_handlers_users(dp: Dispatcher):
    register_handlers_player(dp)
    register_handlers_register(dp)
