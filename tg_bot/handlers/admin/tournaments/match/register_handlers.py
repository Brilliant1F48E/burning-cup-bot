from aiogram import Dispatcher

from .add_match import register_handlers_add_match


def register_handlers_match(dp: Dispatcher):
    register_handlers_add_match(dp)
