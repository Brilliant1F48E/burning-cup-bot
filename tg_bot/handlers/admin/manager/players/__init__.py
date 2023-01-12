from aiogram import Dispatcher

from .view_player import register_handlers_view_player


def register_handlers_player(dp: Dispatcher):
    register_handlers_view_player(dp)
