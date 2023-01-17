from aiogram import Dispatcher


from .start import register_handlers_start
from .tournaments import register_handlers_tournament
from .spam import register_handlers_spam
from .manager import register_handlers_manager


def register_handlers_admin(dp: Dispatcher):
    register_handlers_start(dp)
    register_handlers_manager(dp)
    register_handlers_tournament(dp)
    register_handlers_spam(dp)
